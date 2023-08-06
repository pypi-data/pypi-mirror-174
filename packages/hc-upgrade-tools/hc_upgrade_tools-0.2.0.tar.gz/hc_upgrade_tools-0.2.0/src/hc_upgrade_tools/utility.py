# import a lib can handle http request
import logging
import os
import stat
import logging.handlers
import http.client, urllib.parse
from pickle import FALSE, NONE
import shutil
import datetime
import re

_logger = None

def get_logger():
    global _logger

    if  _logger:
        return _logger
    else:
        _logger = setup_logging("utility", "hc_upgrade_tools.utility.log", logging.DEBUG)
        return _logger

# use setup_logging function declare later

def setup_logging(logger_name, log_file_name, loglevel=logging.DEBUG, log_output_dir="/tmp/hc_upgrade_tools/logs/"):
    """Setup logging configuration

    Args:
      logger_name (str): logger name
      log_file_name (str): log file name
      loglevel (int): log level
      log_output_dir (str): log output dir

    Returns:
      :obj:`logging.Logger`: logger instance
    """

    if not os.path.exists(log_output_dir):
        # mkdir recursively
        os.makedirs(log_output_dir)

    #filename=f"{log_output_dir}/.hc_upgrade_tools/hc_upgrade_tools.log",
    filename = os.path.join(log_output_dir, log_file_name)

    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"

    logger = logging.getLogger(logger_name)

    formatter = logging.Formatter(logformat)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    rotate_file_handler = logging.handlers.RotatingFileHandler(
        filename=filename,
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
        mode="a",
    )
    # rotate_file_handler set formatter
    rotate_file_handler.setFormatter(formatter)

    logger.setLevel(loglevel)
    # add handler
    logger.addHandler(rotate_file_handler)
    logger.addHandler(stream_handler)

    return logger


def download_artifact(artifact_host, artifact_port, remote_path, project_id, original_artifacts_download_dir, artifact_name):
    """Download artifact

    Args:
      artifact_host (str): artifact host
      artifact_port (int): artifact port
      remote_path (str): remote path
      project_id (str): int
      original_artifacts_download_dir (str): artifact dir
      artifact_name (str): artifact name

    Returns:
      str: artifact path
    """
    logger = get_logger()

    if not os.path.exists(original_artifacts_download_dir):
        os.makedirs(original_artifacts_download_dir)
    artifact_path = os.path.join(original_artifacts_download_dir, artifact_name)

    try:
        #encode request params

        request_params = urllib.parse.urlencode({"projectID": project_id})

        with open(artifact_path, "wb") as f:
            conn = http.client.HTTPConnection(artifact_host, artifact_port,  timeout=300)

            # request with query request_params
            conn.request("GET", remote_path + "?" + request_params)
            response = conn.getresponse()

            logger.info(f"download artifacts response status is {response.status}")

            if response.status != 200:
                raise Exception("download artifact failed")

            while True:
                chunk = response.read(1024)
                if not chunk:
                    break
                f.write(chunk)
            f.close()
            conn.close()

            # download artifact bytes stream
            logger.info(f"download artifact {artifact_name} success")
            return artifact_path

    except Exception as error:
        print(f"download artifact failed, error is {error}")

        return None


def handle_artifacts(source_file_path, target_dir, source_sub_folder=None):
    """讲交付物解压到指定目录

    Args:
      source_file_path (str): 交付物路径
      target_dir (str): 目标目录
      source_sub_folder (str): 指定只需要的交付物中的子目录
    """
    logger = get_logger()

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # source file is a zip file
    # unzip source file to target dir, handle exceptions
    try:
        import zipfile
        with zipfile.ZipFile(source_file_path) as z:
            temp_target_dir = os.path.join(target_dir, "tmp")


            if not source_sub_folder:
                z.extractall(target_dir)
            else:
                if not os.path.exists(temp_target_dir):
                    os.makedirs(temp_target_dir)
                # temp target dir is target dir + "tmp"
                # clean temp target dir
                z.extractall(temp_target_dir)
                # move all files in temp_target_dir/source_sub_dir to target_dir
                for file in os.listdir(os.path.join(temp_target_dir, source_sub_folder)):
                    os.rename(os.path.join(temp_target_dir, source_sub_folder, file), os.path.join(target_dir, file))

                # remove temp_target_dir all
                shutil.rmtree(temp_target_dir)

                # walk file named  "wait_for_db_ready.sh" nested in target_dir
                for root, dirs, files in os.walk(target_dir):
                    for file in files:
                        if file == "wait_for_db_ready.sh":
                            logger.info(f"find wait_for_db_ready.sh in {root}")
                            st = os.stat(os.path.join(root, file))
                            os.chmod(os.path.join(root, file), st.st_mode | stat.S_IEXEC)

    except Exception as error:
        print(f"unzip source file failed, error is {error}")
        return FALSE

    logger.info(f"handle artifacts success, target dir is {target_dir}")
    return True


def create_new_release_dir(release_root_dir, max_history_release_count=5):
    # release dir like: 20210514175142
    release_dir = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    release_dir = os.path.join(release_root_dir, release_dir)
    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    # sort release dir name match like 20210514175142 and make sure release dir is a dir
    # keep latest max_history_release_count release dir
    release_dir_list = [os.path.join(release_root_dir, release_dir_name) for release_dir_name in os.listdir(release_root_dir) if
                    os.path.isdir(os.path.join(release_root_dir, release_dir_name)) and
                    re.match(r"\d{14}", release_dir_name)]

    release_dir_list = sorted(release_dir_list, key=lambda x: os.path.getmtime(x), reverse=True)

    if len(release_dir_list) > max_history_release_count:
        for dir in release_dir_list[max_history_release_count:]:
            shutil.rmtree(dir)

    return release_dir


def link_current_to_new_release(link_current_symbol, target_release_dir):
    # if symbolic exists, remove it
    if os.path.islink(link_current_symbol):
        os.remove(link_current_symbol)

    # link current to new release
    os.symlink(target_release_dir, link_current_symbol)


def handle_extra_links(args):
    # element in link_list is a string like: link_symbolic:source_path
    # create all the link symbolics
    link_list = args.extra_symbolics

    for link in link_list:
        link_symbolic, source_path = link.split(":")

        # prefix args.project_dir to source_path and link_symbolic
        link_symbolic = os.path.join(args.project_dir, link_symbolic)
        source_path = os.path.join(args.project_dir, source_path)

        if os.path.islink(link_symbolic):
            os.remove(link_symbolic)
        os.symlink(source_path, link_symbolic)


if __name__ == "__main__":
    #download url :http://10.0.20.115:7070/api/githook/request-artifacts
    artifacts_path =  download_artifact("10.0.20.115", 7070, "/api/githook/request-artifacts", 196, "/tmp/hc_upgrade_tools/artifacts/", "test.tar.gz")
    if artifacts_path:
        handle_artifacts(artifacts_path, "/tmp/hc_upgrade_tools/build/", source_sub_folder="archive/backend/build")
