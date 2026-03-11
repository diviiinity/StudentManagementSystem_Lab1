class Professor:
    def __init__(self, professor_id, professor_name, rank, course_id):
        self.professor_id = professor_id
        self.professor_name = professor_name
        self.rank = rank
        self.course_id = course_id

    def to_dict(self):
        return {
            "Professor_id": self.professor_id,
            "Professor_name": self.professor_name,
            "Rank": self.rank,
            "Course_id": self.course_id
        }

    def __str__(self):
        return (f"Professor ID: {self.professor_id} | "
                f"Name: {self.professor_name} | "
                f"Rank: {self.rank} | "
                f"Course ID: {self.course_id}")