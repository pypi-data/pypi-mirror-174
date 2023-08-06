import asyncio
import logging
from pathlib import Path
from typing import List

import click
import colorlog

from . import build, config_manager, init_project, lib, options, resources, utils


# logging configuration

log = logging.getLogger(__name__)
logging.root.setLevel(logging.INFO)
fmt_string = '%(asctime)s: %(bold)s%(log_color)s%(levelname)-8s%(reset)s - %(name)s: %(message)s'

# console logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(colorlog.ColoredFormatter(fmt_string))
logging.root.addHandler(console_handler)

# file logging
file_handler = logging.FileHandler('atopile.log', mode='w')
# use the colored formatter, but set `no_color` to print to a file in a reasonable format
file_handler.setFormatter(colorlog.ColoredFormatter(fmt_string, no_color=True))
logging.root.addHandler(file_handler)


# cli configuration

def ensure_dir(dir: Path):
    if not dir.exists():
        dir.mkdir(parents=True)
        log.info(f'creating {str(dir)}')


@click.group()
@click.option('--options', '-o', 'options_list', multiple=True)
def cli(options_list: List[str]):
    if options_list:
        options_dict = {}
        for option in options_list:
            k, v = option.split('=', 1)
            v = v.strip('"\' \t\n')
            options_dict[k] = v
        options.update_options(options_dict, options.Level.CLI_OPTION)


@cli.command('options')
def cli_print_options():
    """Show information about configuration options available."""
    print(utils.reindent_str(
        """
        Configuration options.

        Settable via `-o/--options option=value` after `ato`, environment variables, etc...
        In order of increasing precedance:
        """,
        indent = 4
    ))
    for level in options.Level:
        print(f'     - {level.name}')
    print()
    options.print_options()

@cli.command('run')
@click.argument('task')
@options.project_dir.as_click_arg(required=False)
def cli_build(project_dir, task):
    """Build your project."""
    if project_dir:
        options.project_dir.set_value(project_dir, options.Level.CLICK_OPTION)

    build.build(task)

@cli.command('init')
@click.argument('project_dir', 
                type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("-m",
              "--merge",
              is_flag=True,
              show_default=True,
              default=False,
              help="Merge changes with the existing yaml file, preferring the existing file.")
def cli_init(project_dir, merge):
    """
    Add all the atopiley things to your project.
    """
    init_project.init_project(project_dir, merge)
    
@cli.group('kicad-lib')
def kicad_lib():
    pass


# install a resource to the project
@cli.command('install')
@click.argument('which_resources', nargs=-1, required=False)
@click.option('-n', '--name')
@click.option('-b', '--branch')
@options.project_dir.as_click_option()
def cli_install(which_resources, name, branch, project_dir):
    """
    Install a resource into your project if a resource 
    is specified, else, install all resources defined 
    in the config file to this system.

    eg. ato install

    eg. ato install gitlab.atopile.io/atopile/kibot.git

    If you want to specify a branch or name other than default, use the -b or -n flags.
    Note: These are only compatible with a single resource at a time.
    """
    if project_dir:
        options.project_dir.set_value(project_dir, options.Level.CLICK_OPTION)

    config_data = config_manager.load()

    # make sure the urls are unqiue
    current_resources = resources.parse_resources(config_data['resources'])

    # figure out what to install based on the args
    if which_resources:
        # if we're insalling something new
        if name or branch:
            if len(which_resources) > 1:
                log.error('You can only specify a name or branch for a single resource.')
                exit(1)
            else:
                resources_to_install = [resources.GitResource.from_url(which_resources[0], branch, name)]
        else:
            resources_to_install = [resources.GitResource.from_url(url) for url in which_resources]

        # make sure we don't have any duplicates or they're already installed
        resource_refs_to_install = set(r.reference for r in resources_to_install)
        current_resources = set(r.reference for r in current_resources)

        already_installed_refs = resource_refs_to_install.intersection(current_resources)
        for r in already_installed_refs:
            log.warning(f'{r} is already installed. Ignoring it now. Run update instead if you want to update it to the latest version.')
        resource_refs_to_install -= already_installed_refs
        resources_to_install = [r for r in resources_to_install if r.reference in resource_refs_to_install]
        
        # modify the config data if applicable
        config_data.setdefault('resources', []).extend(r.to_dict() for r in resources_to_install)
        config_manager.save()
        
    else:
        # if no arguments are provided, install all resources from the current project definition
        resources_to_install = current_resources

    # install the resources
    if resources_to_install:
        resource_refs = ', '.join(r.reference for r in resources_to_install)
        log.info(f'Installing {resource_refs}')
        resources.install_resources(resources_to_install)
    else:
        log.warning('No resources to install.')


# update a resource
@cli.command('update')
@click.argument('which_resources', nargs=-1, required=False)
@options.project_dir.as_click_option()
def cli_update(which_resources, project_dir):
    """
    Update a resource in your project if a resource
    """
    if project_dir:
        options.project_dir.set_value(project_dir, options.Level.CLICK_OPTION)

    config_data = config_manager.load()

    # figure out what to install based on the args
    if which_resources:
        resources_to_update = []
        for which_resource in which_resources:
            try:
                resources_to_update.append(resources.interpret_ref(which_resource))
            except FileNotFoundError:
                log.error(f'Could not find {which_resource} in the project. Maybe it needs to be installed?')
                exit(1)
    else:
        resources_to_update = resources.parse_resources(config_data['resources'])

    resources_to_update: List[resources.AbstractResource] = list(set(resources_to_update))

    if resources_to_update:
        resource_refs = ', '.join(r.reference for r in resources_to_update)
        log.info(f'Updating {resource_refs}')
        resources.install_resources(resources_to_update)
    else:
        log.warning('No resources to update.')


@kicad_lib.command('add')
@click.argument('lib_to_add')
@click.argument('kicad_project')
@options.project_dir.as_click_option()
def cli_add_kicad_lib(lib_to_add, kicad_project, project_dir):
    """Add a new library to the project's dependencies."""
    if project_dir:
        options.project_dir.set_value(project_dir, options.Level.CLICK_OPTION)
    project_dir = options.project_dir.value
    config_data = config_manager.load()

    # figure out which kicad project the user's talking about
    kicad_project = utils.resolve_project_relative_ref(kicad_project)
    if not kicad_project.suffix == '.kicad_pro':
        log.error(f'{kicad_project} is not a .kicad_pro file.')
        exit(1)

    # figure out which library the user's talking about
    lib_to_add = resources.interpret_ref(lib_to_add)

    # if the user referenced a directory, index it for them
    # otherwise, add the library to the project's dependencies
    if (project_dir / lib_to_add).is_dir():
        lib.index_kicad_libs(indexing_path=lib_to_add, kicad_project=kicad_project)
    else:
        lib_list = config_data.setdefault('libs', {}).setdefault(str(kicad_project), [])
        if str(lib_to_add) not in lib_list:
            lib_list.append(str(lib_to_add))

    lib.dump_kicad_lib_tables()

    config_manager.save()


if __name__ == '__main__':
    cli()
