"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = hc_upgrade_tools.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys
import os


from hc_upgrade_tools import __version__
from hc_upgrade_tools import subcmd
from hc_upgrade_tools import handl_upgrade
from hc_upgrade_tools import utility as util

__author__ = "shixukai"
__copyright__ = "shixukai"
__license__ = "MIT"


_logger = util.setup_logging("main", "hc_upgrade_tools.main.log", logging.DEBUG)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from hc_upgrade_tools.skeleton import fib`,
# when using this Python module as a library.


def toplevel_function(args):
    # show help if no args or no subcommand
    if not sys.argv[1:]:
        os.system("hc_upgrade_tools --help")
        sys.exit(1)

    if not args.subcommand:
        os.system("hc_upgrade_tools --help")
        sys.exit(1)




def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")

    # add subcommand name test_sub and parser
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")


    parser.add_argument(
        "--version",
        action="version",
        version="hc_upgrade_tools {ver}".format(ver=__version__),
    )

    # add parser --number or -n
    parser.add_argument("--log_output_dir", default=f"/tmp/hc_upgrade_tools/logs/", help="log output dir, default is /tmp/hc_upgrade_tools/logs/")

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    parser.set_defaults(func=toplevel_function)

    subcmd.init_subparser(subparsers)
    handl_upgrade.init_subparser(subparsers)

    final_args = parser.parse_args(args)
    final_args.func(final_args)

    return final_args





def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m hc_upgrade_tools.skeleton 42
    #
    run()
