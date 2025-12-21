# gui_main.py
import tkinter as tk
from tkinter import ttk, messagebox

from entities.student import *
from entities.course import *
from entities.score import *
from entities.student_class import *
from entities.teacher import *

from check import *

# ---------------- 主窗口 ----------------
root = tk.Tk()
root.title("学生管理系统")
root.geometry("900x600")

tab_control = ttk.Notebook(root)

# ---------------- 学生管理 Tab ----------------
student_tab = ttk.Frame(tab_control)
tab_control.add(student_tab, text='学生管理')

# 输入框
tk.Label(student_tab, text="学号").grid(row=0, column=0)
student_id_entry = tk.Entry(student_tab)
student_id_entry.grid(row=0, column=1)

tk.Label(student_tab, text="姓名").grid(row=1, column=0)
student_name_entry = tk.Entry(student_tab)
student_name_entry.grid(row=1, column=1)

tk.Label(student_tab, text="性别").grid(row=2, column=0)
student_gender_entry = tk.Entry(student_tab)
student_gender_entry.grid(row=2, column=1)

tk.Label(student_tab, text="班级ID").grid(row=3, column=0)
student_class_entry = tk.Entry(student_tab)
student_class_entry.grid(row=3, column=1)

# 学生操作函数
def add_student_gui():
    student_id = student_id_entry.get()
    name = student_name_entry.get()
    gender = student_gender_entry.get()
    class_id = student_class_entry.get() or None

    # 前置校验
    is_valid, err_msg = check_student(student_id, name, gender, class_id)
    if not is_valid:
        messagebox.showerror("输入错误", err_msg)
        return
    
    try:
        add_student(student_id, name, gender, class_id)
        messagebox.showinfo("成功", f"学生 {student_id} 已添加")
    except Exception as e:
        messagebox.showerror("错误", str(e))

def query_student_gui():
    student_id = student_id_entry.get()
    result = query_student(student_id)
    messagebox.showinfo("查询结果", str(result))

def delete_student_gui():
    student_id = student_id_entry.get()
    delete_student(student_id)
    messagebox.showinfo("成功", f"学生 {student_id} 已删除")

def update_student_gui():
    student_id = student_id_entry.get()
    name = student_name_entry.get() or None
    gender = student_gender_entry.get() or None
    class_id = student_class_entry.get() or None
    update_student(student_id, name, gender, class_id)
    messagebox.showinfo("成功", f"学生 {student_id} 已更新")

# 按钮
tk.Button(student_tab, text="添加学生", command=add_student_gui).grid(row=4, column=0)
tk.Button(student_tab, text="查询学生", command=query_student_gui).grid(row=4, column=1)
tk.Button(student_tab, text="删除学生", command=delete_student_gui).grid(row=5, column=0)
tk.Button(student_tab, text="修改学生", command=update_student_gui).grid(row=5, column=1)

# ---------------- 成绩管理 Tab ----------------
score_tab = ttk.Frame(tab_control)
tab_control.add(score_tab, text='成绩管理')

tk.Label(score_tab, text="学号").grid(row=0, column=0)
score_student_entry = tk.Entry(score_tab)
score_student_entry.grid(row=0, column=1)

tk.Label(score_tab, text="课程ID").grid(row=1, column=0)
score_course_entry = tk.Entry(score_tab)
score_course_entry.grid(row=1, column=1)

tk.Label(score_tab, text="学期").grid(row=2, column=0)
score_semester_entry = tk.Entry(score_tab)
score_semester_entry.grid(row=2, column=1)

tk.Label(score_tab, text="类型").grid(row=3, column=0)
score_type_entry = tk.Entry(score_tab)
score_type_entry.grid(row=3, column=1)

tk.Label(score_tab, text="成绩").grid(row=4, column=0)
score_entry = tk.Entry(score_tab)
score_entry.grid(row=4, column=1)

# 成绩操作
def add_score_gui():
    sid = score_student_entry.get()
    cid = score_course_entry.get()
    semester = score_semester_entry.get()
    score_type = score_type_entry.get() or "平时"
    score_val = int(score_entry.get())

    # 前置校验
    is_valid, err_msg = check_score(sid, cid, semester, score_type="平时", score_val=None)
    if not is_valid:
        messagebox.showerror("输入错误", err_msg)
        return
    add_score(sid, cid, semester, score_type, score_val)
    messagebox.showinfo("成功", f"成绩已添加")

def query_score_gui():
    sid = score_student_entry.get()
    result = query_scores(sid)
    messagebox.showinfo("查询结果", str(result))

def update_score_gui():
    sid = score_student_entry.get()
    cid = score_course_entry.get()
    semester = score_semester_entry.get()
    score_type = score_type_entry.get() or "平时"
    score_val = int(score_entry.get())
    update_score(sid, cid, semester, score_type, score_val)
    messagebox.showinfo("成功", f"成绩已更新")

def delete_score_gui():
    sid = score_student_entry.get()
    cid = score_course_entry.get()
    semester = score_semester_entry.get()
    score_type = score_type_entry.get() or "平时"
    delete_score(sid, cid, semester, score_type)
    messagebox.showinfo("成功", f"成绩已删除")

# 按钮
tk.Button(score_tab, text="添加成绩", command=add_score_gui).grid(row=5, column=0)
tk.Button(score_tab, text="查询成绩", command=query_score_gui).grid(row=5, column=1)
tk.Button(score_tab, text="修改成绩", command=update_score_gui).grid(row=6, column=0)
tk.Button(score_tab, text="删除成绩", command=delete_score_gui).grid(row=6, column=1)

# ---------------- 教师管理 Tab ----------------
teacher_tab = ttk.Frame(tab_control)
tab_control.add(teacher_tab, text='教师管理')

tk.Label(teacher_tab, text="教师ID").grid(row=0, column=0)
teacher_id_entry = tk.Entry(teacher_tab)
teacher_id_entry.grid(row=0, column=1)

tk.Label(teacher_tab, text="姓名").grid(row=1, column=0)
teacher_name_entry = tk.Entry(teacher_tab)
teacher_name_entry.grid(row=1, column=1)

tk.Label(teacher_tab, text="部门").grid(row=2, column=0)
teacher_dept_entry = tk.Entry(teacher_tab)
teacher_dept_entry.grid(row=2, column=1)

def add_teacher_gui():
    tid = teacher_id_entry.get()
    name = teacher_name_entry.get()
    dept = teacher_dept_entry.get() or None

    # 前置校验
    is_valid, err_msg = check_teacher(tid, name, dept=None)
    if not is_valid:
        messagebox.showerror("输入错误", err_msg)
        return
    add_teacher(tid, name, dept)
    messagebox.showinfo("成功", f"教师 {tid} 已添加")

def query_teacher_gui():
    tid = teacher_id_entry.get()
    result = query_teacher(tid)
    messagebox.showinfo("查询结果", str(result))

def delete_teacher_gui():
    tid = teacher_id_entry.get()
    delete_teacher(tid)
    messagebox.showinfo("成功", f"教师 {tid} 已删除")

def update_teacher_gui():
    tid = teacher_id_entry.get()
    name = teacher_name_entry.get() or None
    dept = teacher_dept_entry.get() or None
    update_teacher(tid, name, dept)
    messagebox.showinfo("成功", f"教师 {tid} 已更新")

tk.Button(teacher_tab, text="添加教师", command=add_teacher_gui).grid(row=3, column=0)
tk.Button(teacher_tab, text="查询教师", command=query_teacher_gui).grid(row=3, column=1)
tk.Button(teacher_tab, text="删除教师", command=delete_teacher_gui).grid(row=4, column=0)
tk.Button(teacher_tab, text="修改教师", command=update_teacher_gui).grid(row=4, column=1)

# ---------------- 班级管理 Tab ----------------
class_tab = ttk.Frame(tab_control)
tab_control.add(class_tab, text='班级管理')

tk.Label(class_tab, text="班级ID").grid(row=0, column=0)
class_id_entry = tk.Entry(class_tab)
class_id_entry.grid(row=0, column=1)

tk.Label(class_tab, text="班级名称").grid(row=1, column=0)
class_name_entry = tk.Entry(class_tab)
class_name_entry.grid(row=1, column=1)

tk.Label(class_tab, text="部门").grid(row=2, column=0)
class_dept_entry = tk.Entry(class_tab)
class_dept_entry.grid(row=2, column=1)

def add_class_gui():
    cid = class_id_entry.get()
    cname = class_name_entry.get()
    dept = class_dept_entry.get() or None
    
    # 前置校验
    is_valid, err_msg = check_class(cid, cname, dept=None)
    if not is_valid:
        messagebox.showerror("输入错误", err_msg)
        return
    add_class(cid, cname, dept)
    messagebox.showinfo("成功", f"班级 {cid} 已添加")

def query_class_gui():
    cid = class_id_entry.get()
    result = query_class(cid)
    messagebox.showinfo("查询结果", str(result))

def delete_class_gui():
    cid = class_id_entry.get()
    delete_class(cid)
    messagebox.showinfo("成功", f"班级 {cid} 已删除")

def update_class_gui():
    cid = class_id_entry.get()
    cname = class_name_entry.get() or None
    dept = class_dept_entry.get() or None
    update_class(cid, cname, dept)
    messagebox.showinfo("成功", f"班级 {cid} 已更新")

tk.Button(class_tab, text="添加班级", command=add_class_gui).grid(row=3, column=0)
tk.Button(class_tab, text="查询班级", command=query_class_gui).grid(row=3, column=1)
tk.Button(class_tab, text="删除班级", command=delete_class_gui).grid(row=4, column=0)
tk.Button(class_tab, text="修改班级", command=update_class_gui).grid(row=4, column=1)

# ---------------- 课程管理 Tab ----------------
course_tab = ttk.Frame(tab_control)
tab_control.add(course_tab, text='课程管理')

tk.Label(course_tab, text="课程ID").grid(row=0, column=0)
course_id_entry = tk.Entry(course_tab)
course_id_entry.grid(row=0, column=1)

tk.Label(course_tab, text="课程名称").grid(row=1, column=0)
course_name_entry = tk.Entry(course_tab)
course_name_entry.grid(row=1, column=1)

tk.Label(course_tab, text="学分").grid(row=2, column=0)
course_credit_entry = tk.Entry(course_tab)
course_credit_entry.grid(row=2, column=1)

tk.Label(course_tab, text="教师ID").grid(row=3, column=0)
course_teacher_entry = tk.Entry(course_tab)
course_teacher_entry.grid(row=3, column=1)

def add_course_gui():
    cid = course_id_entry.get()
    cname = course_name_entry.get()
    credits = int(course_credit_entry.get() or 3)
    tid = course_teacher_entry.get() or None
        
    # 前置校验
    is_valid, err_msg = check_course(cid, cname, credits=3, tid=None)
    if not is_valid:
        messagebox.showerror("输入错误", err_msg)
        return
    add_course(cid, cname, credits, tid)
    messagebox.showinfo("成功", f"课程 {cid} 已添加")

def query_course_gui():
    cid = course_id_entry.get()
    result = query_course(cid)
    messagebox.showinfo("查询结果", str(result))

def delete_course_gui():
    cid = course_id_entry.get()
    delete_course(cid)
    messagebox.showinfo("成功", f"课程 {cid} 已删除")

def update_course_gui():
    cid = course_id_entry.get()
    cname = course_name_entry.get() or None
    credits = int(course_credit_entry.get() or 3)
    tid = course_teacher_entry.get() or None
    update_course(cid, cname, credits, tid)
    messagebox.showinfo("成功", f"课程 {cid} 已更新")

tk.Button(course_tab, text="添加课程", command=add_course_gui).grid(row=4, column=0)
tk.Button(course_tab, text="查询课程", command=query_course_gui).grid(row=4, column=1)
tk.Button(course_tab, text="删除课程", command=delete_course_gui).grid(row=5, column=0)
tk.Button(course_tab, text="修改课程", command=update_course_gui).grid(row=5, column=1)

# ---------------- 显示 Tab ----------------
tab_control.pack(expand=1, fill='both')

root.mainloop()
