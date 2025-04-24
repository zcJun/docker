from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import logging
from logging.handlers import TimedRotatingFileHandler
from sqlalchemy import text

# 日志配置
log_handler = TimedRotatingFileHandler(
    'async_mysql_log.log', when='midnight', interval=1, backupCount=7, encoding='utf-8'
)
log_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


class AsyncMySQLServer:
    def __init__(self):
        # 创建异步引擎
        self.engine = create_async_engine(
            "mysql+aiomysql://root:root@127.0.0.1:3306/test",
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=True
        )
        
        # 创建异步会话工厂
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession)

    @asynccontextmanager
    async def get_db(self):
        """
        获取数据库会话的异步上下文管理器
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            await db.close()

    def _log_sql(self, sql_query: str, params: Dict = {}, success: bool = True) -> None:
        if success:
            compiled_sql = text(sql_query).bindparams(**(params or {})).compile(dialect=self.engine.dialect, compile_kwargs={"literal_binds": True})
            logger.info(f"执行成功: {sql_query} | 参数: {params} | 执行结果: {compiled_sql}")
        else:
            compiled_sql = text(sql_query).bindparams(**(params or {})).compile(dialect=self.engine.dialect, compile_kwargs={"literal_binds": True})
            logger.error(f"执行失败: {sql_query} | 参数: {params} | 执行结果: {compiled_sql}")

    async def query(self, sql_query: str, params: Dict = None) -> List[Dict]:
        try:
            async with self.get_db() as db:
                result = await db.execute(text(sql_query), params or {})
                columns = result.keys()
                self._log_sql(sql_query, params, success=True)
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 async_query: {str(e)}", exc_info=False)
            raise

    async def get_row(self, sql_query: str, params: Dict = None) -> Optional[Dict]:
        try:
            async with self.get_db() as db:
                result = await db.execute(text(sql_query), params or {})
                self._log_sql(sql_query, params, success=True)
                row = result.fetchone()
                return dict(zip(result.keys(), row)) if row else None
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 async_get_row: {str(e)}", exc_info=False)
            raise

    async def get_var(self, sql_query: str, params: Dict = None) -> Any:
        try:
            async with self.get_db() as db:
                result = await db.execute(text(sql_query), params or {})
                self._log_sql(sql_query, params, success=True)
                row = result.first()
                return row[0] if row else None
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 async_get_var: {str(e)}", exc_info=False)
            raise

    async def execute(self, sql_query: str, params: Dict = None) -> int:
        try:
            async with self.get_db() as db:
                result = await db.execute(text(sql_query), params or {})
                self._log_sql(sql_query, params, success=True)
                await db.commit()
                return result.rowcount
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 async_execute: {str(e)}", exc_info=False)
            raise

    async def executemany(self, sql_query: str, params_list: List[Dict]) -> int:
        try:
            async with self.get_db() as db:
                result = await db.execute(text(sql_query), params_list)
                for params in params_list:
                    self._log_sql(sql_query, params, success=True)
                await db.commit()
                return result.rowcount
        except Exception as e:
            for params in params_list:
                self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 async_executemany: {str(e)}", exc_info=False)
            raise

    async def insert_id(self, sql_query: str, params: Dict = None) -> int:
        try:
            async with self.get_db() as db:
                result = await db.execute(text(sql_query), params or {})
                self._log_sql(sql_query, params, success=True)
                await db.commit()
                return result.lastrowid
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 async_insert_id: {str(e)}", exc_info=False)
            raise

    async def page_and_size(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        if page < 1 or page_size < 1:
            raise ValueError("页码和每页条数必须大于0")
        offset = (page - 1) * page_size
        return {
            "limit": page_size,
            "offset": offset,
            "page": page,
            "page_size": page_size
        }

    async def query_in(self, sql_query: str, param_name: str, values: tuple, other_conditions: Dict[str, Any] = None) -> List[Dict]:
        try:
            async with self.get_db() as db:
                params = {param_name: values}
                if other_conditions:
                    params.update(other_conditions)
                result = await db.execute(text(sql_query), params)
                self._log_sql(sql_query, params, success=True)
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 async_query_in: {str(e)}", exc_info=False)
            raise

# 创建全局实例
async_mysql_server = AsyncMySQLServer()