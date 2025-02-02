# config.py
import os

# LOCALHOST
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "Kaustubh1")
MYSQL_DB = os.environ.get("MYSQL_DB", "setu")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

