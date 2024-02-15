import json
import os
import asyncio
import aiofiles


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        if not os.path.exists(db_file):
            with open(db_file, 'w') as f:
                json.dump({}, f)

    async def read_data(self):
        try:
            async with aiofiles.open(self.db_file, 'r') as f:
                data = await f.read()
                return json.loads(data) if data else {}
        except json.JSONDecodeError:
            # 如果解析出错，返回一个空的字典
            return {}

    async def write_data(self, data):
        async with aiofiles.open(self.db_file, 'w') as f:
            await f.write(json.dumps(data, indent=4))

    async def get(self, key):
        data = await self.read_data()
        keys = key.split('.')
        result = data
        for k in keys:
            if isinstance(result, dict):
                result = result.get(k, None)
            else:
                return None
        return result

    async def set(self, key, value):
        data = await self.read_data()
        keys = key.split('.')
        current = data
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
        await self.write_data(data)

    async def delete(self, key):
        data = await self.read_data()
        keys = key.split('.')
        current = data
        for k in keys[:-1]:
            if k not in current:
                return False
            current = current[k]
        if keys[-1] in current:
            del current[keys[-1]]
            await self.write_data(data)
            return True
        return False


# 示例用法 db=Database(jsonpath)
# async def process_data(db):
#     # 设置数据，将列表作为值存储在数据库中的一个键下
#     await db.set("person.names", ["Natsumi", "hsn8086", "-4"])
#
#     # 获取数据
#     names = await db.get("person.names")
#     print("Names:", names)
#
#     # 在列表中添加新元素
#     names.append("Ros")
#     await db.set("person.names", names)
#
#     # 再次获取数据，查看是否更新
#     updated_names = await db.get("person.names")
#     print("Names:", updated_names)
