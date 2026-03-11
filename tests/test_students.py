import os
import unittest
import tempfile
import random
import string

from models.student import Student
from services.student_service import (
    STUDENT_FIELDS,
    load_students,
    save_students,
    add_student,
    delete_student,
    update_student,
    search_student,
    sort_students,
)
from services.csv_handler import CSVHandler


def random_email(i):
    return f"student{i}@test.edu"


def random_name(length=6):
    return "".join(random.choice(string.ascii_letters) for _ in range(length)).capitalize()


class TestStudents(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV for tests (doesn't touch real data/)
        self.temp_dir = tempfile.TemporaryDirectory()
        self.student_file = os.path.join(self.temp_dir.name, "students.csv")

        # Create 1000 students
        students = []
        for i in range(1000):
            students.append(
                Student(
                    random_email(i),
                    random_name(),
                    random_name(),
                    course_id=str(random.randint(100, 105)),
                    grade="A",
                    marks=random.randint(0, 100),
                )
            )

        # Save to temp CSV
        CSVHandler.save_data(self.student_file, [s.to_dict() for s in students], STUDENT_FIELDS)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_1000_students(self):
        students = load_students(self.student_file)
        self.assertEqual(len(students), 1000)

    def test_add_student(self):
        new_s = Student("new@student.edu", "New", "Student", "101", "B", 88)
        ok = add_student(self.student_file, new_s)
        self.assertTrue(ok)
        students = load_students(self.student_file)
        self.assertEqual(len(students), 1001)

    def test_add_duplicate_student_fails(self):
        dup = Student(random_email(1), "Dup", "User", "101", "C", 50)
        ok = add_student(self.student_file, dup)
        self.assertFalse(ok)

    def test_delete_student(self):
        ok = delete_student(self.student_file, random_email(10))
        self.assertTrue(ok)
        students = load_students(self.student_file)
        self.assertEqual(len(students), 999)

    def test_update_student(self):
        target = random_email(20)
        ok = update_student(self.student_file, target, first_name="Updated", marks=99)
        self.assertTrue(ok)

        found, _ = search_student(self.student_file, target)
        self.assertIsNotNone(found)
        self.assertEqual(found.first_name, "Updated")
        self.assertEqual(found.marks, 99)

    def test_search_timing(self):
        target = random_email(500)
        found, elapsed = search_student(self.student_file, target)
        self.assertIsNotNone(found)
        self.assertGreaterEqual(elapsed, 0.0)

    def test_sort_timing_and_order_marks(self):
        students, elapsed = sort_students(self.student_file, "marks_asc")
        self.assertGreaterEqual(elapsed, 0.0)

        # verify sorted order
        marks = [s.marks for s in students]
        self.assertEqual(marks, sorted(marks))

    def test_sort_timing_and_order_email_desc(self):
        students, elapsed = sort_students(self.student_file, "email_desc")
        self.assertGreaterEqual(elapsed, 0.0)

        emails = [s.email for s in students]
        self.assertEqual(emails, sorted(emails, reverse=True))


if __name__ == "__main__":
    unittest.main()