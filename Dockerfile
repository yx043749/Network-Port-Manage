# 使用官方 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 设置脚本为可执行
RUN chmod +x /app/entrypoint.sh

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 暴露端口
EXPOSE 7899

# 设置入口点脚本
ENTRYPOINT ["/app/entrypoint.sh"]

# 启动命令
CMD ["python", "port_show.py"]