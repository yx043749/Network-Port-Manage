from flask import Flask, jsonify, render_template, request, abort, redirect, url_for, session
import psutil
import ipaddress
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# 加载 .env 文件中的环境变量
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 用于会话加密

# 从环境变量读取速率限制配置
DEFAULT_RATE_LIMIT = os.getenv('DEFAULT_RATE_LIMIT', '100 per hour')  # 默认每小时 100 次请求
API_RATE_LIMIT = os.getenv('API_RATE_LIMIT', '10 per minute')  # 默认每分钟 10 次请求

# 配置速率限制
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[DEFAULT_RATE_LIMIT]
)

# 从环境变量读取允许的网段、用户名和密码
ALLOWED_SUBNET = ipaddress.ip_network(os.getenv('ALLOWED_SUBNET', '192.168.1.0/24'))
USERNAME = os.getenv('USERNAME', 'admin')
PASSWORD = os.getenv('PASSWORD', 'securepassword')

# 设置 psutil 使用宿主机的 /proc 文件系统
psutil.PROCFS_PATH = "/host_proc"

@app.before_request
def limit_remote_addr():
    client_ip = ipaddress.ip_address(request.remote_addr)
    if client_ip not in ALLOWED_SUBNET:
        abort(403)  # 禁止访问

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="用户名或密码错误")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/api/ports')
@limiter.limit(API_RATE_LIMIT)  # 使用环境变量配置的速率限制
def get_ports():
    if not session.get('logged_in'):
        abort(401)  # 未授权

    ports = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr and conn.pid:
            ports.append({
                'port': conn.laddr.port,
                'pid': conn.pid,
                'process': psutil.Process(conn.pid).name()
            })

    # 按端口号排序
    ports = sorted(ports, key=lambda x: x['port'])

    return jsonify(ports)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # 未登录时跳转到登录页面
    return render_template('index.html')  # 登录后显示端口管理界面

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'), port=7899, host='0.0.0.0')  # 启用 HTTPS，监听所有网络接口
