# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '%(PROJECT_NAME)s'
copyright = '%(YEAR)s, %(AUTHOR_NAMES)s'
author = '%(AUTHOR_NAMES)s'

# The full version, including alpha/beta/rc tags
release = '%(PROJECT_RELEASE)s'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    "sphinx_rtd_theme",
    "myst_parser",
    "sphinx_design",
    "sphinxcontrib.bibtex",
    "sphinx_exercise",
    "sphinx_togglebutton",
    "rst2pdf.pdfbuilder",
]

myst_enable_extensions = ["colon_fence"]

numfig = True # Enable figure, table, code blocks numbering

bibtex_bibfiles = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = '%(PROJECT_LANGUAGE)s'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = [".rst", ".md"]

# List of directives that are to be inserted into the content body
# 1. underline. Usage: :underline:`text to underline`
# 2. add a line break. Usage: text ends with a line break |br|
rst_prolog = """
.. role:: underline
    :class: underline

.. |br| raw:: html

      <br>
"""


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_sidebars = {
    '**': [
        'globaltoc.html',   # Use the global TOC instead of the local one
        'relations.html',   # Adds links to the previous and next chapters
        'searchbox.html',   # Adds a search box
    ]
}

# -- Options for copybutton extension ----------------------------------------
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# -- Options for internationalization ---------------------------------------
locale_dirs = ['locales']
gettext_compact = False  # Ensure separate folders for each language

# Tell Sphinx to look for e.g. slide002_tree_graph.en.png or slide002_tree_graph.fr.png
figure_language_filename = '{root}.{language}{ext}'

import sphinx,os
from pathlib import Path
import shutil

html_context = {
  'current_version' : None,
  'current_language' : None,
  'current_language_code' : None,
  'versions' : [
      ["%(VERSION_NAME)s", None],
      #["jazzy", None]
    ],
  'languages': [
      ["en", "en"],
      ["fr", "fr"]
    ],
  'project_names' :  {
      "en": "%(PROJECT_TITLE_EN)s",
    },
  'logo_path' : {
      "en": "locales/en/logo.svg",
    }
}

LANG_MAP = {
    'en': 'en',
    'fr': 'fr'
}

language_map = {
    'en': {
        "exercise_title_text" : "Exercise",
        "solution_title_text" : "Solution to",
        "togglebutton_hint" : "Click to show",
        "togglebutton_hint_hide" : ""
    },
    'fr': {
        "exercise_title_text" : "Exercice",
        "solution_title_text" : "Solution de",
        "togglebutton_hint" : "Cliquer pour afficher",
        "togglebutton_hint_hide" : ""
    }
}

base_uri = None
config_params = None
version = "%(VERSION_NAME)s" # Set the default version to build the documentation for.

def on_builder_inited(app):
    global base_uri
    outdir = Path(app.outdir)

    if None == base_uri:
        base_uri = outdir.parent.parent
    app.config.html_context['base_url'] = base_uri
    print(f"Base URL set to: {base_uri}")

def on_config_inited(app, config):
    global base_uri
    global version
    global config_params
    global togglebutton_hint
    global togglebutton_hint_hide
    global exercise_title_text
    global solution_title_text

    # global project
    print(f"Language set to: {config.language}")
    if "" != config.html_baseurl:
        base_uri = "https://"+config.html_baseurl
        print(f"Base URL set to: {base_uri}")
    else:
        print(f"Base URL not set")

    # Set the current version
    if config.version is not None and config.version != "":
        version = config.version
        config.html_context['current_version'] = version
    if version is None or version == "":
        raise ValueError("Version is not set. Please set the VERSION_NAME in pkg_generation_config.json.")
    config.html_context['current_version'] = version
    print(f"Version set to: {version}")

    # Also store the current language that Sphinx is building:
    if config.language is not None:
        lg = LANG_MAP[config.language]
        config.html_context['current_language'] = config.language
        config.html_context['current_language_code'] = lg

    # Store the configuration parameters for later use
    config_params = config

def post_process(app, exception):
    global version
    global config_params
    config = config_params
    if config.language is not None:
        if config.language in html_context['project_names'].keys():
            html_logo = html_context['logo_path'][config.language]
            print(f"Logo set to: {html_logo}")
            # Copy the logo file to the static directory of the build
            logo_src = Path(os.path.abspath(__file__)).parent / f"{html_logo}"
            logo_dest = Path(os.path.abspath(__file__)).parent.parent / f"build/html/{version}/{LANG_MAP[config.language]}/_static/logo.svg"
            shutil.copy(logo_src, logo_dest, follow_symlinks=True)

def _dump_exercises(app, doctree):
    from sphinx_exercise.nodes import exercise_node, exercise_enumerable_node
    ex1 = doctree.traverse(exercise_node)
    ex2 = doctree.traverse(exercise_enumerable_node)
    print(f"[DEBUG] Found {len(ex1)} exercise_node, {len(ex2)} exercise_enumerable_node in '{app.builder.name}' build")

def setup(app):
    app.connect('config-inited', on_config_inited)
    app.connect('builder-inited', on_builder_inited)
    app.connect('build-finished', post_process)
    app.connect("doctree-read", _dump_exercises)


# -- Style options
from docutils import nodes
from docutils.parsers.rst import roles

def bold_underline_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = nodes.strong(text, text)
    node['classes'].append('underline')
    return [node], []

roles.register_local_role('bold_underlined', bold_underline_role)

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    "css/custom.css",
]
