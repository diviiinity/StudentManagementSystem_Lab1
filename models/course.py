class Course:
    def __init__(self, course_id, course_name, description):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description

    def to_dict(self):
        return {
            "Course_id": self.course_id,
            "Course_name": self.course_name,
            "Description": self.description
        }

    def __str__(self):
        return f"Course ID: {self.course_id} | Name: {self.course_name} | Description: {self.description}"