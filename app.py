
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

import forms

app = Flask(__name__)
students_form = forms.Student_form()
course_form = forms.Course_form()

#conection mysql
try:
    app.config['MYSQL_HOST'] = 'containers-us-west-121.railway.app'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '6eujku5IdP5t0SCDdDvO'
    app.config['MYSQL_DB'] = 'railway'
    app.config['MYSQL_PORT'] = 6153
    mysql = MySQL(app)
    print('successful connection')
except:
    print('failed connection')


@app.route('/')
def Home():
    return render_template("index.html")


#=================ROUTES STUDENTS============================#
@app.route('/admin/students')
def students(data = dict()):
    try:
        sql = """
                SELECT * FROM student
            """
        
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        data['students'] = cursor.fetchall()
        cursor.close()
    except:
        data['error'] = 'error querying student'
    return render_template('student.html', model = data, form=students_form)

@app.route('/admin/students/new', methods=['POST'])
def new_student():
    student_form = forms.Student_form(request.form) 
    data = dict()

    if student_form.validate():
        id = student_form.id.data
        names = student_form.names.data
        surnames = student_form.surnames.data
        email = student_form.email.data
        phone = student_form.phone.data

        try:
            sql = f"""
                    INSERT INTO student (id, names, surnames, email, phone) 
                    VALUES ('{id}', '{names}', '{surnames}', '{email}', '{phone}')
                """
            
            cursor = mysql.connection.cursor()
            cursor.execute(sql)
            row = cursor.rowcount
            mysql.connection.commit()
            cursor.close()
            if row != 1:
                data['error'] = 'number of row affected is not correct'
            data['succes'] = 'Create student succes'
        except Exception as ex:
            data['error'] = 'Error inserting student data'  
    else:
        data['error'] = 'No se creo el studieante'
    return students(data)

@app.route('/admin/student/update/<id>')
def update_student(id):
    data = dict()
    try:
        sql = f"""
                SELECT * FROM student 
                WHERE id = '{id}'
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        data['student'] = cursor.fetchone()
        cursor.close()
    except:
        data['error'] = 'error update'
    return students(data)

@app.route('/admin/students/update', methods=['POST'])
def update_student_true():
    
    student_form = forms.Student_form(request.form)
    data = dict()
    
    id = request.form['id']
    names = student_form.names.data
    surnames = student_form.surnames.data
    email = student_form.email.data
    phone = student_form.phone.data
    
    try:
        sql = f"""
                UPDATE student
                SET names='{names}', surnames='{surnames}', email='{email}', phone='{phone}'
                WHERE id={id}
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
        data['succes'] = 'update student succes'
    except:
        data['error'] = 'Error updating student data' 
    
    return students(data)
    
@app.route('/admin/student/delete/<id>')
def delete_student(id):
    data = dict()
    try:
        sql = f"""
                DELETE FROM student WHERE id={id}
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
        data['succes'] = "student delete succes"
    except:
        data['error'] = 'error delete'
    return students(data)

#=================ROUTES COURSE============================#

@app.route('/admin/courses')
def courses(data = dict()):
    try:
        sql = "SELECT * FROM course"
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        data['courses'] = cursor.fetchall()
        cursor.close()
    except:
        pass
    return render_template('course.html', model=data, form=course_form)

@app.route('/admin/course/new', methods=['POST'])
def new_course():
    course_form = forms.Course_form(request.form)
    data = dict()
    if course_form.validate():
        name = course_form.name.data
        credits = course_form.credits.data

        try:
            sql = f"""
                    INSERT INTO course (name, credits)
                    VALUES ('{name}',{credits})
                """
            cursor = mysql.connection.cursor()
            cursor.execute(sql)
            if cursor.rowcount != 1:
                data['error'] = 'error'
            else:
                mysql.connection.commit()
                cursor.close()
                data['succes'] = 'Course Add success'
        except:
            data['error'] = 'Error inserting course'
    return courses(data)

@app.route('/admin/courses/delete/<id>')
def delete_course(id):
    data = dict()
    try:
        sql = f"""
                DELETE FROM course WHERE id={id}
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
        data['succes'] = 'Delete course success'
    except:
        data['error'] = 'Error delete course'
    return courses(data)

@app.route('/admin/courses/get/<id>')
def course_get(id):
    data = dict()
    try:
        sql = f"""
                SELECT * FROM course WHERE id={id}
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        data['course'] = cursor.fetchone()
        cursor.close()
    except Exception as ex:
        print(ex)
        data['error'] = 'Error geting course'
    return courses(data)

@app.route('/admin/course/update/<id>', methods=['POST'])
def course_update(id):
    course_form = forms.Course_form(request.form)
    if course_form.validate():
        name = course_form.name.data
        credits = course_form.credits.data
        
        data = dict()
        try:
            sql = f"""
                    UPDATE course 
                    SET name='{name}', credits={credits}
                    WHERE id={id}
                """
            cursor = mysql.connection.cursor()
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.close()
            data['succes'] = 'Update course success'
        except Exception as ex:
            print(ex)
            data['error'] = 'Error updating course'
    return courses()

#=================ROUTES INSCRIPTION=========================#

@app.route('/inscription')
def register():
    return render_template('inscription.html')

@app.route('/inscription/search', methods=['POST'])
def search_inscription(id=None, data=dict()):
    if id == None:
        id = request.form['id']
    
    try:
        #student
        sql = f"""
                SELECT * FROM student
                WHERE id={id}
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        data['student'] = cursor.fetchone()
        cursor.close()
        
        #course_registered
        sql = f"""
                SELECT co.id, co.name, co.credits
                FROM inscription ins
                JOIN course co on (ins.id_course = co.id)
                WHERE ins.id_student={id}
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        data['courses_student'] = cursor.fetchall()
        cursor.close()
        
        #courses
        sql = f"""
                SELECT *
                FROM course
                ORDER BY name
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        data['courses'] = cursor.fetchall()
        cursor.close()
    except:
        data['error'] = 'Error'
        
    return render_template('inscription.html', model=data)

@app.route('/inscription/add', methods=['POST'])
def add_inscription():
    id = request.form['id']
    course = request.form['course']
    
    data = dict()
    try:
        sql = f"""
                INSERT INTO inscription (id_student, id_course)
                VALUES ('{id}', {course})
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        if cursor.rowcount != 1:
            data['error'] = 'error'
        else:
            mysql.connection.commit()
            cursor.close()
            data['succes'] = 'Course register success'
    except Exception as ex:
        print(ex)
        data['error'] = 'Error registered success'
    return search_inscription(id, data)

@app.route('/inscription/delete/<id>/<course>')
def inscription_delete(id, course):
    data = dict()
    try:
        sql = f"""
                DELETE FROM inscription 
                WHERE id_student='{id}'
                AND id_course = {course}
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
        data['succes'] = 'Delete inscription success'
    except Exception as ex:
        print(ex)
        data['error'] = 'Error delete inscription'
    return search_inscription(id, data)

app.run()