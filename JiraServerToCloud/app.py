# coding: utf-8

from HelpTools import SrvExportedCsvReader, RenameAttachAgent

USER_NAME = ''
PASSWORD = ''
JIRA_CLOUD_BASE_URL = ''
JIRA_CLOUD_PROJECT_KEY = ''
JIRA_SERVER_PROJECT_KEY = ''

def backup_project_data():
    pass

def remove_thumbs():
    pass

def rename_attachements(base_csv, project_key):
    pass

def upload_attachment_to_issue(issue_key):
    """
    curl -D- -u {username}:{password} -X POST -H "X-Atlassian-Token: nocheck" -F "file=@{path/to/file}" http://{base-url}/rest/api/2/issue/{issue-key}/attachments
    :param issue_key:
    :return:
    """
    pass


if __name__ == "__main__":
    rename_attachements(base_csv, root_folder)