from testapp import app, db
from flask_admin import Admin, AdminIndexView, expose
from testapp.models import Grade, Lop, Student, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Field


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='Student Management', template_mode='bootstrap4', index_view=MyAdminIndexView())

class GradeView(ModelView):
    pass

class LopView(ModelView):
    form_columns = ["name", "siso", "grade_id"]
    column_list = ["name", "siso", "grade_id"]


admin.add_view(GradeView(Grade, db.session))
admin.add_view(LopView(Lop, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(User, db.session))

