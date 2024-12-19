from testapp import app, dao
from flask import request, render_template, session, redirect, url_for
from testapp.admin import *

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/grade")
def view_grade():
    grades = dao.load_grade()
    return render_template('grade.html', grades=grades)

@app.route("/class")
def view_class():
    grade_id = request.args.get('grade_id')
    classes = dao.load_class(grade_id)

    return render_template('class.html', classes=classes)

@app.route("/student")
def view_student():
    students = dao.load_student()
    return render_template('student.html', students=students)

@app.route("/diem")
def view_diem():
    diems = dao.load_diem()
    students = dao.load_student()

    return render_template('diem.html', diems=diems, students=students)


@app.route("/login", methods=['GET', 'POST'])
def view_login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        users = dao.load_user()
        user = [u for u in users if u.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        # Chuyển về trang login khi sai mk
        return redirect(url_for('view_login'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)