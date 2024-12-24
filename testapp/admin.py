from urllib.parse import uses_relative

from testapp import app, db
from flask_admin import Admin, AdminIndexView, expose
from testapp.models import Grade, Lop, Student, User, UserRole, MonHoc, Teacher
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Field
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='Student Management', template_mode='bootstrap4', index_view=MyAdminIndexView())

class LopView(ModelView):
    form_columns = ['name', 'siso', 'grade_id']
    list_columns = ['name', 'siso', 'grade_id']

class TeacherView(ModelView):
    can_create = True
    list_columns = ['ho', 'ten', 'username', 'password', 'monhoc_id','user_role']
    form_columns = ['ho', 'ten', 'username', 'password', 'active','monhoc_id']

    def create_model(self, form):
        model = self.model()
        form.populate_obj(model)
        model.user_role = UserRole.TEACHER  # Tự động gán user_role
        self.session.add(model)
        self.session.commit()
        return model


class GradeView(ModelView):
    column_list = ['name', 'lops']
    form_columns = ['name']

class MonHocView(ModelView):
    column_list = ['name', 'teachers']
    form_columns = ['name']

class UserView(ModelView):
    form_columns = ['ho', 'ten', 'username', 'password', 'active']  # Thêm user_role vào form_columns





admin.add_view(UserView(User, db.session, name='User'))
admin.add_view(TeacherView(Teacher, db.session, name='Giáo viên'))
admin.add_view(LopView(Lop, db.session, name='Lớp'))
admin.add_view(GradeView(Grade, db.session, name='Khối'))
admin.add_view(MonHocView(MonHoc, db.session, name='Môn học'))
