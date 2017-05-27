# coding: utf-8
import unittest
import os

from JiraServerToCloud.HelpTools import SrvExportedCsvReader, UploadAttachAgent


class testCsvReader(unittest.TestCase):

    def setUp(self):
        pass

    def test_en_csv_file(self):

        test_file = 'Cybersoft-Migration.csv'

        csv_reader = SrvExportedCsvReader(test_file)
        csv_reader.build_attach_name_info()

        for issue, info in csv_reader.issue_attach_info.iteritems():
            print issue
            print len(info.attach_info)
            info.display_all_attach_info()

        self.assertEquals(
            len(csv_reader.issue_attach_info.get('MIG-3').attach_info),
            1)

        self.assertIn(
            ('10100', 'jira-migration-drill-a.png'),
            csv_reader.issue_attach_info.get('MIG-3').attach_info)

        self.assertEquals(
            len(csv_reader.issue_attach_info.get('MIG-1').attach_info),
            3)

        self.assertIn(
            ('10101', 'jira-migration-drill-a.png'),
            csv_reader.issue_attach_info.get('MIG-1').attach_info)

        self.assertIn(
            ('10000', '[2016-09-11] 01_48_59.png'),
            csv_reader.issue_attach_info.get('MIG-1').attach_info)

        self.assertIn(
            ('10001', '[2015-10-24] 00_08_29.png'),
            csv_reader.issue_attach_info.get('MIG-1').attach_info)

        self.assertIsNone(csv_reader.issue_attach_info.get('MIG-2'))

    def test_tw_csv_file(self):

        test_file = 'Cybersoft-Migration_中文.csv'

        csv_reader = SrvExportedCsvReader(test_file)
        csv_reader.build_attach_name_info()

        for issue, info in csv_reader.issue_attach_info.iteritems():
            print issue
            print len(info.attach_info)
            info.display_all_attach_info()

        self.assertEquals(
            len(csv_reader.issue_attach_info.get('MIG-2').attach_info),
            2)

        self.assertIn(
            ('10201', '螢幕快照 2013-12-05 下午10.16.24.jpg'),
            csv_reader.issue_attach_info.get('MIG-2').attach_info)

    def test_rename_attach_agent(self):

        test_file = r'./data/exported.csv'
        csv_reader = SrvExportedCsvReader(test_file)
        csv_reader.build_attach_name_info()

        home_path = os.path.expanduser('~')

        upload_agent = UploadAttachAgent(
            csv_reader.issue_attach_info,
            'MIG',
            home_path + r'/Dropbox/Code/github/JiraMigrationTool/test/JiraServerToCloudTest/data/attachments/MIG/10000'
        )
        upload_agent.remove_all_thumbs()
        upload_agent.rename_all_files()
        upload_agent.upload_all_attachs('MAN')


if __name__ == '__main__':
    unittest.main()
