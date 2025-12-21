"""
check.py - 数据库表前置约束校验工具
所有函数严格对齐数据库表的CHECK约束，提前拦截无效数据
函数规则：
- 核心校验函数：check_xxx(字段1, 字段2, ...) -> (bool, str)
  - 返回值1：是否通过校验（True/False）
  - 返回值2：校验结果描述（空字符串=通过，非空=错误信息）
- 简化版函数：check_xxx_simple(...) -> bool（仅返回是否通过）
"""
import re

# ======================== Class 表约束校验 ========================
def check_class(class_id, class_name, department=None):
    """
    校验班级表数据约束
    :param class_id: 班级ID（必填）
    :param class_name: 班级名称（必填）
    :param department: 所属院系（可选）
    :return: (bool, str) - (是否通过, 错误信息)
    """
    # 1. 班级ID校验：7位纯数字
    if not class_id:
        return False, "班级ID不能为空"
    if len(class_id) != 7:
        return False, f"班级ID必须是7位数字（当前：{len(class_id)}位）"
    if not class_id.isdigit():
        return False, f"班级ID必须是纯数字（当前：{class_id}）"
    
    # 2. 班级名称校验：非空
    if not class_name or not class_name.strip():
        return False, "班级名称不能为空"
    
    # 所有校验通过
    return True, ""

def check_class_simple(class_id, class_name, department=None):
    """简化版：仅返回是否通过校验"""
    return check_class(class_id, class_name, department)[0]

# ======================== Student 表约束校验 ========================
def check_student(student_id, name, gender, class_id=None):
    """
    校验学生表数据约束
    :param student_id: 学生ID（必填）
    :param name: 学生姓名（必填）
    :param gender: 性别（必填）
    :param class_id: 班级ID（可选）
    :return: (bool, str) - (是否通过, 错误信息)
    """
    # 1. 学生ID校验：10位纯数字
    if not student_id:
        return False, "学生ID不能为空"
    if len(student_id) != 10:
        return False, f"学生ID必须是10位数字（当前：{len(student_id)}位）"
    if not student_id.isdigit():
        return False, f"学生ID必须是纯数字（当前：{student_id}）"
    
    # 2. 姓名校验：非空
    if not name or not name.strip():
        return False, "学生姓名不能为空"
    
    # 3. 性别校验：只能是男/女
    if gender not in ["男", "女"]:
        return False, f"性别必须是'男'或'女'（当前：{gender}）"
    
    # 4. 班级ID校验（若填写）：需符合ClassID约束（7位纯数字）
    if class_id:
        class_valid, class_err = check_class_simple(class_id, "临时名称"), check_class(class_id, "临时名称")[1]
        if not class_valid:
            return False, f"班级ID不符合规则：{class_err}"
    
    # 所有校验通过
    return True, ""

def check_student_simple(student_id, name, gender, class_id=None):
    """简化版：仅返回是否通过校验"""
    return check_student(student_id, name, gender, class_id)[0]

# ======================== Teacher 表约束校验 ========================
def check_teacher(teacher_id, name, department=None):
    """
    校验教师表数据约束
    :param teacher_id: 教师ID（必填）
    :param name: 教师姓名（必填）
    :param department: 所属院系（可选）
    :return: (bool, str) - (是否通过, 错误信息)
    """
    # 1. 教师ID校验：5位纯数字
    if not teacher_id:
        return False, "教师ID不能为空"
    if len(teacher_id) != 5:
        return False, f"教师ID必须是5位数字（当前：{len(teacher_id)}位）"
    if not teacher_id.isdigit():
        return False, f"教师ID必须是纯数字（当前：{teacher_id}）"
    
    # 2. 姓名校验：非空
    if not name or not name.strip():
        return False, "教师姓名不能为空"
    
    # 所有校验通过
    return True, ""

def check_teacher_simple(teacher_id, name, department=None):
    """简化版：仅返回是否通过校验"""
    return check_teacher(teacher_id, name, department)[0]

# ======================== Course 表约束校验 ========================
def check_course(course_id, course_name, credits=3, teacher_id=None):
    """
    校验课程表数据约束
    :param course_id: 课程ID（必填）
    :param course_name: 课程名称（必填）
    :param credits: 学分（可选，默认3）
    :param teacher_id: 教师ID（可选）
    :return: (bool, str) - (是否通过, 错误信息)
    """
    # 1. 课程ID校验：6位（前两位CS/FN + 后四位数字）
    if not course_id:
        return False, "课程ID不能为空"
    if len(course_id) != 6:
        return False, f"课程ID必须是6位（当前：{len(course_id)}位）"
    
    # 前两位校验：CS/FN（大写）
    course_prefix = course_id[:2]
    if course_prefix not in ["CS", "FN"]:
        return False, f"课程ID前两位必须是'CS'或'FN'（当前：{course_prefix}）"
    
    # 后四位校验：纯数字
    course_suffix = course_id[2:]
    if not course_suffix.isdigit():
        return False, f"课程ID后四位必须是纯数字（当前：{course_suffix}）"
    
    # 2. 课程名称校验：非空
    if not course_name or not course_name.strip():
        return False, "课程名称不能为空"
    
    # 3. 学分校验：整数（默认3，无范围约束，若需可补充）
    if not isinstance(credits, int):
        return False, f"学分必须是整数（当前：{credits}）"
    
    # 4. 教师ID校验（若填写）：需符合TeacherID约束（5位纯数字）
    if teacher_id:
        teacher_valid, teacher_err = check_teacher(teacher_id, "临时名称")[0], check_teacher(teacher_id, "临时名称")[1]
        if not teacher_valid:
            return False, f"教师ID不符合规则：{teacher_err}"
    
    # 所有校验通过
    return True, ""

def check_course_simple(course_id, course_name, credits=3, teacher_id=None):
    """简化版：仅返回是否通过校验"""
    return check_course(course_id, course_name, credits, teacher_id)[0]

# ======================== Score 表约束校验 ========================
def check_score(student_id, course_id, semester, score_type="平时", score=None):
    """
    校验成绩表数据约束
    :param student_id: 学生ID（必填）
    :param course_id: 课程ID（必填）
    :param semester: 学期（必填，格式：xxxxy，如2025春）
    :param score_type: 成绩类型（可选，默认平时）
    :param score: 分数（必填）
    :return: (bool, str) - (是否通过, 错误信息)
    """
    # 1. 学生ID校验：符合StudentID约束（10位纯数字）
    if not student_id:
        return False, "学生ID不能为空"
    student_valid, student_err = check_student(student_id, "临时姓名", "男")[0], check_student(student_id, "临时姓名", "男")[1]
    if not student_valid:
        return False, f"学生ID不符合规则：{student_err}"
    
    # 2. 课程ID校验：符合CourseID约束（6位CS/FN+数字）
    if not course_id:
        return False, "课程ID不能为空"
    course_valid, course_err = check_course(course_id, "临时课程")[0], check_course(course_id, "临时课程")[1]
    if not course_valid:
        return False, f"课程ID不符合规则：{course_err}"
    
    # 3. 学期校验：xxxxy（5字符，前4位数字，第5位春/夏/秋/冬）
    if not semester:
        return False, "学期不能为空"
    if len(semester) != 5:  # CHAR_LENGTH等价于len（中文1字符）
        return False, f"学期格式必须是'xxxxy'（5位，当前：{len(semester)}位）"
    
    # 前4位：年份（纯数字）
    semester_year = semester[:4]
    if not semester_year.isdigit():
        return False, f"学期前4位必须是年份数字（当前：{semester_year}）"
    
    # 第5位：季节（春/夏/秋/冬）
    semester_season = semester[4]
    if semester_season not in ["春", "夏", "秋", "冬"]:
        return False, f"学期第5位必须是'春/夏/秋/冬'（当前：{semester_season}）"
    
    # 4. 成绩类型校验：平时/期末
    if score_type not in ["平时", "期末"]:
        return False, f"成绩类型必须是'平时'或'期末'（当前：{score_type}）"
    
    # 5. 分数校验：0-100整数
    if score is None:
        return False, "分数不能为空"
    if not isinstance(score, int):
        return False, f"分数必须是整数（当前：{score}）"
    if score < 0 or score > 100:
        return False, f"分数必须在0-100之间（当前：{score}）"
    
    # 所有校验通过
    return True, ""

def check_score_simple(student_id, course_id, semester, score_type="平时", score=None):
    """简化版：仅返回是否通过校验"""
    return check_score(student_id, course_id, semester, score_type, score)[0]

# ======================== 测试用例（可选） ========================
if __name__ == "__main__":
    # 测试Class校验
    print("=== 测试Class校验 ===")
    print(check_class("1234567", "计算机2025级1班"))  # (True, '')
    print(check_class("123456", "计算机2025级1班"))   # (False, '班级ID必须是7位数字（当前：6位）')
    
    # 测试Student校验
    print("\n=== 测试Student校验 ===")
    print(check_student("2024475947", "张三", "男", "1234567"))  # (True, '')
    print(check_student("202447594", "张三", "男", "1234567"))   # (False, '学生ID必须是10位数字（当前：9位）')
    
    # 测试Course校验
    print("\n=== 测试Course校验 ===")
    print(check_course("CS1011", "Python编程"))  # (True, '')
    print(check_course("FS1011", "Python编程"))  # (False, '课程ID前两位必须是'CS'或'FN'（当前：FS）')
    
    # 测试Score校验
    print("\n=== 测试Score校验 ===")
    print(check_score("2024475947", "CS1011", "2025春", "平时", 85))  # (True, '')
    print(check_score("2024475947", "CS1011", "2025春季", "平时", 85))  # (False, '学期格式必须是'xxxxy'（5位，当前：6位）')