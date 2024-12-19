from testapp.models import *
from testapp import app

def load_grade():
    return Grade.query.all()


def load_class(grade_id=None):
    if grade_id:
        classes = Lop.query.filter_by(grade_id=grade_id).all()
    else:
        classes = Lop.query.all()
    return classes

def load_student():
    return Student.query.all()

def load_diem():
    return Diem.query.all()

def get_student_by_id(student_id):
    return Student.query.get(student_id)
