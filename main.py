from services.csv_handler import CSVHandler
from models.student import Student

STUDENT_FILE = "data/students.csv"

# Load students into a list (array structure)
def load_students():
    student_dicts = CSVHandler.load_data(STUDENT_FILE)
    students = []

    for s in student_dicts:
        student = Student(
            s["Email_address"],
            s["First_name"],
            s["Last_name"],
            s["Course_id"],
            s["Grade"],
            s["Marks"]
        )
        students.append(student)

    return students


def save_students(students):
    data = [student.to_dict() for student in students]
    fieldnames = ["Email_address", "First_name", "Last_name",
                  "Course_id", "Grade", "Marks"]
    CSVHandler.save_data(STUDENT_FILE, data, fieldnames)


def add_student():
    email = input("Enter Email: ")
    first = input("Enter First Name: ")
    last = input("Enter Last Name: ")
    course = input("Enter Course ID: ")
    grade = input("Enter Grade: ")
    marks = input("Enter Marks: ")

    students = load_students()

    # Check unique email
    for s in students:
        if s.email == email:
            print("Student with this email already exists!")
            return

    new_student = Student(email, first, last, course, grade, marks)
    students.append(new_student)

    save_students(students)
    print("Student added successfully!")


def display_students():
    students = load_students()

    if not students:
        print("No students found.")
        return

    for student in students:
        print(student)


def delete_student():
    email = input("Enter Email of student to delete: ").strip()

    students = load_students()
    original_count = len(students)

    # keep only students whose email doesn't match
    students = [s for s in students if s.email != email]

    if len(students) == original_count:
        print("No student found with that email.")
        return

    save_students(students)
    print("Student deleted successfully!")


def update_student():
    email = input("Enter Email of student to update: ").strip()
    students = load_students()

    for student in students:
        if student.email == email:
            print("Leave blank to keep current value.")

            new_first = input(f"First Name ({student.first_name}): ")
            new_last = input(f"Last Name ({student.last_name}): ")
            new_course = input(f"Course ID ({student.course_id}): ")
            new_grade = input(f"Grade ({student.grade}): ")
            new_marks = input(f"Marks ({student.marks}): ")

            if new_first:
                student.first_name = new_first
            if new_last:
                student.last_name = new_last
            if new_course:
                student.course_id = new_course
            if new_grade:
                student.grade = new_grade
            if new_marks:
                student.marks = int(new_marks)

            save_students(students)
            print("Student updated successfully!")
            return

    print("No student found with that email.")


import time

def search_student():
    email = input("Enter Email to search: ").strip()

    students = load_students()

    start_time = time.perf_counter()

    found_student = None
    for student in students:
        if student.email == email:
            found_student = student
            break

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    if found_student:
        print("Student Found:")
        print(found_student)
    else:
        print("Student not found.")

    print(f"Search Time: {elapsed_time:.6f} seconds")


def sort_students():
    students = load_students()

    if not students:
        print("No students to sort.")
        return

    print("\nSort By:")
    print("1. Marks Ascending")
    print("2. Marks Descending")
    print("3. Email Ascending")
    print("4. Email Descending")

    choice = input("Enter choice: ")

    import time
    start_time = time.perf_counter()

    if choice == "1":
        students.sort(key=lambda s: s.marks)
    elif choice == "2":
        students.sort(key=lambda s: s.marks, reverse=True)
    elif choice == "3":
        students.sort(key=lambda s: s.email)
    elif choice == "4":
        students.sort(key=lambda s: s.email, reverse=True)
    else:
        print("Invalid choice.")
        return

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print("\nSorted Students:")
    for student in students:
        print(student)

    print(f"\nSorting Time: {elapsed_time:.6f} seconds")


def main():
    while True:
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. Display Students")
        print("3. Delete Student")
        print("4. Update Student")
        print("5. Search Student")
        print("6. Sort Students")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            search_student()
        elif choice == "6":
            sort_students()
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()