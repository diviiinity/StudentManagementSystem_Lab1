import os
import unittest
import tempfile

from models.professor import Professor
from services.professor_service import (
    PROF_FIELDS,
    load_professors,
    add_professor,
    delete_professor,
    update_professor,
)
from services.csv_handler import CSVHandler


class TestProfessors(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.prof_file = os.path.join(self.temp_dir.name, "professors.csv")

        profs = [
            Professor("P1", "Dr. Smith", "Associate", "C101"),
            Professor("P2", "Dr. Lee", "Assistant", "C102"),
        ]
        CSVHandler.save_data(self.prof_file, [p.to_dict() for p in profs], PROF_FIELDS)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_professors(self):
        profs = load_professors(self.prof_file)
        self.assertEqual(len(profs), 2)

    def test_add_professor(self):
        ok = add_professor(self.prof_file, Professor("P3", "Dr. Kim", "Full", "C101"))
        self.assertTrue(ok)
        self.assertEqual(len(load_professors(self.prof_file)), 3)

    def test_add_duplicate_professor_fails(self):
        ok = add_professor(self.prof_file, Professor("P1", "Dup", "Dup", "C101"))
        self.assertFalse(ok)

    def test_update_professor(self):
        ok = update_professor(self.prof_file, "P2", professor_name="Dr. Lee Updated", rank="Associate")
        self.assertTrue(ok)
        profs = load_professors(self.prof_file)
        updated = [p for p in profs if p.professor_id == "P2"][0]
        self.assertEqual(updated.professor_name, "Dr. Lee Updated")
        self.assertEqual(updated.rank, "Associate")

    def test_delete_professor(self):
        ok = delete_professor(self.prof_file, "P1")
        self.assertTrue(ok)
        self.assertEqual(len(load_professors(self.prof_file)), 1)


if __name__ == "__main__":
    unittest.main()