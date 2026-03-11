from services.csv_handler import CSVHandler
from models.student import Student
from models.course import Course
from models.professor import Professor
from encdyc import TextSecurity



STUDENT_FILE = "data/students.csv"
COURSE_FILE = "data/courses.csv"
PROFESSOR_FILE = "data/professors.csv"
LOGIN_FILE = "data/login.csv"
SHIFT_VALUE = 4

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


def course_statistics():
    import statistics

    course_id = input("Enter Course ID: ").strip()
    students = load_students()

    course_students = [s for s in students if s.course_id == course_id]

    if not course_students:
        print("No students found for this course.")
        return

    marks_list = [s.marks for s in course_students]

    average = sum(marks_list) / len(marks_list)
    median = statistics.median(marks_list)

    print(f"\nCourse ID: {course_id}")
    print(f"Number of Students: {len(course_students)}")
    print(f"Average Marks: {average:.2f}")
    print(f"Median Marks: {median:.2f}")


def course_report():
    course_id = input("Enter Course ID for report: ").strip()
    students = load_students()

    course_students = [s for s in students if s.course_id == course_id]

    if not course_students:
        print("No students found for this course.")
        return

    print("\n--- Course Grade Report ---")
    print(f"Course ID: {course_id}")
    print("-" * 50)

    for student in course_students:
        print(f"{student.first_name} {student.last_name} "
              f"| Email: {student.email} "
              f"| Marks: {student.marks} "
              f"| Grade: {student.grade}")
        

# Course

def load_courses():
    course_dicts = CSVHandler.load_data(COURSE_FILE)
    courses = []

    for c in course_dicts:
        courses.append(
            Course(
                c["Course_id"],
                c["Course_name"],
                c["Description"]
            )
        )

    return courses


def save_courses(courses):
    data = [course.to_dict() for course in courses]
    fieldnames = ["Course_id", "Course_name", "Description"]
    CSVHandler.save_data(COURSE_FILE, data, fieldnames)



#course CRUD Functions:

def add_course():
    course_id = input("Enter Course ID: ").strip()
    name = input("Enter Course Name: ").strip()
    description = input("Enter Description: ").strip()

    courses = load_courses()

    for c in courses:
        if c.course_id == course_id:
            print("Course with this ID already exists!")
            return

    courses.append(Course(course_id, name, description))
    save_courses(courses)
    print("Course added successfully!")


def display_courses():
    courses = load_courses()

    if not courses:
        print("No courses found.")
        return

    print("\n--- Courses ---")
    for c in courses:
        print(c)


def delete_course():
    course_id = input("Enter Course ID to delete: ").strip()
    courses = load_courses()
    original_count = len(courses)

    courses = [c for c in courses if c.course_id != course_id]

    if len(courses) == original_count:
        print("No course found with that ID.")
        return

    save_courses(courses)
    print("Course deleted successfully!")


def update_course():
    course_id = input("Enter Course ID to update: ").strip()
    courses = load_courses()

    for c in courses:
        if c.course_id == course_id:
            print("Leave blank to keep current value.")

            new_name = input(f"Course Name ({c.course_name}): ").strip()
            new_desc = input(f"Description ({c.description}): ").strip()

            if new_name:
                c.course_name = new_name
            if new_desc:
                c.description = new_desc

            save_courses(courses)
            print("Course updated successfully!")
            return

    print("No course found with that ID.")

# Professor

def load_professors():
    professor_dicts = CSVHandler.load_data(PROFESSOR_FILE)
    professors = []

    for p in professor_dicts:
        professors.append(
            Professor(
                p["Professor_id"],
                p["Professor_name"],
                p["Rank"],
                p["Course_id"]
            )
        )

    return professors


def save_professors(professors):
    data = [p.to_dict() for p in professors]
    fieldnames = ["Professor_id", "Professor_name", "Rank", "Course_id"]
    CSVHandler.save_data(PROFESSOR_FILE, data, fieldnames)

# Professor CRUD Functions

def add_professor():
    prof_id = input("Enter Professor ID: ").strip()
    name = input("Enter Professor Name: ").strip()
    rank = input("Enter Rank: ").strip()
    course_id = input("Enter Course ID: ").strip()

    professors = load_professors()

    for p in professors:
        if p.professor_id == prof_id:
            print("Professor with this ID already exists!")
            return

    professors.append(Professor(prof_id, name, rank, course_id))
    save_professors(professors)
    print("Professor added successfully!")


def display_professors():
    professors = load_professors()

    if not professors:
        print("No professors found.")
        return

    print("\n--- Professors ---")
    for p in professors:
        print(p)


def delete_professor():
    prof_id = input("Enter Professor ID to delete: ").strip()
    professors = load_professors()
    original_count = len(professors)

    professors = [p for p in professors if p.professor_id != prof_id]

    if len(professors) == original_count:
        print("No professor found with that ID.")
        return

    save_professors(professors)
    print("Professor deleted successfully!")


def update_professor():
    prof_id = input("Enter Professor ID to update: ").strip()
    professors = load_professors()

    for p in professors:
        if p.professor_id == prof_id:
            print("Leave blank to keep current value.")

            new_name = input(f"Name ({p.professor_name}): ").strip()
            new_rank = input(f"Rank ({p.rank}): ").strip()
            new_course = input(f"Course ID ({p.course_id}): ").strip()

            if new_name:
                p.professor_name = new_name
            if new_rank:
                p.rank = new_rank
            if new_course:
                p.course_id = new_course

            save_professors(professors)
            print("Professor updated successfully!")
            return

    print("No professor found with that ID.")

def professor_report():
    prof_id = input("Enter Professor ID: ").strip()

    professors = load_professors()
    students = load_students()

    for p in professors:
        if p.professor_id == prof_id:
            print("\n--- Professor Report ---")
            print(p)
            print("\nStudents in their course:")
            print("-" * 50)

            course_students = [s for s in students if s.course_id == p.course_id]

            if not course_students:
                print("No students found for this professor's course.")
                return

            for s in course_students:
                print(f"{s.first_name} {s.last_name} "
                      f"| Marks: {s.marks} "
                      f"| Grade: {s.grade}")
            return

    print("Professor not found.")


#Login
def load_users():
    return CSVHandler.load_data(LOGIN_FILE)


def save_users(users):
    fieldnames = ["User_id", "Password", "Role"]
    CSVHandler.save_data(LOGIN_FILE, users, fieldnames)


# Register

def register_user():
    user_id = input("Enter Email (User ID): ").strip()
    password = input("Enter Password: ").strip()
    role = input("Enter Role (admin/student/professor): ").strip()

    users = load_users()

    for u in users:
        if u["User_id"] == user_id:
            print("User already exists!")
            return

    cipher = TextSecurity(SHIFT_VALUE)
    encrypted_password = cipher.encrypt(password)

    users.append({
        "User_id": user_id,
        "Password": encrypted_password,
        "Role": role
    })

    save_users(users)
    print("User registered successfully!")


# Login User

def login_user():
    user_id = input("Enter Email: ").strip()
    password = input("Enter Password: ").strip()

    users = load_users()
    cipher = TextSecurity(SHIFT_VALUE)

    for u in users:
        if u["User_id"] == user_id:
            decrypted_password = cipher.decrypt(u["Password"])

            if decrypted_password == password:
                print("Login successful!")
                return u["Role"]

            else:
                print("Incorrect password.")
                return None

    print("User not found.")
    return None

#Password Change

def change_password():
    user_id = input("Enter Email: ").strip()
    old_password = input("Enter Current Password: ").strip()

    users = load_users()
    cipher = TextSecurity(SHIFT_VALUE)

    for u in users:
        if u["User_id"] == user_id:
            decrypted_password = cipher.decrypt(u["Password"])

            if decrypted_password != old_password:
                print("Incorrect current password.")
                return

            new_password = input("Enter New Password: ").strip()
            u["Password"] = cipher.encrypt(new_password)

            save_users(users)
            print("Password updated successfully!")
            return

    print("User not found.")



#Submenu for Login

def login_menu():
    while True:
        print("\n--- Login System ---")
        print("1. Register")
        print("2. Login")
        print("3. Change Password")
        print("4. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            role = login_user()
            if role:
                print(f"Logged in as {role}")
        elif choice == "3":
            change_password()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

#Submenu for professor

def professor_menu():
    while True:
        print("\n--- Professor Management ---")
        print("1. Add Professor")
        print("2. Display Professors")
        print("3. Delete Professor")
        print("4. Update Professor")
        print("5. Professor Report")
        print("6. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_professor()
        elif choice == "2":
            display_professors()
        elif choice == "3":
            delete_professor()
        elif choice == "4":
            update_professor()
        elif choice == "5":
            professor_report()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")



#Submenu for course

def course_menu():
    while True:
        print("\n--- Course Management ---")
        print("1. Add Course")
        print("2. Display Courses")
        print("3. Delete Course")
        print("4. Update Course")
        print("5. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_course()
        elif choice == "2":
            display_courses()
        elif choice == "3":
            delete_course()
        elif choice == "4":
            update_course()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

#MAIN

def main():
    while True:
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. Display Students")
        print("3. Delete Student")
        print("4. Update Student")
        print("5. Search Student")
        print("6. Sort Students")
        print("7. Course Statistics")
        print("8. Course Grade Report")
        print("9. Course Management")
        print("10. Professor Management")
        print("11. Login System")
        print("12. Exit")
        

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
            course_statistics()
        elif choice == "8":
            course_report()
        elif choice == "9":
            course_menu()
        elif choice == "10":
            professor_menu()
        elif choice == "11":
            login_menu()
        elif choice == "12":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
