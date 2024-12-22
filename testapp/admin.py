from testapp import app, db
from flask_admin import Admin, AdminIndexView, expose
from testapp.models import Grade, Lop, Student, User, UserRole, MonHoc, Teacher
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Field


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='Student Management', template_mode='bootstrap4', index_view=MyAdminIndexView())

class LopView(ModelView):
    form_columns = ['name', 'siso', 'grade_id']
    list_columns = ['name', 'siso', 'grade_id']

class TeacherView(ModelView):
    can_create = False
    list_columns = ['ho', 'ten', 'username', 'password', 'monhoc_id','user_role']

class GradeView(ModelView):
    column_list = ['name', 'lops']

class MonHocView(ModelView):
    column_list = ['name', 'teachers']
    form_columns = ['name']

class UserView(ModelView):
    form_columns = ['ho', 'ten', 'username', 'active','password','user_role']

admin.add_view(UserView(User, db.session, name='User'))
admin.add_view(TeacherView(Teacher, db.session, name='Giáo viên'))
admin.add_view(LopView(Lop, db.session, name='Lớp'))
admin.add_view(GradeView(Grade, db.session, name='Khối'))
admin.add_view(MonHocView(MonHoc, db.session, name='Môn học'))
