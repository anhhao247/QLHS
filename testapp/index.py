from click import style

from testapp import app, dao
from flask import request, render_template, session, redirect, url_for, flash
from testapp.admin import *
from testapp.models import Diem, MonHoc
import pandas as pd
from sqlalchemy.exc import IntegrityError
from datetime import datetime


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


    return render_template('diem.html')


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

@app.route('/upload', methods=['GET', 'POST'])
def upload_students():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash("Vui lòng chọn file!", "error")
            return redirect(request.url)

        try:
            # Đọc file Excel bằng pandas
            df = pd.read_excel(file)

            # Kiểm tra và ánh xạ cột nếu cần
            required_columns = ['ho', 'ten', 'sex', 'DoB', 'address', 'sdt', 'email']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                raise ValueError(f"Các cột sau bị thiếu trong file Excel: {', '.join(missing_columns)}")

            # Duyệt từng dòng và thêm vào database
            for _, row in df.iterrows():
                # Tính tuổi từ ngày sinh
                dob = pd.to_datetime(row['DoB'])
                current_date = datetime.now()
                age = (current_date - dob).days // 365  # Tính tuổi bằng số ngày chia cho 365

                # Kiểm tra điều kiện độ tuổi
                if age < 15 or age > 20:
                    flash(f"Học sinh {row['ho']} {row['ten']} không trong độ tuổi từ 15 đến 20.", "warning")
                    continue  # Bỏ qua học sinh này

                # Thêm học sinh vào database nếu hợp lệ
                student = Student(
                    ho=row['ho'],
                    ten=row['ten'],
                    sex=row['sex'],
                    DoB=dob,
                    address=row['address'],
                    sdt=row['sdt'],
                    email=row['email']
                )
                db.session.add(student)

            # Lưu các thay đổi
            db.session.commit()
            flash("Thêm học sinh thành công!", "success")
            return redirect(url_for('upload_students'))

        except ValueError as ve:
            flash(str(ve), "error")
        except IntegrityError:
            db.session.rollback()
            flash("Lỗi: Trùng lặp hoặc dữ liệu không hợp lệ!", "error")
        except Exception as e:
            flash(f"Lỗi không xác định: {str(e)}", "error")

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)