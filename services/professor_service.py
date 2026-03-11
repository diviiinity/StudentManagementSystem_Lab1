from services.csv_handler import CSVHandler
from models.professor import Professor

PROF_FIELDS = ["Professor_id", "Professor_name", "Rank", "Course_id"]


def load_professors(prof_file):
    rows = CSVHandler.load_data(prof_file)
    return [Professor(r["Professor_id"], r["Professor_name"], r["Rank"], r["Course_id"]) for r in rows]


def save_professors(prof_file, professors):
    CSVHandler.save_data(prof_file, [p.to_dict() for p in professors], PROF_FIELDS)


def add_professor(prof_file, prof: Professor):
    professors = load_professors(prof_file)
    if any(p.professor_id == prof.professor_id for p in professors):
        return False
    professors.append(prof)
    save_professors(prof_file, professors)
    return True


def delete_professor(prof_file, professor_id: str):
    professors = load_professors(prof_file)
    new_professors = [p for p in professors if p.professor_id != professor_id]
    if len(new_professors) == len(professors):
        return False
    save_professors(prof_file, new_professors)
    return True


def update_professor(prof_file, professor_id: str, **updates):
    professors = load_professors(prof_file)
    for p in professors:
        if p.professor_id == professor_id:
            if "professor_name" in updates and updates["professor_name"] is not None:
                p.professor_name = updates["professor_name"]
            if "rank" in updates and updates["rank"] is not None:
                p.rank = updates["rank"]
            if "course_id" in updates and updates["course_id"] is not None:
                p.course_id = updates["course_id"]
            save_professors(prof_file, professors)
            return True
    return False