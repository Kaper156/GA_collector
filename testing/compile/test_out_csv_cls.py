import os
import unittest


# TODO Rewrite all of this
class TestCompile(unittest.TestCase):
    def setUp(self):
        # Load settings
        os.chdir('../../')  # TODO fix that (can walk too up)

        # Set folder paths
        self.result_folder = os.path.join(os.getcwd(), 'testing', 'compile', 'results')
        self.expected_folder = os.path.join(os.getcwd(), 'testing', 'compile', 'expected')
        self.sources_folder = os.path.join("testing", "sources", "csv_by_week")

        # Set up cls
        self.csv_out = OutCsv(self.sources_folder, )
        print(f"Set up cls to folder: {self.result_folder}")
        print(f"Loaded {len(FILTERS)} filters")

        # Set expected file paths
        self.exp_avg_f = os.path.join(self.expected_folder, 'avg_week.csv')
        self.exp_merge_f = os.path.join(self.expected_folder, 'merge_week.csv')
        self.exp_li_f = os.path.join(self.expected_folder, 'li_week.csv')

        # Set result file paths
        self.res_avg_f = os.path.join(self.result_folder, 'avg_week.csv')
        self.res_merge_f = os.path.join(self.result_folder, 'merge_week.csv')
        self.res_li_f = os.path.join(self.result_folder, 'li_week.csv')

    def read_file(self, file_path):
        with open(file_path, 'rt', encoding='utf-8') as f:
            return f.read()

    def test_avg(self):
        expected = self.read_file(self.exp_avg_f)

        # Write csv
        self.csv_out.avg_csv(self.res_avg_f)
        result = self.read_file(self.res_avg_f)

        self.assertEqual(expected, result)

    def test_merge(self):
        expected = self.read_file(self.exp_merge_f)

        # Write csv
        self.csv_out.merge_csv(self.res_merge_f)
        result = self.read_file(self.res_merge_f)

        self.assertEqual(expected, result)

    def test_line_items(self):
        expected = self.read_file(self.exp_li_f)

        # Write csv
        self.csv_out.write_distinct_line_items(self.res_li_f)
        result = self.read_file(self.res_li_f)

        self.assertEqual(expected, result)


class ExecuteCompile(TestCompile):

    def test_merge(self):
        # Write csv
        self.csv_out.merge_csv(self.res_merge_f)
        result = self.read_file(self.res_merge_f)

    def test_avg(self):
        self.csv_out.avg_csv(self.res_avg_f)
        result = self.read_file(self.res_avg_f)

    def test_line_items(self):
        # Write csv
        self.csv_out.write_distinct_line_items(self.res_li_f)
        result = self.read_file(self.res_li_f)
