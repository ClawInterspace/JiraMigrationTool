# coding: utf-8

import logging
import getpass
import sys, os

from Log import get_logger
from MigrationInterface import UploadInfo
from HelpTools import SrvExportedCsvReader, UploadAttachAgent

logger = get_logger('./logging.ini')
logging.debug('logger start!')

if len(sys.argv) != 6:
    print 'python app.py <jira_cloud_base_url> <exported_csv_path> ' \
          '<attachment_root_folder> <old_project_key> <new_project_key>'
    sys.exit(0)


upload_info = UploadInfo()

upload_info.JIRA_CLOUD_BASE_URL = sys.argv[1]
upload_info.EXPORTED_CSV_PATH = sys.argv[2]
upload_info.PROJECT_ATTACHMENT_DATA_DIR = os.path.abspath(sys.argv[3])
upload_info.SOURCE_PROJECT_KEY = sys.argv[4]
upload_info.DESTINATION_PROJECT_KEY = sys.argv[5]
upload_info.JIRA_CLOUD_USER_NAME = raw_input('Please type jira cloud user name:')
upload_info.JRIA_CLOUD_PASSWORD = getpass.getpass('Pleases type jira cloud password:')

logging.debug(upload_info.JIRA_CLOUD_BASE_URL)
logging.debug(upload_info.PROJECT_ATTACHMENT_DATA_DIR)
logging.debug(upload_info.SOURCE_PROJECT_KEY)
logging.debug(upload_info.DESTINATION_PROJECT_KEY)

logging.debug(upload_info.EXPORTED_CSV_PATH)
logging.debug(upload_info.JIRA_CLOUD_USER_NAME)
logging.debug('*******')

csv_reader = SrvExportedCsvReader(upload_info.EXPORTED_CSV_PATH)
csv_reader.build_attach_name_info()

upload_agent = UploadAttachAgent(csv_reader.issue_attach_info, upload_info)

upload_agent.remove_all_thumbs()
upload_agent.rename_all_files()
upload_agent.upload_all_attachs()
