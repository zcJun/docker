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
- 如果使用 `docker-compose`命令，需要进入到含有`docker-compose.yml`的相关文件
- 或者 `docker-compose -f /data/python/python_project/docker-compose.yml up --build`


## Docker部署Python fastapi框架
- 1.把拉取文件夹`python_project`相关文件部署到 `/data/python/python_project`
- 2.进入到 `cd /data/python/python_project`
- 3.执行命令编译 `docker-compose up -build` 编译项目，编译完项目使用ctrl+c，再使用 `docker-compose up -d`运行项目
- 相关命令：重启`docker-compose restart app`， 停止`docker-compose stop`， 启动`docker-compose start`， 前台启动`docker-compose up`，后台启动`docker-compose up -d`等等。 
