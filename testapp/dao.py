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

def load_diem_theo_mon_hoc(monhoc_id=None):
    if monhoc_id:
        diems = Diem.query.filter_by(monhoc_id=monhoc_id).all()
    else:
        pass
    return diems

def load_user():
    return User.query.all()

def get_student_by_id(student_id):
    return Student.query.get(student_id)
