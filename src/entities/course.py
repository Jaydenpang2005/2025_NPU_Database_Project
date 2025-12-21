# course.py
from db import get_connection

# 增加课程
def add_course(course_id, course_name, credits=3, teacher_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Course WHERE CourseID=%s", (course_id,))
    if cursor.fetchone():
        conn.close()
        print(f"课程 {course_id} 已存在")
        return
    sql = "INSERT INTO Course (CourseID, CourseName, Credits, TeacherID) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql, (course_id, course_name, credits, teacher_id))
    conn.commit()
    conn.close()

# 删除课程
def delete_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Course WHERE CourseID=%s", (course_id,))
    conn.commit()
    conn.close()

# 修改课程
def update_course(course_id, course_name=None, credits=None, teacher_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE Course SET "
    params = []
    if course_name:
        sql += "CourseName=%s,"
        params.append(course_name)
    if credits:
        sql += "Credits=%s,"
        params.append(credits)
    if teacher_id:
        sql += "TeacherID=%s,"
        params.append(teacher_id)
    sql = sql.rstrip(',') + " WHERE CourseID=%s"
    params.append(course_id)
    cursor.execute(sql, tuple(params))
    conn.commit()
    conn.close()

# 查询课程
def query_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Course WHERE CourseID=%s", (course_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# 按教师或学期查询课程
def query_courses_by_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Course WHERE TeacherID=%s", (teacher_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def query_all_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CourseID, CourseName, Credits, TeacherID FROM Course")
    result = cursor.fetchall()
    conn.close()
    return result

# # course.py
# from db import get_connection

# def add_course(course):
#     conn = get_connection()
#     cursor = conn.cursor()
#     sql = "INSERT INTO Course VALUES (%s)"
#     cursor.execute(sql, course)
#     conn.commit()
#     conn.close()
