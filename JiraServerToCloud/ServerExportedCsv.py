# coding: utf-8
import logging
import csv
from itertools import count

_logger = logging.getLogger(__name__)


def remap(fieldnames, duplicated_field_name):
    price_count = count(1)
    return [duplicated_field_name + '{}'.format(next(price_count))
            if f.startswith(duplicated_field_name) else f
            for f in fieldnames]


class Reader(object):

    issue_attach_info = {}
    # {old_issue_key: IssueAttachmentMigrationInfo}

    issueid_attachments_map = {}
    # {filepath: (old_filename, new_filename, old_issue_key)}

    def __init__(self, file_path):
        """

        :param file_path:
        """
        self.issue_attach_info = {}
        self.issueid_attachments_map = {}

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

                _logger.debug(row[fn_issue_key])

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

        except Exception as e:
            raise Exception('cell value format error: "%s"' % cell_value)

        return file_id, file_name


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
