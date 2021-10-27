# aiida-archive-demo

A demonstration of the aiida-core version 2.0 archive.

This site is a Jupyter Notebook to demonstrate the new [AiiDA](aiida) v2.0 archive functionality (see [aiidateam/aiida-core#5145](https://github.com/aiidateam/aiida-core/pull/5145)).

## Development

The full development environment is available at using a [Conda](https://conda.io/) environment:

```console
conda env create -f environment.yml
conda activate aiida-archive-demo
```

To convert the Markdown files to Jupyter Notebooks, use [jupytext](https://jupytext.readthedocs.io):

```console
jupytext --to ipynb docs/index.md
```

Once you have added new material, you can sync to the Markdown file:

```console
jupytext --sync docs/index.ipynb
```

To build the docs you can also use [tox](https://tox.readthedocs.io) and [tox-conda](https://tox-conda.readthedocs.io):

```console
tox -e docs-clean
```

or to update the docs using cached data:

```console
tox -e docs-update
```
