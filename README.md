# Network-Port-Manage

## 项目简介
Network-Port-Manage 是一个基于 Flask 的 Web 应用程序，用于监控主机的端口使用情况。用户可以通过登录界面访问系统，并查看当前主机的端口与进程的对应关系。

## 功能特性
- **用户登录**：通过用户名和密码登录系统。
- **端口监控**：显示主机的端口与进程对应关系，并支持按端口号排序。
- **速率限制**：通过 Flask-Limiter 限制 API 的访问频率。
- **HTTPS 支持**：自动生成 SSL 证书，启用 HTTPS。

## 环境变量
以下环境变量在 `docker-compose.yml` 中定义：
- `ALLOWED_SUBNET`：允许访问的子网（举例：`192.168.1.0/24`, 默认所有网段可以访问）。
- `USERNAME`：登录用户名（默认：`admin`）。
- `PASSWORD`：登录密码（默认：`password`）。
- `DEFAULT_RATE_LIMIT`：全局速率限制（默认：`100 per hour`）。
- `API_RATE_LIMIT`：API 速率限制（默认：`10 per minute`）。

## 部署步骤

### 1. 构建 Docker 镜像
在项目根目录运行以下命令：
```bash
docker build -t network-port-manage .
```

### 2. 启动服务
通过 Docker Compose 启动服务：
```bash
docker-compose up -d
```

### 3. 访问应用
在浏览器中访问：
```
https://<主机IP>:7899
```
使用 `docker-compose.yml` 中定义的用户名和密码登录。

## 注意事项
1. **主机网络模式**：容器使用 `host` 网络模式，直接访问主机的网络堆栈。
2. **挂载 `/proc` 文件系统**：通过挂载 `/proc` 文件系统，容器内的 `psutil` 可以读取宿主机的进程和端口信息。
3. **HTTPS 支持**：容器启动时会自动生成自签名 SSL 证书。

## 常用命令

### 查看容器日志
```bash
docker logs -f network-port-manage
```

### 停止服务
```bash
docker-compose down
```

### 重启服务
```bash
docker-compose restart
```

## 界面效果如下
![159a7b27-97a7-4b83-97e1-b977927d5291](https://github.com/user-attachments/assets/06216d46-36cf-4f2c-bcc9-0655f7aa10fc)

## 许可证
本项目遵循 [GNU Affero General Public License v3 (AGPL-3.0)](https://www.gnu.org/licenses/agpl-3.0.html) 许可证。


