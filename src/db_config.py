import json
import os

def load_db_config():
    """
    读取数据库配置文件
    :return: 数据库连接参数字典
    :raises: FileNotFoundError, json.JSONDecodeError, KeyError
    """
    # 配置文件路径（和当前脚本同目录）
    config_path = os.path.join(os.path.dirname(__file__), "../config.json")
    
    # 检查配置文件是否存在
    if not os.path.exists(config_path):
        # 若不存在，创建默认配置文件
        default_config = {
            "database": {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "StudentDB",
                "charset": "utf8mb4"
            }
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        print(f"配置文件不存在，已创建默认配置：{config_path}")
        return default_config["database"]
    
    # 读取并解析配置文件
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        # 校验必要的配置项
        required_keys = ["host", "user", "password", "database", "charset"]
        for key in required_keys:
            if key not in config["database"]:
                raise KeyError(f"配置文件缺少必要字段：{key}")
        return config["database"]
    except json.JSONDecodeError as e:
        raise Exception(f"配置文件格式错误（JSON解析失败）：{str(e)}")
    except KeyError as e:
        raise Exception(f"配置文件内容错误：{str(e)}")