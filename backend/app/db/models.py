from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy 基类：所有 ORM 模型继承此类
# 注意：此处的 Base 是数据库层基类（用于 db/session 等基础设施），
# 业务模型定义在 app/models/ 下各自的文件中（user/token/admin 等），
# 两者通过 app.models.base 共享同一 Base，不存在重复定义。
Base = declarative_base()