from fastapi import FastAPI, HTTPException
from database import MySQLServer
from async_database import AsyncMySQLServer
app = FastAPI()

my_sql_server = MySQLServer()
async_mysql_server = AsyncMySQLServer()

@app.get("/test1")
async def get_users():
    """
    获取所有用户信息
    @returns {dict} 用户列表
    """
    try:
        # 调用 MySQLServer 的 query 方法获取用户信息
        # result = my_sql_server.query("SELECT * FROM users1")
        result = my_sql_server.query("SELECT * FROM users WHERE id = :id", {"id": 98})
        
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败")

@app.get("/test2")
async def get_row():
    """
    获取单条记录
    """
    try:
        result = my_sql_server.get_row("SELECT * FROM users WHERE id = :id", {"id": 98})
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败")

@app.get("/test3")
async def get_var():
    """
    获取单个值
    """
    try:
        result = my_sql_server.get_var("SELECT name FROM users WHERE id = :id", {"id": 98})
        return {
            "code": 200,
            "message": "success",
            "data": {"name": result}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败")

@app.get("/test4")
async def execute():
    """
    执行SQL语句
    """
    try:
        result = my_sql_server.execute("UPDATE users SET name = :name WHERE id = :id", {"id": 98, "name": "test"})
        return {
            "code": 200,
            "message": "success",
            "data": {"count": result}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败")
@app.get("/test5")
async def executemany():
    """
    执行批量SQL语句
    """
    try:
        # # 调用 executemany 方法执行批量更新操作
        # result = my_sql_server.executemany("UPDATE users SET name = :name WHERE id = :id", 
        #                                     [{"id": 98, "name": "test11"}, 
        #                                      {"id": 97, "name": "test22"}])

        # 批量插入
        result = my_sql_server.executemany("INSERT INTO users (name, age) VALUES (:name, :age)", 
                                            [{"name": "test1111", "age": 18}, 
                                             {"name": "test2222", "age": 17}])
        return {
            "code": 200,
            "message": "success",
            "data": {"count": result}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败")

@app.get("/test6")
async def insert_id():
    """
    执行插入操作并返回插入的ID
    """
    try:
        result = my_sql_server.insert_id("INSERT INTO users (name, age) VALUES (:name, :age)", 
                                          {"name": "test3333", "age": 16})
        return {
            "code": 200,
            "message": "success",
            "data": {"id": result}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败")
    
@app.get("/test7/{page}")
async def page_and_size(page: int = 1):
    """
    生成分页SQL片段及相关信息
    """
    try:
        result = my_sql_server.page_and_size(page=page, page_size=5)
        result = my_sql_server.query("SELECT * FROM users LIMIT :limit OFFSET :offset", {"limit": result["limit"], "offset": result["offset"]})
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败")


@app.get("/async_test1")
async def get_users():
    """
    获取所有用户信息
    @returns {dict} 用户列表
    """
    try:
        # 调用 MySQLServer 的 query 方法获取用户信息
        # result = my_sql_server.query("SELECT * FROM users1")
        result =  await async_mysql_server.query("SELECT * FROM users WHERE id = :id", {"id": 98})
        
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败")

@app.get("/async_test2")
async def get_row():
    """
    获取单条记录
    """
    try:
        result = await async_mysql_server.get_row("SELECT * FROM users WHERE id = :id", {"id": 98})
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败")

@app.get("/async_test3")
async def get_var():
    """
    获取单个值
    """
    try:
        result = await async_mysql_server.get_var("SELECT name FROM users WHERE id = :id", {"id": 98})
        return {
            "code": 200,
            "message": "success",
            "data": {"name": result}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败")

@app.get("/async_test4")
async def execute():
    """
    执行SQL语句
    """
    try:
        result = await async_mysql_server.execute("UPDATE users SET name = :name WHERE id = :id", {"id": 98, "name": "test"})
        return {
            "code": 200,
            "message": "success",
            "data": {"count": result}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败")
@app.get("/async_test5")
async def executemany():
    """
    执行批量SQL语句
    """
    try:
        # # 调用 executemany 方法执行批量更新操作
        # result = await async_mysql_server.executemany("UPDATE users SET name = :name WHERE id = :id", 
        #                                     [{"id": 98, "name": "test11"}, 
        #                                      {"id": 97, "name": "test22"}])

        # 批量插入
        result = await async_mysql_server.executemany("INSERT INTO users (name, age) VALUES (:name, :age)", 
                                            [{"name": "test1111", "age": 18}, 
                                             {"name": "test2222", "age": 17}])
        return {
            "code": 200,
            "message": "success",
            "data": {"count": result}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败")

@app.get("/async_test6")
async def insert_id():
    """
    执行插入操作并返回插入的ID
    """
    try:
        result = await async_mysql_server.insert_id("INSERT INTO users (name, age) VALUES (:name, :age)", 
                                          {"name": "test3333", "age": 16})
        return {
            "code": 200,
            "message": "success",
            "data": {"id": result}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败")
    
@app.get("/async_test7/{page}")
async def page_and_size(page: int = 1):
    """
    生成分页SQL片段及相关信息
    """
    try:
        result = await async_mysql_server.page_and_size(page=page, page_size=5)
        result = await async_mysql_server.query("SELECT * FROM users LIMIT :limit OFFSET :offset", {"limit": result["limit"], "offset": result["offset"]})
        return {
            "code": 200,
            "message": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败")
    


@app.get("/redis_test")
async def test_redis_connection():
    """
    测试Redis连接和基本操作
    @returns {dict} Redis操作结果
    """
    try:
        from async_redis import async_redis_server
        
        # 使用异步上下文管理器获取Redis连接
        async with async_redis_server.get_redis() as redis:
            # 设置测试键值对
            await redis.set('test_key', 'hello_world', ex=30)
            
            # 获取测试值
            result = await redis.get('test_key')
            
            return {
                "code": 200,
                "message": "success",
                "data": {
                    "key": "test_key",
                    "value": result
                }
            }
    except Exception as e:
        # 记录错误日志
        raise HTTPException(status_code=500, detail=f"Redis操作失败: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10011)
