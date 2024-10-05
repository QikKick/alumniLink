from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Alumni(db.Model):
    __tablename__ = 'alumni'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)

    work_experiences = db.relationship('WorkExperience', backref='alumni', cascade='all, delete-orphan', lazy=True)
    studies = db.relationship('Study', backref='alumni', cascade='all, delete-orphan', lazy=True)
    certificates = db.relationship('Certificate', backref='alumni', cascade='all, delete-orphan', lazy=True)
    skills = db.relationship('AlumniSkill', backref='alumni', cascade='all, delete-orphan', lazy=True)
    posts = db.relationship('Post', backref='alumni', cascade='all, delete-orphan', lazy=True)


class WorkExperience(db.Model):
    __tablename__ = 'work_experience'
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_working = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        db.CheckConstraint(
            "(is_working = TRUE AND end_date IS NULL) OR (is_working = FALSE AND end_date IS NOT NULL)",
            name="check_is_working_end_date"
        ),
        db.CheckConstraint(
            "(end_date IS NULL OR start_date <= end_date)",
            name="check_start_end_date"
        ),
    )


class Study(db.Model):
    __tablename__ = 'study'
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer)

    __table_args__ = (
        db.CheckConstraint(
            "start_year >= 1900 AND start_year <= extract(year from current_date) + 10",
            name="check_start_year"
        ),
        db.CheckConstraint(
            "end_year IS NULL OR start_year <= end_year",
            name="check_start_end_year"
        ),
    )


class Certificate(db.Model):
    __tablename__ = 'certificate'
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)


class AlumniSkill(db.Model):
    __tablename__ = 'alumni_skill'
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id', ondelete='CASCADE'), primary_key=True)
    skill_name = db.Column(db.String(100), primary_key=True)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


class ChangeLog(db.Model):
    __tablename__ = 'change_log'
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    action = db.Column(db.String(10), nullable=False)  # INSERT, UPDATE, DELETE
    change_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    old_data = db.Column(db.JSON)
    new_data = db.Column(db.JSON)

    user = db.relationship('User')


# Add necessary indexes as per the SQL script

db.Index('idx_alumni_name', Alumni.name)
db.Index('idx_alumni_surname', Alumni.surname)
db.Index('idx_alumni_skill_skill_name', AlumniSkill.skill_name)
db.Index('idx_post_creation_date', Post.creation_date)
