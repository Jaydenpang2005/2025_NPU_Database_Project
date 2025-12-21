# gui_with_overview.py
import tkinter as tk
from tkinter import ttk, messagebox

from entities.student import *
from entities.course import *
from entities.score import *
from entities.teacher import *
from entities.student_class import *

root = tk.Tk()
root.title("学生管理系统 - 实时表格版")
root.geometry("1000x700")

tab_control = ttk.Notebook(root)

# ----------------- 学生管理 Tab -----------------
student_tab = ttk.Frame(tab_control)
tab_control.add(student_tab, text='学生管理')

# Treeview 显示
student_tree = ttk.Treeview(student_tab, columns=("ID","Name","Gender","ClassID"), show="headings")
for col in ("ID","Name","Gender","ClassID"):
    student_tree.heading(col, text=col)
student_tree.pack(fill='both', expand=True)

def refresh_student_tree():
    for row in student_tree.get_children():
        student_tree.delete(row)
    # 获取所有学生
    # 你可以写一个 query_all_students() 函数返回列表
    students = query_all_students()  # [(id, name, gender, class_id), ...]
    for s in students:
        student_tree.insert("", "end", values=s)

tk.Button(student_tab, text="刷新学生表", command=refresh_student_tree).pack()

# ----------------- 成绩管理 Tab -----------------
score_tab = ttk.Frame(tab_control)
tab_control.add(score_tab, text='成绩管理')

score_tree = ttk.Treeview(score_tab, columns=("ID","CourseName","Semester","Type","Score"), show="headings")
for col in ("ID","CourseName","Semester","Type","Score"):
    score_tree.heading(col, text=col)
score_tree.pack(fill='both', expand=True)

def refresh_score_tree():
    for row in score_tree.get_children():
        score_tree.delete(row)
    scores = query_all_scores()  # [(id, course, semester, type, score), ...]
    for s in scores:
        score_tree.insert("", "end", values=s)

tk.Button(score_tab, text="刷新成绩表", command=refresh_score_tree).pack()

# ----------------- 教师管理 Tab -----------------
teacher_tab = ttk.Frame(tab_control)
tab_control.add(teacher_tab, text='教师管理')

teacher_tree = ttk.Treeview(teacher_tab, columns=("TeacherID","Name","Department"), show="headings")
for col in ("TeacherID","Name","Department"):
    teacher_tree.heading(col, text=col)
teacher_tree.pack(fill='both', expand=True)

def refresh_teacher_tree():
    for row in teacher_tree.get_children():
        teacher_tree.delete(row)
    teachers = query_all_teachers()  # [(id, name, Department), ...]
    for t in teachers:
        teacher_tree.insert("", "end", values=t)

tk.Button(teacher_tab, text="刷新教师表", command=refresh_teacher_tree).pack()

# ----------------- 班级管理 Tab -----------------
class_tab = ttk.Frame(tab_control)
tab_control.add(class_tab, text='班级管理')

class_tree = ttk.Treeview(class_tab, columns=("ClassID","ClassName","Department"), show="headings")
for col in ("ClassID","ClassName","Department"):
    class_tree.heading(col, text=col)
class_tree.pack(fill='both', expand=True)

def refresh_class_tree():
    for row in class_tree.get_children():
        class_tree.delete(row)
    classes = query_all_classes()  # [(id, name, Department), ...]
    for c in classes:
        class_tree.insert("", "end", values=c)

tk.Button(class_tab, text="刷新班级表", command=refresh_class_tree).pack()

# ----------------- 课程管理 Tab -----------------
course_tab = ttk.Frame(tab_control)
tab_control.add(course_tab, text='课程管理')

course_tree = ttk.Treeview(course_tab, columns=("CourseID","CourseName","Credits","TeacherID"), show="headings")
for col in ("CourseID","CourseName","Credits","TeacherID"):
    course_tree.heading(col, text=col)
course_tree.pack(fill='both', expand=True)

def refresh_course_tree():
    for row in course_tree.get_children():
        course_tree.delete(row)
    courses = query_all_courses()  # [(id, name, credits, teacher_id), ...]
    for c in courses:
        course_tree.insert("", "end", values=c)

tk.Button(course_tab, text="刷新课程表", command=refresh_course_tree).pack()

# ----------------- 主窗口显示 -----------------
tab_control.pack(expand=1, fill='both')
root.mainloop()
