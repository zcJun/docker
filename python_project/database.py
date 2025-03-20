from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import contextmanager
import logging
from logging.handlers import TimedRotatingFileHandler


# 日志配置
log_handler = TimedRotatingFileHandler(
    'mysql_log.log', when='midnight', interval=1, backupCount=7, encoding='utf-8'
)
log_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


"""
MySQL数据库操作类,提供各种数据库操作方法
"""
class MySQLServer:
    def __init__(self):
        # 创建同步引擎
        self.engine = create_engine(
            "mysql+pymysql://root:root@127.0.0.1:3306/test",
            pool_pre_ping=True,  # 自动检测连接是否有效
            pool_recycle=3600,   # 一小时后回收连接
            echo=True            # SQL日志是否输出
        )
        
        # 创建会话工厂
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_db(self):
        """
        获取数据库会话的上下文管理器
        @returns {Session} 数据库会话对象
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def log_query(query_str: str, params: dict):
        # 创建一个副本以避免修改原参数
        params_copy = params.copy()
        for key in params_copy.keys():
            # 替换冒号开头的命名参数
            query_str = query_str.replace(f":{key}", str(params_copy[key]))
        return query_str

    def _log_sql(self, sql_query: str, params: Dict = {}, success: bool = True) -> None:
        """
        记录SQL执行日志
        @param {str} sql_query - 执行的SQL语句
        @param {Dict} params - 执行参数
        @param {bool} success - 执行是否成功
        """
        if success:
            compiled_sql = text(sql_query).bindparams(**(params or {})).compile(dialect=self.engine.dialect, compile_kwargs={"literal_binds": True})
            logger.info(f"执行成功: {sql_query} | 参数: {params} | 执行结果: {compiled_sql}")
        else:
            compiled_sql = text(sql_query).bindparams(**(params or {})).compile(dialect=self.engine.dialect, compile_kwargs={"literal_binds": True})
            logger.error(f"执行失败: {sql_query} | 参数: {params} | 执行结果: {compiled_sql}")

    def query(self, sql_query: str, params: Dict = None) -> List[Dict]:
        """
        执行查询并返回所有结果
        @param sql_query: SQL查询语句
        @param params: 查询参数
        @returns 查询结果列表
        """
        try:
            with self.get_db() as db:
                result = db.execute(text(sql_query), params or {})
                columns = result.keys()
                self._log_sql(sql_query, params, success=True)
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 query: {str(e)}", exc_info=False)
            raise

    def get_row(self, sql_query: str, params: Dict = None) -> Optional[Dict]:
        """
        执行查询并返回单条记录
        @param {str} sql_query - SQL查询语句
        @param {Dict} params - 查询参数
        @returns {Optional[Dict]} 单条记录或None
        """
        try:
            with self.get_db() as db:
                result = db.execute(text(sql_query), params or {})
                self._log_sql(sql_query, params, success=True)
                row = result.fetchone()
                return dict(zip(result.keys(), row)) if row else None
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 get_row: {str(e)}", exc_info=False)
            raise

    def get_var(self, sql_query: str, params: Dict = None) -> Any:
        """
        执行查询并返回单个值
        @param {str} sql_query - SQL查询语句
        @param {Dict} params - 查询参数
        @returns {Any} 查询结果值
        """
        try:
            with self.get_db() as db:
                result = db.execute(text(sql_query), params or {})
                self._log_sql(sql_query, params, success=True)
                row = result.first()
                return row[0] if row else None
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 get_var: {str(e)}", exc_info=False)
            raise

    def execute(self, sql_query: str, params: Dict = None) -> int:
        """
        执行更新操作
        @param {str} sql_query - SQL更新语句
        @param {Dict} params - 更新参数
        @returns {int} 更新记录的ID
        """
        try:
            with self.get_db() as db:
                result = db.execute(text(sql_query), params or {})
                self._log_sql(sql_query, params, success=True)
                db.commit()
                return result.rowcount
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 execute: {str(e)}", exc_info=False)
            raise

    def executemany(self, sql_query: str, params_list: List[Dict]) -> int:
        """
        执行批量更新操作
        @param {str} sql_query - SQL批量更新语句
        @param {List[Dict]} params_list - 批量更新参数列表
        @returns {int} 更新记录的ID
        """
        try:
            with self.get_db() as db:
                result = db.execute(text(sql_query), params_list)
                for params in params_list:
                    self._log_sql(sql_query, params, success=True)
                db.commit()
                return result.rowcount
        except Exception as e:
            for params in params_list:
                self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 executemany: {str(e)}", exc_info=False)
            raise

    def insert_id(self, sql_query: str, params: Dict = None) -> int:
        """
        执行插入操作并返回插入的ID
        @param {str} sql_query - SQL插入语句
        @param {Dict} params - 插入参数
        @returns {int} 插入记录的ID
        """
        try:
            with self.get_db() as db:
                result = db.execute(text(sql_query), params or {})
                self._log_sql(sql_query, params, success=True)
                db.commit()
                return result.lastrowid
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 insert_id: {str(e)}", exc_info=False)
            raise
        
    def page_and_size(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        生成分页SQL片段及相关信息
        @param {int} page - 当前页码（从1开始，默认1）
        @param {int} page_size - 每页条数（默认10）
        @returns {Dict[str, Any]} 分页参数字典
        """
        if page < 1 or page_size < 1:
            raise ValueError("页码和每页条数必须大于0")
        offset = (page - 1) * page_size
        return {
            "limit": page_size,
            "offset": offset,
            "page": page,
            "page_size": page_size
        }

    def query_in(self, sql_query: str, param_name: str, values: tuple, 
                 other_conditions: Dict[str, Any] = None) -> List[Dict]:
        """
        专门处理IN查询的SQL执行方法，同时支持其他WHERE条件
        @param {str} sql_query - SQL查询语句
        @param {str} param_name - IN子句参数名
        @param {tuple} values - IN子句值元组
        @param {Dict[str, Any]} other_conditions - 其他WHERE条件参数
        @returns {List[Dict]} 查询结果列表
        """
        try:
            with self.get_db() as db:
                params = {param_name: values}
                if other_conditions:
                    params.update(other_conditions)
                result = db.execute(text(sql_query), params)
                self._log_sql(sql_query, params, success=True)
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            self._log_sql(sql_query, params, success=False)
            logger.error(f"发生错误 query_in: {str(e)}", exc_info=False)
            raise

# 创建全局实例
mysql_server = MySQLServer()