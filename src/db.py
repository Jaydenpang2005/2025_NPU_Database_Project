# db.py
import pymysql
from db_config import load_db_config  # 导入配置读取函数

def get_connection():
    """
    获取数据库连接（从config.json读取配置）
    :return: pymysql.Connection 对象
    :raises: pymysql.MySQLError, Exception
    """
    try:
        # 加载配置
        db_config = load_db_config()
        # 创建连接
        conn = pymysql.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            charset=db_config["charset"]
        )
        return conn
    except pymysql.MySQLError as e:
        raise Exception(f"数据库连接失败：{str(e)}")
    except Exception as e:
        raise Exception(f"获取连接失败：{str(e)}")

# 测试连接（可选）
if __name__ == "__main__":
    try:
        conn = get_connection()
        print("数据库连接成功！")
        conn.close()
    except Exception as e:
        print(f"连接失败：{str(e)}")
