# coding: utf-8
import logging
import csv
from itertools import count
import os
import subprocess
import shutil

from MigrationInterface import IssueAttachmentMigrationInfo


def remap(fieldnames, duplicated_field_name):
    price_count = count(1)
    return [duplicated_field_name + '{}'.format(next(price_count))
            if f.startswith(duplicated_field_name) else f
            for f in fieldnames]


class SrvExportedCsvReader(object):

    issue_attach_info = {}
    # {old_issue_key: IssueAttachmentMigrationInfo}

    def __init__(self, file_path):
        """

        :param file_path:
        """
        self.issue_attach_info = {}
        self._file_path = file_path

    def build_attach_name_info(self):

        with open(self._file_path, 'rb') as csvfile:

            reader = csv.reader(csvfile)

            # fn: field name
            fn_issue_key = 'Issue key'
            fn_attachment = 'Attachment'

            # rename field name to avoid duplicated field(attachment) name
            fieldnames = remap(next(reader), fn_attachment)

            for row in reader:

                row = dict(zip(fieldnames, row))

                tmp_issue = IssueAttachmentMigrationInfo()
                tmp_issue.old_issue_key = row[fn_issue_key]

                logging.debug(row[fn_issue_key])

                for field_name, field_value in row.iteritems():
                    if field_name.startswith(fn_attachment) and field_value.strip() != "":
                        file_id, file_name = \
                            self._extract_attach_info_from_csv_value(field_value)
                        tmp_issue.attach_info.append((file_id, file_name))

                if len(tmp_issue.attach_info) > 0:
                    self.issue_attach_info[tmp_issue.old_issue_key] = tmp_issue

    @classmethod
    def _extract_attach_info_from_csv_value(cls, cell_value):
        """
        
        :param cell_value:
         example value, "19/May/17 5:33 PM;alanliu;jira-migration-drill-a.png;http://192.168.2.222/secure/attachment/10100/jira-migration-drill-a.png"
        :return: 
        """
        segments = cell_value.split(';')

        try:
            # TODO: more specific format checking
            date = segments[0]
            user_name = segments[1]
            file_name = segments[2]
            file_url = segments[3]
            file_id = file_url.strip().split('/')[-2]

            file_name_encode = file_name.replace(' ', '_')

        except Exception as e:
            raise Exception('cell value format error: "%s"' % cell_value)

        return file_id, file_name_encode


class UploadAttachAgent(object):

    """
    Responsible for rename all attachment files to correct file name.
    # TODO: doesn't know project id from exported file
    """

    def __init__(self, issue_migra_info, upload_info):

        # get project folder absolutely path
        self._src_proj_key = upload_info.SOURCE_PROJECT_KEY
        self._proj_attach_root = os.path.abspath(upload_info.PROJECT_ATTACHMENT_DATA_DIR)
        self.issue_migra_info = issue_migra_info
        self.upload_info = upload_info

    def remove_all_thumbs(self):
        """

        :return:
        """

        proj_root_dir = self._proj_attach_root

        all_issue_dirs = []
        for file_or_dir in os.listdir(proj_root_dir):

            cur_path = os.path.join(proj_root_dir, file_or_dir)
            if os.path.isdir(cur_path):
                all_issue_dirs.append(cur_path)
                # remove all thumbs
                try:
                    thumbs_dir = os.path.join(cur_path, 'thumbs')
                    shutil.rmtree(thumbs_dir)
                except Exception:
                    logging.error('Remove "%s" failed' % thumbs_dir)

        return True

    def rename_all_files(self):

        proj_root_dir = self._proj_attach_root
        migrate_data = self.issue_migra_info

        for issue_key, issue_info in migrate_data.iteritems():
            for file_id, file_name in dict(issue_info.attach_info).iteritems():
                old_attach_path = os.path.join(proj_root_dir, issue_key, file_id)
                new_attach_path = os.path.join(proj_root_dir, issue_key, file_name)
                if os.path.isfile(old_attach_path):
                    try:
                        os.rename(old_attach_path, new_attach_path)
                    except Exception:
                        logging.error('Rename "{%s}" failed' % old_attach_path)
                else:
                    logging.error('Cannot find "%s"' % old_attach_path)

        return True

    def upload_all_attachs(self):

        proj_root_dir = self._proj_attach_root
        migrate_data = self.issue_migra_info
        upload_info = self.upload_info

        for issue_key, issue_info in migrate_data.iteritems():
            for file_id, file_name in dict(issue_info.attach_info).iteritems():
                file_path = os.path.join(proj_root_dir, issue_key, file_name)
                # upload the attachment
                cloud_issue_key = upload_info.DESTINATION_PROJECT_KEY\
                                  + '-' + issue_info.issue_id

                self.upload_attach(
                    upload_info.JIRA_CLOUD_USER_NAME,
                    upload_info.JRIA_CLOUD_PASSWORD,
                    file_path,
                    upload_info.JIRA_CLOUD_BASE_URL,
                    cloud_issue_key
                )

    @classmethod
    def upload_attach(cls, jira_usr_name, jira_pwd, file_path, jira_url, issue_key):
        # TODO: modify to PyCurl

        cmd = r'curl -D- -u {username}:{password} -X POST -H "X-Atlassian-Token: nocheck" ' \
              r'-F "file=@{file}" {jira_url}/rest/api/2/issue/{issue_key}/attachments'\
            .format(username=jira_usr_name,
                    password=jira_pwd,
                    file=file_path,
                    jira_url=jira_url,
                    issue_key=issue_key)

        logging.debug(cmd)
        subprocess.call(cmd, shell=True)
