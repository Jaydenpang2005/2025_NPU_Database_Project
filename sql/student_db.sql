/* ========================
   DATABASE
======================== */
DROP DATABASE IF EXISTS StudentDB;
CREATE DATABASE StudentDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;
USE StudentDB;


/* ========================
   TABLE: Class
======================== */
DROP TABLE IF EXISTS Class;

CREATE TABLE Class (
    -- 主键
    ClassID VARCHAR(20) PRIMARY KEY,
    ClassName VARCHAR(50) NOT NULL,
    Department VARCHAR(50),
    -- 约束：ClassID必须是7位纯数字
    CHECK (
        -- 约束：长度严格等于7位
        LENGTH(ClassID) = 7
        -- 约束：全部字符为数字
        AND ClassID REGEXP '^[0-9]{7}$'
    )
);


/* ========================
   TABLE: Student
======================== */
DROP TABLE IF EXISTS Student;

CREATE TABLE Student (
    -- 主键
    ID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Gender CHAR(2)
    -- 约束：限定性别只能是男或女
    CHECK (Gender IN ('男','女')),
    ClassID VARCHAR(20),
    -- 约束：学生ID必须是10位
    CHECK (LENGTH(ID) = 10),
    -- 约束：要求学生ID为10位纯数字
    CHECK (ID REGEXP '^[0-9]{10}$'),
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


/* ========================
   TABLE: Teacher
======================== */
DROP TABLE IF EXISTS Teacher;

CREATE TABLE Teacher (
    -- 主键
    TeacherID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Department VARCHAR(50),
    -- 约束：教师ID必须是5位
    CHECK (LENGTH(TeacherID) = 5),
    -- 约束：要求教师ID为5位纯数字
    CHECK (TeacherID REGEXP '^[0-9]{5}$')
);


/* ========================
   TABLE: Course
======================== */
DROP TABLE IF EXISTS Course;

CREATE TABLE Course (
    -- 主键
    CourseID VARCHAR(20) PRIMARY KEY,
    CourseName VARCHAR(50) NOT NULL,
    Credits INT DEFAULT 3,
    TeacherID VARCHAR(20),
    -- 约束：CourseID约束（6位，前两位CS/FN，后四位数字）
    CHECK (
        -- 约束：总长度6位
        LENGTH(CourseID) = 6
        -- 约束：前两位是CS或FN（大写）
        AND LEFT(CourseID, 2) IN ('CS', 'FN')
        -- 约束：后四位是数字
        AND RIGHT(CourseID, 4) REGEXP '^[0-9]{4}$'
    ),
    FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


/* ========================
   TABLE: Score
======================== */
DROP TABLE IF EXISTS Score;

CREATE TABLE Score (
    StudentID VARCHAR(20),
    CourseID VARCHAR(20),
    Semester VARCHAR(20) NOT NULL,
    ScoreType VARCHAR(20) DEFAULT '平时',
    Score INT,
    -- 复合主键
    PRIMARY KEY (StudentID, CourseID, Semester, ScoreType),
    -- 外键约束（级联删除/更新）
    FOREIGN KEY (StudentID) REFERENCES Student(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    -- 约束：分数范围约束（0-100）
    CHECK (Score BETWEEN 0 AND 100),
    -- 约束：限定 ScoreType 只能是 '平时' 或 '期末'
    CHECK (ScoreType IN ('平时', '期末')),
    -- 约束：限定 Semester 格式：xxxxy（xxxx为4位年份，y为春/夏/秋/冬）
    CHECK (
        -- 约束：字符长度必须为5位
        CHAR_LENGTH(Semester) = 5
        -- 约束：前4位为数字（年份）
        AND SUBSTRING(Semester, 1, 4) REGEXP '^[0-9]{4}$'
        -- 约束：第5位为春夏秋冬之一
        AND SUBSTRING(Semester, 5, 1) IN ('春', '夏', '秋', '冬')
    )
);


/* ========================
   VIEW: Average Score per student per semester
======================== */
DROP VIEW IF EXISTS V_AvgScore;

CREATE VIEW V_AvgScore AS
SELECT 
    StudentID,
    Semester,
    AVG(Score) AS AvgScore
FROM Score
GROUP BY StudentID, Semester;


/* ========================
   TRIGGER: validate score range（触发器）
======================== */
DROP TRIGGER IF EXISTS trg_score_insert;

DELIMITER $$

CREATE TRIGGER trg_score_insert
BEFORE INSERT ON Score
FOR EACH ROW
-- 约束：分数范围约束（0-100）
BEGIN
    IF NEW.Score < 0 OR NEW.Score > 100 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Score must be between 0 and 100';
    END IF;
END$$

DELIMITER ;


-- ========================
-- INDEXES (物理设计)
-- ========================
CREATE INDEX idx_student_class ON Student(ClassID);
CREATE INDEX idx_score_course_semester ON Score(CourseID, Semester);
CREATE INDEX idx_score_student_semester ON Score(StudentID, Semester);
CREATE INDEX idx_course_teacher ON Course(TeacherID);


/* ========================
   SAMPLE DATA
======================== */

-- Classes
INSERT INTO Class VALUES
('1012305','计算机一班','计算机系'),
('1012406','计算机二班','计算机系');

-- Students
INSERT INTO Student VALUES
('2024475947','张三','男','1012305'),
('2025085833','李四','女','1012406'),
('2026548634','王五','男','1012305');

-- Teachers
INSERT INTO Teacher VALUES
('20021','赵老师','计算机系'),
('18012','钱老师','计算机系');

-- Courses
INSERT INTO Course VALUES
('CS1011','数据库',3,'20021'),
('CS1024','操作系统',3,'18012'),
('CS1038','计算机网络',3,'20021');

-- Scores
INSERT INTO Score VALUES
('2024475947','CS1011','2025春','平时',85),
('2024475947','CS1024','2025春','期末',90),
('2025085833','CS1011','2025春','平时',78),
('2026548634','CS1038','2025春','期末',92);
