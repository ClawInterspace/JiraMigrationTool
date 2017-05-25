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