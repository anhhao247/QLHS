from testapp.models import *
from testapp import app

def load_grade():
    return Grade.query.all()

def load_class(grade_id=None, kw=None):
    classes = Lop.query.all()
    if grade_id:
        classes = classes.filter(Lop.grade_id.__eq__(grade_id))

    if kw:
        classes = classes.filter(Lop.name.contains(kw))
    return classes

def load_student():
    return Student.query.all()

def get_student_by_id(student_id):
    return Student.query.get(student_id)
