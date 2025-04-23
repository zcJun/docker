#!/bin/bash

echo "🚀 开始安装和配置 Samba 共享目录 /data/xiaomi（用于 CW500 摄像头，启用 SMB1 协议，无 IP 限制）"

# 检查父目录
if [ ! -d "/data" ]; then
    echo "❌ 父目录 /data 不存在，请先创建！"
    exit 1
fi

# 获取用户输入的密码
read -sp "请输入 Samba 用户密码（建议使用强密码）: " SAMBA_PASS
echo
if [ -z "$SAMBA_PASS" ]; then
    echo "❌ 密码不能为空！"
    exit 1
fi

# 安装 Samba
sudo apt update && sudo apt install -y samba || { echo "❌ Samba 安装失败！"; exit 1; }

# 创建共享目录
SHARE_DIR="/data/xiaomi"
sudo mkdir -p "$SHARE_DIR" || { echo "❌ 创建目录 $SHARE_DIR 失败！"; exit 1; }
sudo chmod 770 "$SHARE_DIR"

# 设置访问账号
SAMBA_USER="cw500"
if ! id "$SAMBA_USER" &>/dev/null; then
    sudo useradd -M -s /sbin/nologin "$SAMBA_USER" || { echo "❌ 创建用户 $SAMBA_USER 失败！"; exit 1; }
    echo "🔧 已创建系统用户 $SAMBA_USER（无登录权限）"
fi

# 设置 Samba 密码
echo -e "$SAMBA_PASS\n$SAMBA_PASS" | sudo smbpasswd -a "$SAMBA_USER" || { echo "❌ 设置 Samba 密码失败！"; exit 1; }
sudo smbpasswd -e "$SAMBA_USER" || { echo "❌ 启用 Samba 用户失败！"; exit 1; }
echo "🔐 已设置 Samba 用户 $SAMBA_USER 密码"

# 设置权限
if ! getent group sambashare &>/dev/null; then
    sudo groupadd sambashare || { echo "❌ 创建 sambashare 组失败！"; exit 1; }
    echo "🔧 已创建 sambashare 组"
fi
sudo chown "$SAMBA_USER":sambashare "$SHARE_DIR"
sudo chmod 770 "$SHARE_DIR"
sudo usermod -aG sambashare "$SAMBA_USER" || { echo "❌ 添加用户到 sambashare 组失败！"; exit 1; }

# 备份配置文件
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak.$(date +%F-%H%M) || { echo "❌ 备份配置文件失败！"; exit 1; }

# 启用 SMB1 协议
if ! grep -q "client min protocol" /etc/samba/smb.conf; then
    if grep -q '^\[global\]' /etc/samba/smb.conf; then
        sudo sed -i '/^\[global\]/a\   client min protocol = NT1\n   server min protocol = NT1' /etc/samba/smb.conf || { echo "❌ 配置 SMB1 失败！"; exit 1; }
    else
        echo -e "[global]\n   client min protocol = NT1\n   server min protocol = NT1" | sudo tee -a /etc/samba/smb.conf || { echo "❌ 配置 SMB1 失败！"; exit 1; }
    fi
    echo "🔧 已启用 SMB1 协议支持（兼容 CW500 摄像头）"
    echo "⚠️ 严重警告：SMB1 协议不安全，且未限制 IP 地址，任何设备可能尝试访问共享目录！"
    echo "  - 强烈建议使用强密码，并确保服务器不在公网。"
    echo "  - 考虑升级 CW500 固件以支持 SMB2/SMB3，或通过防火墙限制访问 IP。"
else
    echo "⚠️ 协议配置已存在，跳过"
fi

# 添加共享配置
if ! grep -q "\[xiaomi\]" /etc/samba/smb.conf; then
    echo -e "\n[xiaomi]\n   path = $SHARE_DIR\n   browseable = yes\n   writable = yes\n   valid users = $SAMBA_USER\n   guest ok = no\n   force user = $SAMBA_USER\n   create mask = 0770\n   directory mask = 0770" | sudo tee -a /etc/samba/smb.conf || { echo "❌ 添加共享配置失败！"; exit 1; }
    echo "✅ 已添加 [xiaomi] 共享配置"
else
    echo "⚠️ 共享配置已存在，跳过"
fi

# 检查 Samba 配置有效性
sudo testparm -s /etc/samba/smb.conf >/dev/null 2>&1 || { echo "❌ Samba 配置文件有语法错误，请检查！"; exit 1; }

# 重启 Samba 服务
sudo systemctl restart smbd nmbd || { echo "❌ Samba 服务重启失败！"; exit 1; }
sudo systemctl enable smbd nmbd >/dev/null 2>&1

# 显示连接信息
IP_ADDR=$(ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | grep -v '127.0.0.1' | head -1)
if [ -z "$IP_ADDR" ]; then
    echo "⚠️ 无法获取服务器 IP 地址，请运行 'ip addr' 手动查看！"
    IP_ADDR="你的IP地址"
fi
echo "✅ 完成！CW500 摄像头可以使用以下信息连接共享目录："
echo "📂 共享路径：\\\\$IP_ADDR\\xiaomi"
echo "👤 用户名：$SAMBA_USER"
echo "🔐 密码：你设置的密码"
echo "📌 注意：已启用 SMB1 协议且未限制 IP 地址，请确保网络安全！"
