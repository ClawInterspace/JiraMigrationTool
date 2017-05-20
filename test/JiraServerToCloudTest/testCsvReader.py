import unittest

from JiraServerToCloud.ServerExportedCsv import Reader


class testCsvReader(unittest.TestCase):

    def setUp(self):
        self.test_file = 'Cybersoft-Migration.csv'

    def test_something(self):
        csv_reader = Reader(self.test_file)
        csv_reader.build_lookup_map()

if __name__ == '__main__':
    unittest.main()
