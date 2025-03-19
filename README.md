## Docker Compose 安装
- 1.下载适用于 Linux x86_64 的 Docker Compose
- `curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose`
- 2.应用可执行权限
- `chmod +x /usr/local/bin/docker-compose`
- 3.验证安装是否成功
- `docker-compose --version`

## 使用docker 创建 mysql数据库
- `先执行 mysql/mkdir_mysql.sh 创建文件夹`
- `再执行 mysql/docker-compose.yml  启动需要在文件夹中运行找到docker-compose.yml`

## 相关命令
- 创建文件夹 `sh mkdir_mysql.sh`
- 创建容器 `docker-compose up -d`
- 删除容器 `docker-compose down`
