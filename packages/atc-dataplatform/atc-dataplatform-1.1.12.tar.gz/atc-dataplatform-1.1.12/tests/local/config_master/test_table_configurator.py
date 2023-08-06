import unittest

from atc.config_master import TableConfigurator

from . import tables1, tables2, tables3, tables4


class TestTableConfigurator(unittest.TestCase):
    def test_01_import_config(self):
        tc = TableConfigurator()
        tc.add_resource_path(tables1)
        tc.reset(debug=True)
        self.assertRegex(tc.table_name("MyFirst"), "first__.*")
        self.assertRegex(tc.table_name("MyAlias"), "first__.*")
        self.assertRegex(tc.table_name("MyForked"), "another")

        tc.reset(debug=False)
        self.assertRegex(tc.table_name("MyFirst"), "first")
        self.assertRegex(tc.table_name("MyAlias"), "first")
        self.assertRegex(tc.table_name("MyForked"), "first")

    def test_02_details(self):
        tc = TableConfigurator()

        tc.reset(debug=True)
        details = tc.get_all_details()
        self.assertRegex(details["MyFirst_path"], "/tmp/my/first__.*")

        tc.reset(debug=False)
        details = tc.get_all_details()
        self.assertRegex(details["MyFirst_path"], "/mnt/my/first")

    def test_03_json(self):
        tc = TableConfigurator()

        with self.assertRaises(KeyError):
            tc.add_resource_path(tables2)

        tc.set_extra(ENV="dev")
        tc.add_resource_path(tables2)
        tc.reset(debug=True)
        self.assertRegex(tc.table_name("MyThird"), "first__.*")

        self.assertRegex(
            tc.get_all_details()["MyFourth_path"], "/tmp/dev/path/to/delta"
        )

    def test_04_recursing(self):
        tc = TableConfigurator()
        tc.set_prod()
        self.assertEqual(tc.table_path("MyRecursing"), "/mnt/tables/recursing")

    def test_05_test_self_recursion_detection(self):
        tc = TableConfigurator()
        tc.set_prod()
        with self.assertRaises(ValueError):
            tc.add_resource_path(tables3)

    def test_06_freestyle(self):
        tc = TableConfigurator()
        tc.set_prod()
        tc.add_resource_path(tables4)
        details = tc.get_all_details()
        self.assertTrue("MyFreeTable_eggs", details)
        self.assertEqual(tc.table_property("MyFreeTable", "bacon"), "")
