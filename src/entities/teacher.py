# teacher.py
from db import get_connection

# 增加教师
def add_teacher(teacher_id, name, department=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Teacher WHERE TeacherID=%s", (teacher_id,))
    if cursor.fetchone():
        conn.close()
        print(f"教师 {teacher_id} 已存在")
        return
    cursor.execute("INSERT INTO Teacher (TeacherID, Name, Department) VALUES (%s,%s,%s)", (teacher_id,name,department))
    conn.commit()
    conn.close()

# 删除教师
def delete_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Teacher WHERE TeacherID=%s", (teacher_id,))
    conn.commit()
    conn.close()

# 修改教师
def update_teacher(teacher_id, name=None, department=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE Teacher SET "
    params=[]
    if name:
        sql += "Name=%s,"
        params.append(name)
    if department:
        sql += "Department=%s,"
        params.append(department)
    sql = sql.rstrip(',') + " WHERE TeacherID=%s"
    params.append(teacher_id)
    cursor.execute(sql, tuple(params))
    conn.commit()
    conn.close()

# 查询教师
def query_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Teacher WHERE TeacherID=%s", (teacher_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# 查询教师所授课程
def query_teacher_courses(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Course WHERE TeacherID=%s", (teacher_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def query_all_teachers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TeacherID, Name, Department FROM Teacher")
    result = cursor.fetchall()
    conn.close()
    return result