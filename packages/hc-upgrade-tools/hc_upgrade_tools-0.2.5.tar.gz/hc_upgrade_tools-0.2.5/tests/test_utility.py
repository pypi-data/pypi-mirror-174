import pytest
import unittest.mock

import hc_upgrade_tools.utility as util

# test util.handle_artifacts
def test_handle_artifacts():
    # test handle_artifacts with source_sub_folder is None
    with unittest.mock.patch('shutil.rmtree') as mock_rmtree:
        with unittest.mock.patch('os.path.exists') as mock_exists:
            with unittest.mock.patch('os.makedirs') as mock_makedirs:
                with unittest.mock.patch('zipfile.ZipFile') as mock_zipfile:
                    # mock logger, return a mock object
                    mock_logger = unittest.mock.Mock()
                    util.get_logger = unittest.mock.Mock(return_value=mock_logger)

                    mock_zipfile.return_value.__enter__.return_value.extractall = unittest.mock.Mock()

                    mock_exists.return_value = True

                    util.handle_artifacts("source_file_path", "target_dir")

                    mock_makedirs.assert_not_called()
                    mock_rmtree.assert_called_once_with("target_dir")

                    assert mock_exists.call_count == 2
                    mock_zipfile.return_value.__enter__.return_value.extractall.assert_called_once_with("target_dir")


    # test handle_artifacts with source_sub_folder is not None
    with unittest.mock.patch('shutil.rmtree') as mock_rmtree:
        with unittest.mock.patch('os.path.exists') as mock_exists:
            with unittest.mock.patch('os.makedirs') as mock_makedirs:
                with unittest.mock.patch('os.makedirs') as mock_oslistdir:
                    #mock zip file with
                    with unittest.mock.patch('zipfile.ZipFile') as mock_zipfile:
                        # mock logger, return a mock object
                        mock_logger = unittest.mock.Mock()
                        util.get_logger = unittest.mock.Mock(return_value=mock_logger)

                        mock_oslistdir.return_value = []
                        mock_exists.return_value = True
                        mock_zipfile.return_value.__enter__.return_value.extractall = unittest.mock.Mock()
                        util.handle_artifacts("source_file_path", "target_dir", "source_sub_folder")

                        mock_rmtree.assert_called_once_with("target_dir")

                        assert mock_exists.call_count == 3
                        mock_makedirs.assert_not_called()

                        mock_zipfile.assert_called_once_with("source_file_path")
                        mock_zipfile.return_value.__enter__.return_value.extractall.assert_called_once_with("target_dir/tmp")
