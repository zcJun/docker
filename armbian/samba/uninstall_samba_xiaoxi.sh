#!/bin/bash

echo "🧹 正在卸载 Samba 并还原配置..."

# 检查是否有备份文件
backup_file=$(ls -t /etc/samba/smb.conf.bak.* 2>/dev/null | head -n 1)

if [ -n "$backup_file" ]; then
    echo "🔄 发现备份文件：$backup_file，正在还原..."
    sudo cp "$backup_file" /etc/samba/smb.conf
else
    echo "⚠️ 未找到 smb.conf 的备份文件，跳过还原"
fi

# 重启 Samba 服务（避免配置残留影响）
sudo systemctl restart smbd

# 卸载 Samba
sudo apt remove --purge -y samba
sudo apt autoremove -y

# 删除共享目录（可选）
read -p "❓ 是否删除共享目录 /data/xiaomi？[y/N]: " del_dir
if [[ "$del_dir" =~ ^[Yy]$ ]]; then
    sudo rm -rf /data/xiaomi
    echo "🗑️ 已删除共享目录"
else
    echo "📁 共享目录保留"
fi

echo "✅ 卸载和还原完成"
