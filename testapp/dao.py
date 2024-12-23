from functools import wraps

from flask import session, redirect, url_for
from sqlalchemy.exc import NoResultFound

from testapp.models import *
from testapp import app
from werkzeug.security import check_password_hash


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
  return Diem.query.all()
# load user
def load_user():
    return User.query.all()

# load giaovien
def load_teacher():
    return Teacher.query.all()

def get_student_by_id(student_id):
    return Student.query.get(student_id)

# Load học kỳ
def load_hoc_ky():
    return HocKy.query.all()

def check_password(Stored_password, entered_password):
    return check_password_hash(Stored_password, entered_password)


def get_user_by_username(username):
    # Truy vấn cơ sở dữ liệu để lấy thông tin người dùng
    # Ví dụ, trả về một đối tượng người dùng có chứa mật khẩu đã băm
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        return {"id": user.id, "username": user.username, "password": user.password}
    return None

def get_user_by_id(user_id):
    # Lấy thông tin người dùng từ cơ sở dữ liệu dựa trên user_id
    user = User.query.get(user_id)  # Truy vấn cơ sở dữ liệu với user_id
    if user:
        return {
            "id": user.id,
            "name": user.name,
            "job": user.user_role
        }
    return None  # Nếu không tìm thấy người dùng, trả về None
