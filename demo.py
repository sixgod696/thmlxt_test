from flask import Flask, render_template, jsonify
import time
import socket
import threading
app = Flask(__name__)

# 用于存储最新数据的全局变量
latest_data = ""


def get_data():
    global latest_data
    HOST = '192.168.4.1'
    PORT = 9000
    # HOST = '192.168.229.63'
    # PORT = 6000
    ADDR = (HOST, PORT)

    while True:
        print("请求数据请求数据")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcpCliSock:
                tcpCliSock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                tcpCliSock.connect(ADDR)
                data = tcpCliSock.recv(2000)

                if data:  # 确保接收到了数据
                    latest_data = data.decode('utf-8')  # 解码为字符串
                    print(latest_data)
                else:
                    print("No data received")
            print(latest_data)  # 打印最新的数据
        except Exception as e:
            error_data = "Error: " + str(e)
        time.sleep(5)


@app.route('/')
def index():
    # 渲染一个简单的HTML页面
    return render_template('index.html')


@app.route('/get_latest_data')
def get_latest_data():
    # 创建一个线程来运行get_data函数
    thread = threading.Thread(target=get_data)
    thread.daemon = True
    thread.start()
    # 收到的字符串

    data = "Roll=13.36 Yall=136.6 Weight_Shiwu=0.31 g Weight_Shiwu2=39383.13 g Weight_Shiwu3=0.08 g Weight_Shiwu4=0.10 g warning=2"

    # data = latest_data
    print("收到的数据：" + data)
    # 拆分字符串成键值对
    items = data.split()

    # 初始化字典存储变量名和值
    variables = {}

    # 遍历每个键值对，将其加入字典
    for item in items:
        if '=' in item:
            key, value = item.split('=')
            # print(key)
            # print(value)
            variables[key] = value

    # 将字典中的值赋给相应的变量名
    Roll = float(variables['Roll'])
    Yall = float(variables['Yall'])
    Weight_Shiwu = float(variables['Weight_Shiwu'])
    Weight_Shiwu2 = float(variables['Weight_Shiwu2'])
    Weight_Shiwu3 = float(variables['Weight_Shiwu3'])
    Weight_Shiwu4 = float(variables['Weight_Shiwu4'])
    warning = float(variables['warning'])

    # print("---------------------")
    # print(Weight_Shiwu)
    # print(Weight_Shiwu2)
    # 返回最新的data作为JSON
    return jsonify({'左右倾斜角度': Roll,'前后倾斜角度': Yall,'腰椎受力程度': Weight_Shiwu,'腰椎平均受力时间': Weight_Shiwu2,'左倾受力程度': Weight_Shiwu3,'右倾受力程度': Weight_Shiwu4,'是否久坐': warning})


if __name__ == '__main__':


    # 启动Flask应用
    app.run(host='0.0.0.0', port=5000, debug=True)