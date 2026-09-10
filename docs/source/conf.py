# Configuration file for the Sphinx documentation builder.

# -- Project information

project = "Rail Express"
copyright = "2026, FANNΞC"
author = "FANNΞC"

release = "1.0.0"
version = "1.0.0"

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx_rtd_theme",
]

autosectionlabel_prefix_document = True
html_show_sourcelink = False
html_theme_options = {
    "display_version": False,  # Hides version number
    "version_dropdown": False, # Hides dropdown
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"
