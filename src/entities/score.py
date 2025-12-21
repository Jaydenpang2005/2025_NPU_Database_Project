# score.py
from db import get_connection

# 添加成绩
def add_score(student_id, course_id, semester, score_type='平时', score=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Score WHERE StudentID=%s AND CourseID=%s AND Semester=%s AND ScoreType=%s",
        (student_id, course_id, semester, score_type)
    )
    if cursor.fetchone():
        print(f"成绩已存在，跳过插入")
        conn.close()
        return
    sql = "INSERT INTO Score (StudentID, CourseID, Semester, ScoreType, Score) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(sql, (student_id, course_id, semester, score_type, score))
    conn.commit()
    conn.close()

# 修改成绩
def update_score(student_id, course_id, semester, score_type, score):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE Score SET Score=%s WHERE StudentID=%s AND CourseID=%s AND Semester=%s AND ScoreType=%s"
    cursor.execute(sql, (score, student_id, course_id, semester, score_type))
    conn.commit()
    conn.close()

# 删除成绩
def delete_score(student_id, course_id, semester, score_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM Score WHERE StudentID=%s AND CourseID=%s AND Semester=%s AND ScoreType=%s",
        (student_id, course_id, semester, score_type)
    )
    conn.commit()
    conn.close()

# 查询成绩
def query_scores(student_id, semester=None):
    conn = get_connection()
    cursor = conn.cursor()
    if semester:
        cursor.execute(
            "SELECT * FROM Score WHERE StudentID=%s AND Semester=%s",
            (student_id, semester)
        )
    else:
        cursor.execute("SELECT * FROM Score WHERE StudentID=%s", (student_id,))
    result = cursor.fetchall()
    conn.close()
    return result

# 查询平均成绩
def query_avg_score(student_id, semester=None):
    conn = get_connection()
    cursor = conn.cursor()
    if semester:
        cursor.execute("SELECT AvgScore FROM V_AvgScore WHERE StudentID=%s AND Semester=%s", (student_id, semester))
    else:
        cursor.execute("SELECT AvgScore FROM V_AvgScore WHERE StudentID=%s", (student_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# 查询班级或课程排名
def query_score_ranking(course_id, semester):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT StudentID, Score
        FROM Score
        WHERE CourseID=%s AND Semester=%s
        ORDER BY Score DESC
    """, (course_id, semester))
    result = cursor.fetchall()
    conn.close()
    return result

def query_all_scores():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT StudentID, CourseID, Semester, ScoreType, Score FROM Score")
    result = cursor.fetchall()
    conn.close()
    return result


# from db import get_connection

# # 添加成绩
# def add_score(id, course, score):
#     conn = get_connection()
#     cursor = conn.cursor()
#     # 先检查是否存在
#     cursor.execute("SELECT * FROM score WHERE ID=%s AND CourseName=%s", (id, course))
#     if cursor.fetchone():
#         print(f"学生 {id} 的课程 {course} 已存在成绩，跳过插入")
#         conn.close()
#         return
#     # 不存在则插入
#     sql = "INSERT INTO score (ID, CourseName, Score) VALUES (%s, %s, %s)"
#     cursor.execute(sql, (id, course, score))
#     conn.commit()
#     conn.close()

# # 查询某学生所有成绩
# def query_scores(id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     sql = "SELECT CourseName, Score FROM score WHERE ID=%s"
#     cursor.execute(sql, (id,))
#     result = cursor.fetchall()
#     conn.close()
#     return result

# # 修改成绩
# def update_score(id, course, score):
#     conn = get_connection()
#     cursor = conn.cursor()
#     sql = "UPDATE score SET Score=%s WHERE ID=%s AND CourseName=%s"
#     cursor.execute(sql, (score, id, course))
#     conn.commit()
#     conn.close()

# # 查询平均成绩
# def query_avg_score(id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     sql = "SELECT AvgScore FROM V_AvgScore WHERE ID=%s"
#     cursor.execute(sql, (id,))
#     result = cursor.fetchone()
#     conn.close()
#     return result
