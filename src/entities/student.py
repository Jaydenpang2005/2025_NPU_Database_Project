# student.py
from db import get_connection

# 增加学生
def add_student(student_id, name, gender, class_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student WHERE ID=%s", (student_id,))
    if cursor.fetchone():
        conn.close()
        print(f"学生 {student_id} 已存在，跳过插入")
        return
    sql = "INSERT INTO Student (ID, Name, Gender, ClassID) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql, (student_id, name, gender, class_id))
    conn.commit()
    conn.close()

# 删除学生
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Student WHERE ID=%s", (student_id,))
    conn.commit()
    conn.close()

# 修改学生
def update_student(student_id, name=None, gender=None, class_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE Student SET "
    params = []
    if name:
        sql += "Name=%s,"
        params.append(name)
    if gender:
        sql += "Gender=%s,"
        params.append(gender)
    if class_id:
        sql += "ClassID=%s,"
        params.append(class_id)
    sql = sql.rstrip(',') + " WHERE ID=%s"
    params.append(student_id)
    cursor.execute(sql, tuple(params))
    conn.commit()
    conn.close()

# 查询学生信息
def query_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student WHERE ID=%s", (student_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# 查询班级信息
def query_class_students(class_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student WHERE ClassID=%s", (class_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def query_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Name, Gender, ClassID FROM Student")
    result = cursor.fetchall()
    conn.close()
    return result

# # student.py
# from db import get_connection

# # 增加学生
# def add_student(id, name, gender):
#     conn = get_connection()
#     cursor = conn.cursor()
#     # 先检查是否存在
#     cursor.execute("SELECT * FROM student WHERE ID=%s", (id,))
#     if cursor.fetchone():
#         print(f"学生 {id} 已存在，跳过插入")
#         conn.close()
#         return
#     # 不存在则插入
#     sql = "INSERT INTO student (ID, name, gender) VALUES (%s, %s, %s)"
#     cursor.execute(sql, (id, name, gender))
#     conn.commit()
#     conn.close()


# # 查询学生
# def query_student(id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     sql = "SELECT * FROM Student WHERE ID=%s"
#     cursor.execute(sql, id)
#     result = cursor.fetchone()
#     conn.close()
#     return result

# # 修改学生
# def update_student(id, name):
#     conn = get_connection()
#     cursor = conn.cursor()
#     sql = "UPDATE Student SET Name=%s WHERE ID=%s"
#     cursor.execute(sql, (name, id))
#     conn.commit()
#     conn.close()

# # 删除学生
# def delete_student(id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     sql = "DELETE FROM Student WHERE ID=%s"
#     cursor.execute(sql, id)
#     conn.commit()
#     conn.close()
