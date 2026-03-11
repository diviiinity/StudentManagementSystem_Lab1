from services.csv_handler import CSVHandler
from models.course import Course

COURSE_FIELDS = ["Course_id", "Course_name", "Description"]


def load_courses(course_file):
    rows = CSVHandler.load_data(course_file)
    return [Course(r["Course_id"], r["Course_name"], r["Description"]) for r in rows]


def save_courses(course_file, courses):
    CSVHandler.save_data(course_file, [c.to_dict() for c in courses], COURSE_FIELDS)


def add_course(course_file, course: Course):
    courses = load_courses(course_file)
    if any(c.course_id == course.course_id for c in courses):
        return False
    courses.append(course)
    save_courses(course_file, courses)
    return True


def delete_course(course_file, course_id: str):
    courses = load_courses(course_file)
    new_courses = [c for c in courses if c.course_id != course_id]
    if len(new_courses) == len(courses):
        return False
    save_courses(course_file, new_courses)
    return True


def update_course(course_file, course_id: str, **updates):
    courses = load_courses(course_file)
    for c in courses:
        if c.course_id == course_id:
            if "course_name" in updates and updates["course_name"] is not None:
                c.course_name = updates["course_name"]
            if "description" in updates and updates["description"] is not None:
                c.description = updates["description"]
            save_courses(course_file, courses)
            return True
    return False

