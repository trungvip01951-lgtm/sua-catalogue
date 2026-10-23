"""Kiểm gán mã việc bằng dữ liệu gốc; chỉ đọc, không sửa catalogue."""
import json
from pathlib import Path
import unicodedata
import unittest
from refresh_index import tasks_for_file

ROOT = Path(__file__).resolve().parents[1]
TASKS = json.loads((ROOT/'vendor/catfix_original/GOI_SUA_CATALOGUE_CHATGPT/tasks/tasks.json').read_text(encoding='utf8'))


class FileTaskScopeTests(unittest.TestCase):
    def test_sa_does_not_inherit_redpump_logo_rule(self):
        groups, ids = tasks_for_file(TASKS, 'Giếng/Perotac bơm giếng SA_compressed (bản mới).pdf')
        self.assertEqual(groups, ['G04'])
        self.assertIn(35, ids)
        self.assertIn(132, ids)
        self.assertNotIn(162, ids)

    def test_redpump_gets_its_own_logo_and_shared_tasks_once(self):
        _, ids = tasks_for_file(TASKS, 'Giếng/Redpump gieng SL_compressed (bản mới).pdf')
        self.assertIn(162, ids)
        self.assertIn(132, ids)
        self.assertNotIn(35, ids)
        self.assertEqual(ids.count(132), 1)

    def test_two_excel_files_do_not_inherit_each_other_tasks(self):
        _, dwo = tasks_for_file(TASKS, 'Trục ngang/Catalogue DWO (bản mới).xlsx')
        _, perotac = tasks_for_file(TASKS, 'Nước thải/Catalogue perotac (bản mới).xlsx')
        self.assertIn(123, dwo)
        self.assertNotIn(66, dwo)
        self.assertIn(66, perotac)
        self.assertNotIn(123, perotac)

    def test_vietnamese_nfd_file_name_matches_same_authority(self):
        name = 'Giếng/Perotac bơm giếng SA_compressed (bản mới).pdf'
        self.assertEqual(tasks_for_file(TASKS, name), tasks_for_file(TASKS, unicodedata.normalize('NFD', name)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
