from flask import redirect
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3' 
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
class course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True)
    course_name = db.Column(db.String, unique=True)
    course_description = db.Column(db.String)
class student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
class enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer,   db.ForeignKey("student.student_id"), primary_key=True, nullable=False)
    ecourse_id = db.Column(db.Integer,  db.ForeignKey("course.course_id"), primary_key=True, nullable=False) 
@app.route("/",methods=['GET','POST'])
def Home():
    articles = course.query.all()
    students = student.query.all()
    statement = 'No student found.Add students now ?'
    return render_template('index.html',statement=statement,students=students)

@app.route("/student/create",methods=["GET","POST"])
def add_student():
    if request.method=="GET":
        return render_template('addstudent.html')
    elif request.method=="POST":
        query0 = student(roll_number=request.form['roll'],first_name=request.form['f_name'],last_name=request.form['l_name'])
        try:
            db.session.add(query0)
            db.session.commit()
        except:
            return render_template('already_exist.html')
        for i in request.form:
            if i in ['course1','course2','course3','course4']:
                query1 = db.session.query(course).filter(course.course_name==request.form[i]).first()
                query2 = enrollments(ecourse_id=query1.course_id,estudent_id=query0.student_id)
                db.session.add(query2)
        db.session.commit()
        return redirect("/")
@app.route("/student/<int:student_id>/update",methods=['GET',"POST"])
def update(student_id):
    students = student.query.all()
    if request.method=="GET":
        return render_template('update.html',student=students)
    elif request.method=="POST":
        roll = student.query.filter_by(roll_number=student_id).first()
        print(roll.roll_number)
        print(student_id)
        roll.first_name = request.form['f_name']
        roll.last_name = request.form['l_name']
        roll2 = enrollments.query.filter_by(estudent_id=roll.student_id).delete()
        db.session.commit()
        for i in request.form:
            if i in ['course1','course2','course3','course4']:
                query1 = db.session.query(course).filter(course.course_name==request.form[i]).first()
                query2 = enrollments(ecourse_id=query1.course_id,estudent_id=roll.student_id)
                db.session.add(query2)
        db.session.commit()
        return redirect("/")


@app.route("/student/<int:student_id>/delete",methods=['GET',"POST"])
def delete(student_id):
    roll = student.query.filter_by(student_id=student_id).delete()
    roll2 = enrollments.query.filter_by(estudent_id=student_id).delete()
    db.session.commit()
    return redirect("/")

@app.route("/student/<int:student_id>",methods=['GET',"POST"])
def details(student_id):
    students = student.query.all()
    roll = student.query.filter_by(student_id=student_id).first()
    q = db.session.query(course).join(enrollments).filter(enrollments.estudent_id==student_id).all()
    return render_template('student_detail.html',student=roll,course=q)

if __name__=='__main__':
    app.run(debug=True)