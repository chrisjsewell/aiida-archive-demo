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
The archive allows

:::{tip}
Use the {octicon}`rocket` dropdown at the top of the page to launch interactive sessions.
:::

```{code-cell} ipython3
from aiida import orm, __version__
from aiida.tools.archive import get_format

archive_format = get_format()

__version__, archive_format.latest_version
```

```{code-cell} ipython3
archive_format = get_format()
archive_format.read_version("archives/calc.aiida")
```

```{code-cell} ipython3
import yaml

with archive_format.open("archives/calc.aiida", mode="r") as archive:
    metadata = archive.get_metadata()
print(yaml.dump(metadata))
```

```{code-cell} ipython3
with archive_format.open("archives/calc.aiida", mode="r") as archive:
    node = archive.get(orm.Node, uuid="05d64c2c-8f49-446f-bd07-8509d55e0c49")
    print(node)
    print(node.exit_status)
```

```{code-cell} ipython3
:tags: [raises-exception, hide-output]

node.computer
```

```{code-cell} ipython3
with archive_format.open("archives/calc.aiida", mode="r") as archive:
    qb = archive.querybuilder()
    qb.append(orm.Node, tag="calc", filters={'uuid': '05d64c2c-8f49-446f-bd07-8509d55e0c49'})
    qb.append(orm.Node, with_incoming="calc")
    print(qb.all())
```

```{code-cell} ipython3
with archive_format.open("archives/calc.aiida", mode="r") as archive:
    graph = archive.graph()
    graph.recurse_descendants("05d64c2c-8f49-446f-bd07-8509d55e0c49")
    graph.recurse_ancestors("05d64c2c-8f49-446f-bd07-8509d55e0c49")
graph.graphviz
```

```{code-cell} ipython3
import matplotlib.pyplot as plt

with archive_format.open("archives/calc.aiida", mode="r") as archive:
    traj = archive.get(orm.Node, pk=19432)
    plt.plot(traj.get_array("energy_hartree"))
    ax = plt.gca()
    ax.set_xlabel("Step")
    ax.set_ylabel("Energy (hartree)")
```

```{code-cell} ipython3
import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms


with archive_format.open("archives/calc.aiida", mode="r") as archive:
    atoms = archive.get(orm.Node, pk=19404).get_ase()

fig, ax = plt.subplots()
plot_atoms(atoms, ax, radii=0.5, rotation=("10x,10y,0z"))
```

```{code-cell} ipython3
from ase.visualize import view


with archive_format.open("archives/calc.aiida", mode="r") as archive:
    atoms = archive.get(orm.Node, pk=19404).get_ase()

view(atoms, viewer='x3d')
```

```{code-cell} ipython3
with archive_format.open("archives/calc.aiida", mode="r") as archive:
    folder = archive.get(orm.Node, pk=19406)
    print(folder.list_object_names())
    print(folder.get_object_content('aiida.out')[:988])
```
