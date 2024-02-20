# import asyncio
import motor.motor_asyncio


class DB:
    def __init__(self, uri, db_name, username=None, password=None):
        """
        初始化数据库连接。
        :param uri: 数据库URI
        :param db_name: 数据库名称
        :param username: 用户名（可选）
        :param password: 密码（可选）
        """
        if username and password:
            uri = f"mongodb://{username}:{password}@{uri}"
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def insert(self, collection, data):
        """
        在指定的集合中插入数据。
        :param collection: 集合名称
        :param data: 要插入的数据
        :return: 插入的数据的ID
        """
        result = await self.db[collection].insert_one(data)
        return result.inserted_id

    async def find(self, collection, query, page=1, limit=100):
        """
        在指定的集合中查找数据。
        :param collection: 集合名称
        :param query: 查询条件
        :param page: 页码（默认为1）
        :param limit: 每页的数据量（默认为100）
        :return: 查询结果列表
        """
        skip = (page - 1) * limit
        cursor = self.db[collection].find(query).skip(skip).limit(limit)
        result = await cursor.to_list(length=limit)
        return result

    async def update(self, collection, query, field, new_value):
        """
        更新指定集合中的数据。
        :param collection: 集合名称
        :param query: 查询条件
        :param field: 要更新的字段
        :param new_value: 新的值
        :return: 被修改的数据数量
        """
        result = await self.db[collection].update_one(query, {"$set": {field: new_value}})
        return result.modified_count

#
# async def example():
#     # 创建一个DB对象，连接到你的数据库
#     db = DB(uri="localhost:27017", db_name="user")
#
#     # 插入一条数据到"users"集合
#     user_data = {"name": "Natsumi", "email": "unknown@unknown.com"}
#     insert_result = await db.insert("users", user_data)
#     print(f"替换ID {insert_result}")
#
#     # 查找"users"集合中的所有数据
#     find_result = await db.find("users", {})
#     print(f"数据: {find_result}")
#
#     # 更新"users"集合中的一条数据
#     update_result = await db.update("users", {"name": "Natsumi"}, "email", "new_em1121ail@example.com")
#     update_result = await db.update("users", {"name": "Natsumi"}, "email1", "new_em1121ail@example.com")
#     update_result = await db.update("users", {"name": "Natsumi"}, "email1", {"address": "beihai"})
#     update_result = await db.update("users", {"name": "Natsumi"}, "email1.address", "nanning")
#     update_result = await db.update("users", {"name": "Natsumi"}, "a", "b")
#     print(f"更新 {update_result} 数据")
#
#     # 获取"users"集合中的第1页数据，每页有10条数据
#     page_result = await db.find("users", {}, page=1, limit=10)
#     print(f"数据: {page_result}")
#
#
# asyncio.run(example())
