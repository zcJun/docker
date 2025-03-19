#!/bin/bash

# 定义所有目录
BASE_DIR=/data
MYSQL_DIR=${BASE_DIR}/mysql1
DATA_DIR=${MYSQL_DIR}/data    # 数据目录
CONF_DIR=${MYSQL_DIR}/conf    # 配置目录
LOG_DIR=${MYSQL_DIR}/log      # 日志目录

# 一次性创建所有目录
echo "创建所有目录..."
mkdir -p ${DATA_DIR} ${CONF_DIR} ${LOG_DIR} || { echo "创建失败！"; exit 1; }

# 设置目录权限（改为 755）
echo "设置目录权限..."
chmod 755 ${DATA_DIR} || { echo "设置 data 权限失败！"; exit 1; }
chmod 755 ${CONF_DIR} || { echo "设置 conf 权限失败！"; exit 1; }
chmod 755 ${LOG_DIR} || { echo "设置 log 权限失败！"; exit 1; }

# 如果系统启用了 SELinux，设置上下文
if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled; then
    echo "检测到 SELinux 已启用，设置上下文..."
    chcon -Rt container_file_t ${MYSQL_DIR} || { echo "设置 SELinux 上下文失败！"; exit 1; }
fi

echo "目录创建和权限设置完成！"


# 创建 my.cnf 文件
MYSQL_CONF=${CONF_DIR}/my.cnf
cat <<EOF > ${MYSQL_CONF}
[mysqld]
# 字符集和排序规则
character-set-server=utf8mb4
collation-server=utf8mb4_general_ci

# 默认存储引擎
default-storage-engine=InnoDB

# InnoDB 缓冲池大小
innodb_buffer_pool_size=128M

# 最大连接数
max_connections=100

# 数据和临时文件路径
datadir=/var/lib/mysql
tmpdir=/tmp

# 超时时间
wait_timeout=600

# 临时表和排序缓冲区
max_tmp_tables=32
max_sort_length=1M

# 服务绑定地址，允许任意IP连接（可以根据需要更改为特定IP）
bind-address=0.0.0.0

# 错误日志（已启用）
log-error=/var/log/mysql/error.log
log-error-verbosity=2  # 记录错误和警告

# 通用查询日志
general_log=1  # 开启通用日志
general_log_file=/var/log/mysql/general.log  # 日志文件路径

# 慢查询日志
slow_query_log=1  # 开启慢查询日志
slow_query_log_file=/var/log/mysql/slow.log  # 日志文件路径
long_query_time=2  # 超过 2 秒的查询记录为慢查询
log_slow_admin_statements=1  # 记录慢的管理语句（如 ALTER TABLE）
log_queries_not_using_indexes=1  # 记录未使用索引的查询

# 二进制日志
log_bin=/var/log/mysql/mysql-bin.log  # 开启二进制日志并指定路径
binlog_format=ROW  # 使用 ROW 格式，适合复制和恢复
expire_logs_days=7  # 二进制日志保留 7 天，防止磁盘占满
max_binlog_size=100M  # 每个二进制日志文件最大 100MB

[client]
# 客户端字符集
default-character-set=utf8mb4

# 连接超时和最大数据包
connect-timeout=30
max_allowed_packet=16M

# 初始化连接字符集
init-connect='SET NAMES utf8mb4 COLLATE utf8mb4_general_ci'
EOF

# 确保配置文件权限正确
chmod 644 ${MYSQL_CONF} || { echo "设置 my.cnf 权限失败！"; exit 1; }
