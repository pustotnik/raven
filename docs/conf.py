# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
from os import path
import sys

HERE = path.dirname(path.abspath(__file__))
ZENMAKE_DIR = path.join(path.pardir, 'src', 'zenmake')
sys.path.insert(0, path.abspath(ZENMAKE_DIR))

from zm.constants import APPNAME, CAP_APPNAME, AUTHOR, COPYRIGHT_ONE_LINE
from zm import version as _ver
from zm.pyutils import _t

# -- Project information -----------------------------------------------------

project = _t(CAP_APPNAME)
copyright = _t(COPYRIGHT_ONE_LINE)
author = _t(AUTHOR)

# The short X.Y version
version = _t('.'.join(_ver.current().split('.')[:2]))
# The full version, including alpha/beta/rc tags
release = _t(_ver.current())


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    #'sphinx.ext.autodoc',
    #'sphinx.ext.ifconfig',
    #'sphinx.ext.viewcode',
    #'sphinx.ext.intersphinx',
    #'sphinxcontrib.spelling',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
#source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = [_t('_build'), 'Thumbs.db', '.DS_Store', _t('*.inc')]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# These values determine how to format the current date, used as the replacement for |today|.
# - If you set today to a non-empty value, it is used.
# - Otherwise, the current time is formatted using time.strftime() and the
#   format given in today_fmt.
# The default is now today and a today_fmt of '%B %d, %Y' (or, if translation is
# enabled with language, an equivalent format for the selected locale).
today_fmt = '%Y-%m-%d'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
#html_theme = 'agogo'
#html_theme = 'haiku'

# sphinx_rtd_theme
sys.path.insert(0, path.join(HERE, '_themes'))
import sphinx_rtd_theme
extensions.append('sphinx_rtd_theme')
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': False,
    'display_version' : False,
}
#if sphinx_rtd_theme.__version__ > '4.2':
#    html_theme_options['style_nav_header_background'] = '#4c3a7a'
html_theme_options['style_nav_header_background'] = '#4c3a7a'
html_theme_path = ["_themes", ]

# This causes wide tables to wrap content within their cells rather than
# producing a table with a scroll bar see
# https://github.com/readthedocs/sphinx_rtd_theme/issues/117 for details.
# https://rackerlabs.github.io/docs-rackspace/tools/rtd-tables.html
html_context = {
    'css_files': [
        '_static/theme_overrides.css',  # fix wide tables in RTD theme
    ],
}

# sphinx_bootstrap_theme
#import sphinx_bootstrap_theme
#html_theme = 'bootstrap'
#html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
#html_theme_options = {
#}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If false, no index is generated.
#html_use_index = False

# If this is not None, a ‘Last updated on:’ timestamp is inserted at every page
# bottom, using the given strftime() format. The empty string is equivalent
# to '%b %d, %Y' (or a locale-dependent equivalent).
html_last_updated_fmt = '%Y-%m-%d'

# If given, this must be the name of an image file (path relative to the
# configuration directory) that is the logo of the docs. It is placed at the
# top of the sidebar; its width should therefore not exceed 200 pixels.
# Default: None.
#html_logo = '_static/logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/logo.ico'

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'zenmakedoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, '%s.tex' % CAP_APPNAME, _t('%s Documentation' % CAP_APPNAME),
     _t(author), 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, APPNAME, _t('%s Documentation' % CAP_APPNAME),
     [author], 1)
]

man_show_urls = True

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, CAP_APPNAME, _t('%s Documentation' % CAP_APPNAME),
     author, CAP_APPNAME, 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

#intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
