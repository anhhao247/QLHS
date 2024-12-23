from functools import wraps

from click import style
from pandas.core import methods

from testapp import app, dao
from flask import request, render_template, session, redirect, url_for, flash, jsonify
from testapp.admin import *
from testapp.dao import get_user_by_id
from testapp.models import Diem, MonHoc, User
import pandas as pd
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from flask import jsonify
from werkzeug.security import check_password_hash


# Đặt khóa bí mật (secret key) cho ứng dụng Flask
app.secret_key = 'secret_key'  # Dùng để mã hóa thông tin session

# Thời gian hết hạn session (ví dụ 1 giờ)
app.permanent_session_lifetime = timedelta(hours=1)

# Tạo Decorator kiểm tra đăng nhập
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('view_login'))  # Nếu không đăng nhập, chuyển hướng đến trang login
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    # Kiểm tra nếu người dùng đã đăng nhập (kiểm tra session)
    if 'user_id' in session:
        user_id = session['user_id']
        user = get_user_by_id(user_id)
        if user:
            return render_template('index.html', user=user)
        else:
            return redirect(url_for('view_login'))  # Chuyển hướng nếu không tìm thấy user
    else:
        return redirect(url_for('view_login'))  # Nếu chưa đăng nhập, chuyển hướng đến trang login


@app.route("/grade")
@login_required
def view_grade():
    user_id = session['user_id']
    user = get_user_by_id(user_id)  # Lấy thông tin người dùng từ cơ sở dữ liệu
    grades = dao.load_grade()
    return render_template('grade.html', grades=grades, user=user)

@app.route("/class")
@login_required
def view_class():
    user_id = session['user_id']
    user = get_user_by_id(user_id)  # Lấy thông tin người dùng từ cơ sở dữ liệu
    grade_id = request.args.get('grade_id')
    classes = dao.load_class(grade_id)

    return render_template('class.html', classes=classes, user=user)

# @app.route("/user")
# def view_user():
#     return render_template('user')

@app.route("/teacher")
@login_required
def view_teacher():
    user_id = session['user_id']
    user = get_user_by_id(user_id)  # Lấy thông tin người dùng từ cơ sở dữ liệu

    teachers = dao.load_teacher()
    return render_template('teacher.html', teachers=teachers, user=user)

@app.route("/student")
@login_required
def view_student():
    user_id = session['user_id']
    user = get_user_by_id(user_id)  # Lấy thông tin người dùng từ cơ sở dữ liệu
    students = dao.load_student()
    return render_template('student.html', students=students, user=user)



@app.route("/diem", methods=["GET", "POST"])
@login_required
def view_diem():
    user_id = session['user_id']
    user = get_user_by_id(user_id)  # Lấy thông tin người dùng từ cơ sở dữ liệu
    if request.method == "POST":
        lop_id = request.form.get("lop")
        monhoc_id = request.form.get("monhoc")
        hoc_ky_id = request.form.get("hoc_ky")

        # Truy vấn cơ sở dữ liệu để lấy bảng điểm
        diems = dao.load_diem_theo_lop_mon_hoc_hoc_ky(lop_id, monhoc_id, hoc_ky_id)

        return render_template('diem.html', diems=diems, user=user)

    # Lấy danh sách lớp, môn học và học kỳ để hiển thị trong dropdown
    danh_sach_lop = dao.load_class()
    danh_sach_mon_hoc = dao.load_monhoc()
    danh_sach_hoc_ky = dao.load_hoc_ky()

    return render_template('diem.html',
                           danh_sach_lop=danh_sach_lop, danh_sach_mon_hoc=danh_sach_mon_hoc,
                           danh_sach_hoc_ky=danh_sach_hoc_ky, user=user)

# monhoc
@app.route("/monhoc")
@login_required
def view_monhoc():
    user_id = session['user_id']
    user = get_user_by_id(user_id)  # Lấy thông tin người dùng từ cơ sở dữ liệu

    monhocs = dao.load_monhoc()
    return render_template('monhoc.html',monhocs=monhocs, user=user)


@app.route("/them_monhoc", methods=['POST'])
@login_required
def them_monhoc():


    data = request.get_json()
    name = data.get("name")

    try:
        if name:
            dao.them_monhoc(name)  # Gọi hàm thêm môn học
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Invalid input"}), 400
    except ValueError as e:  # Bắt lỗi nếu môn học đã tồn tại
        return jsonify({"error": str(e)}), 400


@app.route("/sua_monhoc/<int:id>", methods=['PUT'])
def sua_monhoc(id):
    data = request.get_json()
    name = data.get("name")

    try:
        if dao.sua_monhoc(id, name):
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400  # Trả về lỗi nếu môn học đã tồn tại


@app.route("/xoa_monhoc/<int:id>", methods=['DELETE'])
def xoa_monhoc(id):
    if dao.xoa_monhoc(id):
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Not found"}), 404

# monhoc

@app.route("/login", methods=['GET', 'POST'])
def view_login():
    if request.method == 'POST':
        data = request.get_json()  # Lấy dữ liệu JSON từ yêu cầu AJAX
        username = data.get('username')
        password = data.get('password')

        # Lấy thông tin người dùng từ cơ sở dữ liệu
        user = dao.get_user_by_username(username)

        if user and User.check_password(user["password"], password):
            # Đăng nhập thành công, lưu thông tin vào session
            session.permanent = True  # Đảm bảo session có thời gian hết hạn
            session['user_id'] = user['id']
            return jsonify({"success": True}), 200  # Trả về thông báo thành công
        else:
            # Đăng nhập thất bại, trả về thông báo lỗi
            return jsonify({"success": False, "error": "Tên đăng nhập hoặc mật khẩu không chính xác"}), 400

    return render_template('login.html')




@app.route("/logout")
def logout():
    session.clear()  # Xóa toàn bộ session
    flash("Bạn đã đăng xuất thành công!", "success")
    return redirect(url_for('view_login'))  # Chuyển hướng về trang login


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