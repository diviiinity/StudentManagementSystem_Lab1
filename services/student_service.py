import time
from services.csv_handler import CSVHandler
from models.student import Student

STUDENT_FIELDS = ["Email_address", "First_name", "Last_name", "Course_id", "Grade", "Marks"]


def load_students(student_file):
    rows = CSVHandler.load_data(student_file)
    students = []
    for r in rows:
        students.append(
            Student(
                r["Email_address"],
                r["First_name"],
                r["Last_name"],
                r["Course_id"],
                r["Grade"],
                r["Marks"],
            )
        )
    return students


def save_students(student_file, students):
    CSVHandler.save_data(student_file, [s.to_dict() for s in students], STUDENT_FIELDS)


def add_student(student_file, student: Student):
    students = load_students(student_file)
    if any(s.email == student.email for s in students):
        return False
    students.append(student)
    save_students(student_file, students)
    return True


def delete_student(student_file, email: str):
    students = load_students(student_file)
    new_students = [s for s in students if s.email != email]
    if len(new_students) == len(students):
        return False
    save_students(student_file, new_students)
    return True


def update_student(student_file, email: str, **updates):
    students = load_students(student_file)
    for s in students:
        if s.email == email:
            if "first_name" in updates and updates["first_name"] is not None:
                s.first_name = updates["first_name"]
            if "last_name" in updates and updates["last_name"] is not None:
                s.last_name = updates["last_name"]
            if "course_id" in updates and updates["course_id"] is not None:
                s.course_id = updates["course_id"]
            if "grade" in updates and updates["grade"] is not None:
                s.grade = updates["grade"]
            if "marks" in updates and updates["marks"] is not None:
                s.marks = int(updates["marks"])
            save_students(student_file, students)
            return True
    return False


def search_student(student_file, email: str):
    students = load_students(student_file)
    start = time.perf_counter()
    found = None
    for s in students:
        if s.email == email:
            found = s
            break
    elapsed = time.perf_counter() - start
    return found, elapsed


def sort_students(student_file, mode: str):
    """
    mode:
      marks_asc, marks_desc, email_asc, email_desc
    """
    students = load_students(student_file)
    start = time.perf_counter()

    if mode == "marks_asc":
        students.sort(key=lambda s: s.marks)
    elif mode == "marks_desc":
        students.sort(key=lambda s: s.marks, reverse=True)
    elif mode == "email_asc":
        students.sort(key=lambda s: s.email)
    elif mode == "email_desc":
        students.sort(key=lambda s: s.email, reverse=True)
    else:
        raise ValueError("Invalid sort mode")

    elapsed = time.perf_counter() - start
    return students, elapsed