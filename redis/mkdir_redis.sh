
#!/bin/bash

# 定义所有目录
BASE_DIR="/data"
MYSQL_DIR="${BASE_DIR}/redis"
DATA_DIR="${MYSQL_DIR}/data"

# 一次性创建所有目录
echo "创建所有目录..."
mkdir -p "${DATA_DIR}"|| { echo "创建失败！"; exit 1; }

# 设置目录权限（改为 755）
echo "设置目录权限..."
chmod 755 "${DATA_DIR}" || { echo "设置 data 权限失败！"; exit 1; }

# 如果系统启用了 SELinux，设置上下文
if command -v selinuxenabled &> /dev/null && selinuxenabled; then
    echo "检测到 SELinux 已启用，设置上下文..."
    chcon -Rt container_file_t "${MYSQL_DIR}" || { echo "设置 SELinux 上下文失败！"; exit 1; }
fi

echo "目录创建和权限设置完成！"

# 创建 my.cnf 文件
MYSQL_CONF="${MYSQL_DIR}/redis.conf"

echo "创建 MySQL 配置文件..."
cat > "${MYSQL_CONF}" << 'EOF'

# 绑定的IP地址，0.0.0.0 表示允许所有IP连接
bind 0.0.0.0

# Redis默认监听6379端口，可以根据需要修改
port 6379

# 设置Redis的访问密码
requirepass password

# RDB持久化设置
save 900 1
save 300 10
save 60 10000

# 开启AOF持久化
appendonly yes

# AOF重写时是否可以执行被阻塞的命令
aof-use-rdb-preamble yes

# 日志级别，可选值有debug, verbose, notice, warning
loglevel notice

# 指定日志文件路径，确保它指向/data目录下的文件
logfile /data/redis.log

# 数据库数量，默认是16个数据库
databases 16

# 设置实例的最大内存限制，避免占用过多内存
maxmemory 1024mb

# 达到最大内存后的淘汰策略
maxmemory-policy noeviction
EOF

# 确保配置文件权限正确
chmod 644 "${MYSQL_CONF}" || { echo "设置 redis.conf 权限失败！"; exit 1; }

echo "Redis 配置文件创建完成！"

