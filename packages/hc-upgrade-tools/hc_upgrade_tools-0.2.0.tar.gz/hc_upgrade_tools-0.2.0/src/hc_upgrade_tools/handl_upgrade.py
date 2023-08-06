import logging
from hc_upgrade_tools import utility as util
import os


# get logger for this file
_logger = util.setup_logging(
    "download_pkg", "hc_upgrade_tools.download.log", logging.DEBUG
)

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
    subparser = subparsers.add_parser("dl-pkg", help="sub command help")

    # add argument "--host"
    subparser.add_argument(
        "--host", help="host name or ip address", type=str, metavar="STR", required=True
    )
    # add argument "--port"
    subparser.add_argument(
        "--port", help="port number", type=int, metavar="INT", required=True
    )
    # add argument resource-path
    subparser.add_argument(
        "--resource-path",
        help="resource path",
        type=str,
        metavar="STR",
        default="/api/githook/request-artifacts",
    )
    # add argument "projectID"
    subparser.add_argument("--projectID", help="project ID", type=str, metavar="STR")
    # add argument "project-dir"
    subparser.add_argument(
        "--project-dir",
        help="项目跟目录",
        type=str,
        metavar="STR",
        required=True,
    )
    # add argument "release-root-dir"
    subparser.add_argument(
        "--release-root-dir",
        help="releases 默认在项目根目录下的releases目录, 也可以通过此参数指定",
        type=str,
        metavar="STR",
    )
    # add argument "target-source-sub-folder-in-artifact"
    subparser.add_argument(
        "--target-sub-folder-in-artifact",
        help="交付物解压后的目标文件件",
        type=str,
        metavar="STR",
    )
    # add list argument "extra-links"
    subparser.add_argument(
        "--extra-symbolics",
        help="额外链接, 相对于项目的根目录。例如：--extra-symbolics 'current/dock-compose.yml:shared/dock-compose.yml', 'current/config:shared/config' \
            形式为： symbolic_link_path:source_path",
        type=str,
        metavar="STR",
        nargs="*",
        default=[],
    )

    subparser.set_defaults(func=main_process)

    return subparser


def main_process(args):
    upgrade_porcess_root_dir = "/tmp/hc_upgrade_tools"

    project_id = args.projectID
    original_artifacts_download_dir = os.path.join(upgrade_porcess_root_dir, "artifacts")
    artifact_name = "artifact.zip"

    artifacts_path = util.download_artifact(
        args.host, args.port, args.resource_path, project_id, original_artifacts_download_dir, artifact_name
    )
    _logger.debug(f"artifacts_path: {artifacts_path}")
    _logger.debug(f"upgrade_porcess_root_dir: {upgrade_porcess_root_dir}")

    if artifacts_path:
        # releases 默认在项目根目录下的releases目录
        project_release_dir = os.path.join(args.project_dir, "releases")

        if args.release_root_dir:
            project_release_dir = args.release_root_dir

        # 生成目标文件，以日期为文件名
        target_release_dir = util.create_new_release_dir(project_release_dir)
        _logger.debug(f"target_release_dir: {target_release_dir}")

        util.handle_artifacts(
            artifacts_path,
            target_release_dir,
            source_sub_folder=args.target_sub_folder_in_artifact,
        )

        # 将目标文件夹软连接到current目录
        current_link = os.path.join(args.project_dir, "current")
        util.link_current_to_new_release(current_link, target_release_dir)


        # 创建其他额外的链接
        _logger.debug(f"extra_symbolics: {args.extra_symbolics}")
        util.handle_extra_links(args)
