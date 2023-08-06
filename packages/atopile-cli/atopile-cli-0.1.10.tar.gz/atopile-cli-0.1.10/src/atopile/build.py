
import asyncio
import logging
import shutil
import traceback
from pathlib import Path
from typing import Dict, List

import aiodocker
from attr import define
from tqdm import tqdm

from . import config_manager, options, scan
from .stages import Stage
from .tree import TreeView

program_log = logging.getLogger(__name__)

@define
class Build:
    docker: aiodocker.Docker
    build_graph: scan.BuildGraph
    build_log: logging.Logger
    job_semaphores: asyncio.locks.Semaphore
    done: List[str] = []

    def mark_stage_done(self, stage_ref: str):
        """
        Mark a stage done, assert it's outputs were generated, else raise an error
        """
        for output_node in self.build_graph.get_outputs(stage_ref):
            output = self.build_graph.nodes[output_node]['io']
            if output.exists():
                self.done.append(output_node)
            else:
                self.build_log.error(f'{stage_ref} didn\'t produce {str(output_node)} as expected')
        self.done.append(stage_ref)

    def get_ready_to_run_stages(self) -> Dict[str, Stage]:
        ready_to_run = {}
        for stage_ref, stage in self.build_graph.stages.items():
            upstream = self.build_graph.direct_upstream_nodes(stage_ref)
            for ref in upstream:
                node = self.build_graph.nodes[ref]
                if ref not in self.done:
                    if node['type'] == scan.NodeType.IO and isinstance(node['io'], scan.File):
                        pass
                    else:
                        # something part of build-time isn't ready quite yet
                        break
            else:
                # everything below is ready
                ready_to_run[stage_ref] = stage
        return ready_to_run

    async def _run_stage(self, stage_ref: str):
        try:
            async with self.job_semaphores:
                build_dir: Path = options.build_dir.value / stage_ref
                build_dir.mkdir(parents=True, exist_ok=True)

                stage = self.build_graph.stages[stage_ref]
                inputs = self.build_graph.get_inputs(stage_ref)

                # run the stage
                exit_status = await stage.run(self.docker, inputs)

                # copy files to dist
                for output_name, dist_location in stage.dist.items():
                    if output_name in stage.outputs:
                        output_paths = stage.outputs[output_name].fs_location
                        pass
                    else:
                        output_paths = list(build_dir.glob(output_name))
                        if not output_paths:
                            self.build_log.warning(f'Couldn\'t find {output_name} in {build_dir}')
                            continue

                    if not isinstance(output_paths, list):
                        output_paths = [output_paths]

                    for output_path in output_paths:
                        dist: Path = options.dist_dir.value
                        if dist_location:
                            dist = dist / dist_location
                        dist.mkdir(parents=True, exist_ok=True)
                        shutil.copy(str(output_path), str(dist / output_path.name))

                # mark the stage done so others depending on it can run
                self.mark_stage_done(stage_ref)

        except Exception as e:
            program_log.error(f'Error running {stage_ref}. Printing traceback:')
            for line in traceback.format_exc().splitlines():
                program_log.error(line)
            raise e

        # check its success
        if exit_status != 0:
            self.build_log.error(f'{stage_ref} failed')
            raise RuntimeError

    async def run(self, until_dead: bool = False) -> int:
        # pull all images to make sure we've got them locally
        program_log.info('Hold tight! This may take a few minutes...')
        images = aiodocker.docker.DockerImages(self.docker)
        for stage in tqdm(self.build_graph.stages.values()):
            await images.pull(stage.stage_def.image)

        remaining_stages = set(self.build_graph.stages.keys()).difference(self.done)
        stage_runner_tasks: Dict[str, asyncio.Task] = {}

        level = 0

        # as long as there's stuff to do
        while remaining_stages:
            # check on existing tasks
            for stage_ref in list(stage_runner_tasks.keys()):
                task = stage_runner_tasks[stage_ref]
                if task.done():
                    del stage_runner_tasks[stage_ref]
                    ex = task.exception()
                    if ex:
                        level = logging.ERROR
                        self.build_log.error(f'{stage_ref} failed with exception {repr(ex)}')
            
            # cancel remaining tasks
            if not until_dead and level >= logging.ERROR:
                for task in stage_runner_tasks.values():
                    if not task.done():
                        task.cancel()
                        self.build_log.warning(f'Cancelled {task.get_name()}')
                self.build_log.warning('Cancelled remaining tasks')
                break

            # schedule new tasks
            ready_to_run = set(self.get_ready_to_run_stages().keys())
            ready_and_unscheduled = ready_to_run.intersection(remaining_stages)
            for stage_ref in ready_and_unscheduled:
                task = asyncio.create_task(self._run_stage(stage_ref))
                stage_runner_tasks[stage_ref] = task
                remaining_stages.remove(stage_ref)
            
            # polling rate limiter
            await asyncio.sleep(1)

        # wait for them all to finish
        await asyncio.gather(*list(stage_runner_tasks.values()))
        await self.docker.close()
        return level

    @classmethod
    def from_build_graph(cls, build_graph: scan.BuildGraph, workers: int = 8) -> 'Build':
        try:
            docker = aiodocker.Docker()
        except ValueError:
            program_log.error('Docker isn\'t running')
            raise

        job_semaphores = asyncio.locks.Semaphore(workers)
        build_log = logging.getLogger(build_graph.name)

        return cls(
            docker=docker,
            build_graph=build_graph,
            build_log=build_log,
            job_semaphores=job_semaphores,
        )

def build(goal_name: str):
    logger_goal_name = goal_name.replace('.', '_')
    build_log = logging.getLogger(f'build.{logger_goal_name}')

    config_data = config_manager.load()

    project_name = config_data.get('name') or 'untitled'
    build_log.info(f'Building {project_name}!')

    if goal_name not in config_data.get('tasks', {}):
        build_log.error(f'Nothing to do for task {goal_name}')
        exit(1)

    stages = Stage.from_goal_name(goal_name)
    build_graph = scan.BuildGraph.from_stages(config_data['name'], stages)

    build_log.info('=== Build Tree ===')
    tree_view = TreeView.from_build_graph(build_graph)
    build_log.info(str(tree_view))

    build = Build.from_build_graph(build_graph)

    loop = asyncio.get_event_loop()
    exit_logging_level = loop.run_until_complete(build.run())
    loop.close()

    exit(int(exit_logging_level > logging.WARNING))
