
from sqlalchemy import create_engine
from base import DB_URI

engine = create_engine(DB_URI)  # 创建引擎
conn = engine.connect()  # 连接
result = conn.execute('SELECT 1')  # 执行SQL
print(result.fetchone())
conn.close()  # 关闭连接