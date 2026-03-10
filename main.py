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


def main():
    while True:
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. Display Students")
        print("3. Delete Student")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()