# class.py
from db import get_connection

# 添加班级
def add_class(class_id, class_name, department=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Class WHERE ClassID=%s", (class_id,))
    if cursor.fetchone():
        conn.close()
        print(f"班级 {class_id} 已存在")
        return
    cursor.execute("INSERT INTO Class (ClassID, ClassName, Department) VALUES (%s,%s,%s)", (class_id, class_name, department))
    conn.commit()
    conn.close()

# 删除班级
def delete_class(class_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Class WHERE ClassID=%s", (class_id,))
    conn.commit()
    conn.close()

# 修改班级
def update_class(class_id, class_name=None, department=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE Class SET "
    params=[]
    if class_name:
        sql += "ClassName=%s,"
        params.append(class_name)
    if department:
        sql += "Department=%s,"
        params.append(department)
    sql = sql.rstrip(',') + " WHERE ClassID=%s"
    params.append(class_id)
    cursor.execute(sql, tuple(params))
    conn.commit()
    conn.close()

# 查询班级信息
def query_class(class_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Class WHERE ClassID=%s", (class_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# 查询班级平均成绩
def query_class_avg_score(class_id, semester=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT AVG(s.Score) as AvgScore
        FROM Score s
        JOIN Student st ON s.StudentID = st.ID
        WHERE st.ClassID=%s
    """
    params = [class_id]
    if semester:
        sql += " AND s.Semester=%s"
        params.append(semester)
    cursor.execute(sql, tuple(params))
    result = cursor.fetchone()
    conn.close()
    return result

def query_all_classes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ClassID, ClassName, Department FROM Class")
    result = cursor.fetchall()
    conn.close()
    return result