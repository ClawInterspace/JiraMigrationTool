class IssueAttachmentMigrationInfo(object):

    CLOUD_BASE_URL = ''
    CLOUD_USER_NAME = ''
    CLOUD_PASSWORD = ''

    old_issue_key = ''
    # an issue perhaps has more than one attachment
    # [(file_id1, file_name1), (file_id2, file_name2)...]
    attach_info = []

    file_base_path = ''
    new_issue_key = ''

    def __init__(self):
        self.attach_info = []

    def display_all_attach_info(self):
        print self.old_issue_key
        for attach_info in self.attach_info:
            print attach_info[0], attach_info[1]

    @property
    def issue_id(self):
        return self.old_issue_key.split('-')[-1]


class UploadInfo:

    JIRA_CLOUD_BASE_URL = ''
    JIRA_CLOUD_USER_NAME = ''
    JRIA_CLOUD_PASSWORD = ''

    EXPORTED_CSV_PATH = ''
    PROJECT_ATTACHMENT_DATA_DIR = ''
    SOURCE_PROJECT_KEY = ''
    DESTINATION_PROJECT_KEY = ''
