# coding: utf-8

import logging
from Log import get_logger
from HelpTools import SrvExportedCsvReader, UploadAttachAgent


logger = get_logger('./logging.ini')
logging.debug('logger start!')

JIRA_CLOUD_USER_NAME = ''
JRIA_CLOUD_PASSWORD = ''
JIRA_CLOUD_BASE_URL = ''
JIRA_CLOUD_PROJECT_KEY = ''
JIRA_SERVER_PROJECT_KEY = ''


