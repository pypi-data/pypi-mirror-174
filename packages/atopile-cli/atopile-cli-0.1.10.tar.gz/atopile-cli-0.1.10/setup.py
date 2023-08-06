import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='atopile-cli',
    version='0.1.10',
    author='Matthew Wildoer',
    author_email='mawildoer@gmail.com',
    description=('The atopile command line interface.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://atopile.io/',
    install_requires=[
        'attrs',
        'aiodocker',
        'click',
        'colorlog',
        'ruamel.yaml',
        'networkx',
        'termcolor',
        'treelib',
        'GitPython',
        'tqdm',
    ],
    packages=setuptools.find_packages(where='src'),
    package_dir = {'': 'src'},
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'ato = atopile.cli:cli',
        ]
    }
)