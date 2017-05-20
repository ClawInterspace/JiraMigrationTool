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

    issue_fname_lookup_map = {}
    issueid_attachments_map = {}

    def __init__(self, file_path):
        """

        :param file_path:
        """
        self._file_path = file_path

    def build_lookup_map(self):

        with open(self._file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            fieldnames = remap(next(reader), 'Attachment')
            for row in reader:
                row = dict(zip(fieldnames, row))
                print row['Issue key'], \
                    row['Attachment1'], \
                    row['Attachment2'], \
                    row['Attachment3']