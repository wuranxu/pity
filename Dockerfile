# 使用基础镜像
FROM python:slim-buster
# 创建服务运行的目录
RUN mkdir /opt/server
#拷贝宿主机上下文目录到容器的/opt/server下
COPY . /opt/server
#cd命令进入到/opt/server，执行pip命令安装项目所需的包
RUN cd /opt/server && pip3 install -r requirements.txt -i https://pypi.douban.com/simple
#切换到/opt/server工作目录下
WORKDIR /opt/server
#容器启动时运行项目启动命令
CMD python3 main.py