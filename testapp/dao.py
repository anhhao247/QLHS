from testapp.models import *
from testapp import app

# load khoi
def load_grade():
    return Grade.query.all()

# load lop
def load_class(grade_id=None):
    if grade_id:
        classes = Lop.query.filter_by(grade_id=grade_id).all()
    else:
        classes = Lop.query.all()
    return classes

# load monhoc
def load_monhoc(grade_id=None):
    return  MonHoc.query.all()


def them_monhoc(name):
    if MonHoc.query.filter_by(name=name).first():
        raise ValueError("Môn học đã tồn tại!")
    new_monhoc = MonHoc(name=name)
    db.session.add(new_monhoc)
    db.session.commit()


def sua_monhoc(id, name):
    # Kiểm tra nếu môn học mới có tên giống với môn học khác
    if MonHoc.query.filter_by(name=name).first():
        raise ValueError("Môn học đã tồn tại!")

    monhoc = MonHoc.query.get(id)
    if monhoc:
        monhoc.name = name
        db.session.commit()
        return True
    return False


def xoa_monhoc(id):
    monhoc = MonHoc.query.get(id)
    if not monhoc:
        return False
    # Kiểm tra nếu môn học liên kết với dữ liệu khác
    if Diem.query.filter_by(monhoc_id=id).first():
        raise ValueError("Không thể xóa môn học vì có dữ liệu liên quan.")
    db.session.delete(monhoc)
    db.session.commit()
    return True


# load hoc sinh
def load_student():
    return Student.query.all()

# load diem theo mon
def load_diem_theo_mon_hoc(monhoc_id=None):
    if monhoc_id:
        diems = Diem.query.filter_by(monhoc_id=monhoc_id).all()
    else:
        pass
    return diems

# load user
def load_user():
    return User.query.all()

# load giaovien
def load_teacher():
    return Teacher.query.all()

def get_student_by_id(student_id):
    return Student.query.get(student_id)
