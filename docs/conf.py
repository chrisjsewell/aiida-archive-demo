"""Sphinx configuration"""
import os

project = "AiiDA Version 2.0 Archive Demo"
author = "Chris Sewell"
copyright = f"{author}, 2021"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints", "*.ipynb"]

extensions = ["myst_nb", "sphinx.ext.intersphinx", "sphinx_copybutton", "sphinx_design", "sphinx_thebe"]

myst_enable_extensions = ["colon_fence"]
nb_merge_streams = True
jupyter_execute_notebooks = "cache"
execution_show_tb = "READTHEDOCS" in os.environ

intersphinx_mapping = {
    "aiida": ("https://aiida.readthedocs.io/projects/aiida-core/en/v1.6.5/", None),
}
# note, find things in the inventory with:
# sphobjinv suggest --url "https://aiida.readthedocs.io/projects/aiida-core/en/v1.6.5/objects.inv" Node

html_theme = "sphinx_book_theme"
html_title = "AiiDA v2.0 Archive Demo"
# html_static_path = ["_static"]
# html_css_files = ["custom.css"]
html_logo = "_static/logo-square.svg"
html_theme_options = {
    "home_page_in_toc": True,
    # "single_page": True,
    "show_navbar_depth": 2,
    "repository_url": "https://github.com/chrisjsewell/aiida-archive-demo",
    "repository_branch": "main",
    "use_repository_button": True,
    "use_edit_page_button": True,
    "use_issues_button": True,
    "path_to_docs": "docs",
    "launch_buttons": {
        "notebook_interface": "classic",
        "binderhub_url": "https://mybinder.org",
        "jupyterhub_url": "",
        "thebe": True,
        "colab_url": "https://colab.research.google.com",
    },
}
