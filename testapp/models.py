from xmlrpc.client import DateTime

from sqlalchemy import Column, Integer, Float, String, Boolean, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from testapp import app, db
from datetime import datetime
from flask_login import UserMixin
import hashlib
import enum

# class Category(db.Model):
#     __tablename__ = 'category'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     products = relationship('Product', backref='category', lazy=True)
#
# class Product(db.Model):
#     __tablename__ = 'product'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     price = Column(Float, default=0)
#     # created_date = Column(DateTime, default=datetime.now())
#     category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
#     tags = relationship('Tag', secondary='product_tag', lazy='subquery',
#                         backref=backref('products', lazy=True))
#
#
# class Tag(db.Model):
#     __tablename__ = 'tag'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#
# product_tag = db.Table('product_tag',
#                        Column('product_id', Integer, ForeignKey(Product.id), primary_key=True),
#                        Column('tag_id', Integer, ForeignKey(Tag.id), primary_key=True))

# demo3----------------------------------------------------------------------------------------------------------------------------


# class Grade(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     classes = relationship('Class', backref='grade', lazy=True)
#
# class Class(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     si_so = Column(Integer, nullable=False)
#     grade_id = Column(Integer, ForeignKey(Grade.id), nullable=False)
#     students = relationship('Student', secondary='student_class', lazy='subquery',
#                             backref=backref('classes', lazy=True))
#
# class Student(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#
#
# student_class = db.Table('student_class',
#                          Column('student_id', Integer, ForeignKey(Student.id), primary_key=True),
#                          Column('class_id', Integer, ForeignKey(Class.id), primary_key=True))


# demo4-----------------------------------------------------------------------------------------------------------------------------
# class student_class(db.Model):
#     student_id = Column(ForeignKey('student.id'), primary_key=True)
#     class_id = Column(ForeignKey('class.id'), primary_key=True)
#     mark = Column(Float, default=0)
#
#
# class Class(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     si_so = Column(Integer, nullable=False)
#     students = relationship('student_class', backref='class')
#
# class Student(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#     classes = relationship('student_class', backref='student')

# DemoUser --------------------------------------------------------------------------------------------------------------------------------------
class UserRole(enum.Enum):
    ADMIN = 1
    STAFF = 2
    TEACHER = 3

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole, nullable=False))

class Admin(User):
    __tablename__ = 'admin'
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    ho = Column(String(50))
    ten = Column(String(50))
    permissions = Column(String(255))

class Staff(User):
    __tablename__ = 'staff'
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    ho = Column(String(50))
    ten = Column(String(50))

class Teacher(User):
    __tablename__ = 'teacher'
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    ho = Column(String(50))
    ten = Column(String(50))
    monhoc_id = Column(Integer, ForeignKey('monhoc.id'), nullable=False)

class MonHoc(db.Model):
    __tablename__ = 'monhoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    teachers = relationship('Teacher', backref='monhoc', lazy=True)
    diems = relationship('Diem', backref='monhoc', lazy=True)

class Diem(db.Model):
    __tablename__ = 'diem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum('15p', '45p', 'ck'), nullable=False)
    value = Column(Float, nullable=False)
    monhoc_id = Column(Integer, ForeignKey('monhoc.id'), nullable=False)
    hocky_id = Column(Integer, ForeignKey('hocky.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)

class HocKy(db.Model):
    __tablename__ = 'hocky'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    diems = relationship('Diem', backref='hocky', lazy=True)

class Student(db.Model):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho = Column(String(50), nullable=False)
    ten = Column(String(50), nullable=False)
    sex = Column(Enum('Nam', 'Nữ'), nullable=False)
    DoB = Column(DateTime, nullable=False)
    address = Column(String(100), nullable=False)
    sdt = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    diems = relationship('Diem', backref='student', lazy=True)


class Lop(db.Model):
    __tablename__ = 'lop'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    grade_id = Column(Integer, ForeignKey('grade.id'), nullable=False)
    students = relationship('Student', secondary='lop_student', lazy='subquery',
                               backref=backref('lops', lazy=True))

class Grade(db.Model):
    __tablename__ = 'grade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    lops = relationship('Lop', backref='grade', lazy=True)

lop_student = db.Table('lop_student',
                       Column('lop_id', Integer,ForeignKey('lop.id'), primary_key=True),
                       Column('student_id', Integer,ForeignKey('student.id'), primary_key=True))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()