---
jupytext:
  formats: md:myst,ipynb
  notebook_metadata_filter: language_info,sd_hide_title
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.4
kernelspec:
  display_name: Python 3
  language: python
  name: python3
language_info:
  name: python
  pygments_lexer: ipython3
sd_hide_title: true
---

# AiiDA Version 2.0 Archive Demo

::::{grid}
:reverse:

:::{grid-item}
:columns: 12 4 4 4

```{image} ./_static/logo-square.svg
:width: 200px
:class: sd-m-auto
```

:::
:::{grid-item}
:columns: 12 8 8 8
:child-align: center
:class: sd-fs-3 sd-text-center sd-font-weight-bold

AiiDA Version 2.0 Archive Demonstrator
:::
::::

+++

This site is a Jupyter Notebook to demonstrate the new [AiiDA](aiida) v2.0 archive functionality (see [aiidateam/aiida-core#5145](https://github.com/aiidateam/aiida-core/pull/5145)).

The new archive gives **full** access to the AiiDA data exploration API,
without the need to import it into a profile, or even have a profile loaded or PostgreSQL installed.
This allows for post-computation analysis and sharing of data with colleagues,
without the usual setup overhead of AiiDA: simply install `aiida-core` and go!

:::{tip}
The outputs of this notebook are dynamically generated on documentation build.
Use the {octicon}`rocket` dropdown at the top of the page to launch interactive sessions.
:::

```{code-cell} ipython3
from aiida import orm, __version__

__version__
```

## Reading the archive version and metadata

After loading the archive format class, we can read the archive version of any legacy archive.

```{code-cell} ipython3
from aiida.tools.archive import get_format

archive_format = get_format()
archive_format.latest_version
```

```{code-cell} ipython3
archive_format.read_version("archives/calc.aiida")
```

If the archive is not at the latest version, you will need to run `verdi archive migrate`, which will migrate the archive to the latest version.

Once the archive is at the current version, we can read the metadata of the archive.
To read data from the archive, similar to a file, we must use the `open` context.

```{code-cell} ipython3
import yaml

with archive_format.open("archives/calc.aiida", mode="r") as archive:
    metadata = archive.get_metadata()
print(yaml.dump(metadata))
```

## Querying the archive

We can load any entity (node, computer, user, etc.) from the archive with the `get` method of the read handle.

```{code-cell} ipython3
with archive_format.open("archives/calc.aiida", mode="r") as archive:
    node = archive.get(orm.Node, uuid="05d64c2c-8f49-446f-bd07-8509d55e0c49")
    print(node)
    print(node.exit_status)
```

Note, if you try to access data from the archive outside of the context of the archive, you will get an error (unless it has already been loaded).

```{code-cell} ipython3
:tags: [raises-exception, hide-output]

node.computer
```

We can access the full `QueryBuilder` interface, to query data in the archive, see [the querying how-to guide](aiida:how-to:data:find).

```{code-cell} ipython3
with archive_format.open("archives/calc.aiida", mode="r") as archive:
    qb = archive.querybuilder()
    qb.append(orm.Node, tag="calc", filters={'uuid': '05d64c2c-8f49-446f-bd07-8509d55e0c49'})
    qb.append(orm.Node, with_incoming="calc")
    print(qb.all())
```

## Visualising the archive provenance

We can use the AiiDA provenance viewer to view the provenance of the archive, see [the tutorial here](aiida:how-to:data:visualise-provenance).
Note, you will need [Graphviz](https://www.graphviz.org/) installed for this feature.

```{code-cell} ipython3
with archive_format.open("archives/calc.aiida", mode="r") as archive:
    graph = archive.graph()
    graph.recurse_descendants("05d64c2c-8f49-446f-bd07-8509d55e0c49")
    graph.recurse_ancestors("05d64c2c-8f49-446f-bd07-8509d55e0c49")
graph.graphviz
```

## Analysing data from the archive

We can now plot data from the outputs of computations, for example using [matplotlib](https://matplotlib.org/).

```{code-cell} ipython3
import matplotlib.pyplot as plt

with archive_format.open("archives/calc.aiida", mode="r") as archive:
    traj = archive.get(orm.Node, pk=19432)
    plt.plot(traj.get_array("energy_hartree"))
    ax = plt.gca()
    ax.set_xlabel("Step")
    ax.set_ylabel("Energy (hartree)")
```

Integration with ASE is also possible, to plot atomic configurations, or even create 3D models (see [ASE viewer for Jupyter notebooks](https://wiki.fysik.dtu.dk/ase/ase/visualize/visualize.html)).

```{code-cell} ipython3
import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms


with archive_format.open("archives/calc.aiida", mode="r") as archive:
    atoms = archive.get(orm.Node, pk=19404).get_ase()

fig, ax = plt.subplots()
ax = plot_atoms(atoms, ax, radii=0.5, rotation=("10x,10y,0z"))
```

```{code-cell} ipython3
from ase.visualize import view


with archive_format.open("archives/calc.aiida", mode="r") as archive:
    atoms = archive.get(orm.Node, pk=19404).get_ase()

view(atoms, viewer='x3d')
```

## Accessing repository files

Finally, we can access files in the repository, for example to read the raw computation log files.

```{code-cell} ipython3
with archive_format.open("archives/calc.aiida", mode="r") as archive:
    folder = archive.get(orm.Node, pk=19406)
    print(folder.list_object_names())
    print(folder.get_object_content('aiida.out')[:988])
```
