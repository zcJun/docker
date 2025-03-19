#!/bin/bash

# 定义所有目录
BASE_DIR="/data"
MYSQL_DIR="${BASE_DIR}/mysql"
DATA_DIR="${MYSQL_DIR}/data"    # 数据目录
CONF_DIR="${MYSQL_DIR}/conf"    # 配置目录
LOG_DIR="${MYSQL_DIR}/log"      # 日志目录

# 一次性创建所有目录
echo "创建所有目录..."
mkdir -p "${DATA_DIR}" "${CONF_DIR}" "${LOG_DIR}" || { echo "创建失败！"; exit 1; }

# 设置目录权限（改为 755）
echo "设置目录权限..."
chmod 755 "${DATA_DIR}" || { echo "设置 data 权限失败！"; exit 1; }
chmod 755 "${CONF_DIR}" || { echo "设置 conf 权限失败！"; exit 1; }
chmod 755 "${LOG_DIR}" || { echo "设置 log 权限失败！"; exit 1; }

# 如果系统启用了 SELinux，设置上下文
if command -v selinuxenabled &> /dev/null && selinuxenabled; then
    echo "检测到 SELinux 已启用，设置上下文..."
    chcon -Rt container_file_t "${MYSQL_DIR}" || { echo "设置 SELinux 上下文失败！"; exit 1; }
fi

echo "目录创建和权限设置完成！"

# # 创建 my.cnf 文件
# MYSQL_CONF="${CONF_DIR}/my.cnf"

# echo "创建 MySQL 配置文件..."
# cat > "${MYSQL_CONF}" << 'EOF'
# EOF

# # 确保配置文件权限正确
# chmod 644 "${MYSQL_CONF}" || { echo "设置 my.cnf 权限失败！"; exit 1; }

# echo "MySQL 配置文件创建完成！"
