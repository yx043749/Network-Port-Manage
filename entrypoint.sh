#!/bin/bash

# 检查是否已存在 SSL 证书
if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
    echo "生成 SSL 证书..."
    openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
else
    echo "SSL 证书已存在，跳过生成。"
fi

# 启动 Flask 应用
exec "$@"
