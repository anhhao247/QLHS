from testapp import app, dao
from flask import request, render_template

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/grade")
def view_grade():
    grades = dao.load_grade()
    return render_template('grade.html', grades=grades)

@app.route("/class")
def view_class():
    classes = dao.load_class()
    return render_template('class.html', classes=classes)

@app.route("/student")
def view_student():
    students = dao.load_student()
    return render_template('student.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)