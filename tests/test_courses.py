import os
import unittest
import tempfile

from models.course import Course
from services.course_service import (
    COURSE_FIELDS,
    load_courses,
    add_course,
    delete_course,
    update_course,
)
from services.csv_handler import CSVHandler


class TestCourses(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.course_file = os.path.join(self.temp_dir.name, "courses.csv")

        # seed with a couple courses
        courses = [
            Course("C101", "Intro to CS", "Basics"),
            Course("C102", "Data Structures", "Trees, lists, sorting"),
        ]
        CSVHandler.save_data(self.course_file, [c.to_dict() for c in courses], COURSE_FIELDS)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_courses(self):
        courses = load_courses(self.course_file)
        self.assertEqual(len(courses), 2)

    def test_add_course(self):
        ok = add_course(self.course_file, Course("C103", "Algorithms", "Big-O"))
        self.assertTrue(ok)
        self.assertEqual(len(load_courses(self.course_file)), 3)

    def test_add_duplicate_course_fails(self):
        ok = add_course(self.course_file, Course("C101", "Dup", "Dup"))
        self.assertFalse(ok)

    def test_update_course(self):
        ok = update_course(self.course_file, "C102", course_name="DSA", description="Updated")
        self.assertTrue(ok)
        courses = load_courses(self.course_file)
        updated = [c for c in courses if c.course_id == "C102"][0]
        self.assertEqual(updated.course_name, "DSA")
        self.assertEqual(updated.description, "Updated")

    def test_delete_course(self):
        ok = delete_course(self.course_file, "C101")
        self.assertTrue(ok)
        self.assertEqual(len(load_courses(self.course_file)), 1)


if __name__ == "__main__":
    unittest.main()