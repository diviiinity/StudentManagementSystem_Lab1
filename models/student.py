class Student:
    def __init__(self, email, first_name, last_name, course_id, grade, marks):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.course_id = course_id
        self.grade = grade
        self.marks = int(marks)

    def to_dict(self):
        """Convert student object to dictionary for CSV storage"""
        return {
            "Email_address": self.email,
            "First_name": self.first_name,
            "Last_name": self.last_name,
            "Course_id": self.course_id,
            "Grade": self.grade,
            "Marks": self.marks
        }

    def __str__(self):
        return (f"Email: {self.email}, "
                f"Name: {self.first_name} {self.last_name}, "
                f"Course: {self.course_id}, "
                f"Grade: {self.grade}, "
                f"Marks: {self.marks}")
    
    