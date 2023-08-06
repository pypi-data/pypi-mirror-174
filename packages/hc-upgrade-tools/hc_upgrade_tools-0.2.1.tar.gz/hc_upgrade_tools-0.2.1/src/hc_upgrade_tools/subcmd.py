import logging
from hc_upgrade_tools import utility as util


# get logger for this file
_logger = util.setup_logging("sub_cmd", "hc_upgrade_tools.sub.cmd.log", logging.DEBUG)



# init sub command parser as subparser of skeleton.py
# subparser add_argument in this file
def init_subparser(subparsers):
    """Init sub command parser as subparser of skeleton.py

    Args:
      subparsers (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    subparser = subparsers.add_parser("sub1", help="sub command help")

    subparser.add_argument("--foo2", help="foo help")

    # add argument for loglevel
    subparser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    subparser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    subparser.set_defaults(func=run_sub)

    return subparser


def run_sub(args):
    _logger.debug("run_sub")
    pass
