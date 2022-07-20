ARG PYTHON_VERSION=${PYTHON_VERSION}
FROM python:${PYTHON_VERSION}

ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}

RUN apt-get update -yqq && \
    groupadd -g ${PGID} pyflask && \
    useradd -u ${PUID} -g pyflask -s /bin/bash -m pyflask && \
    usermod -p "*" pyflask

USER root

# 安装基础工具
RUN apt update && \
    apt upgrade -y && \
    apt install -y software-properties-common net-tools iputils-ping openssh-server vim && \
    apt install -y make build-essential libssl-dev zlib1g-dev && \
    apt install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl && \
    apt install -y llvm libncurses5-dev libncursesw5-dev


# USER pyflask

# 安装默认需要的包
ADD ./requirements.txt /home/pyflask/requirements.txt

ARG PIP_REGISTRY=${PIP_REGISTR}
RUN pip install -i ${PIP_REGISTRY} --upgrade pip && \
    pip install -i ${PIP_REGISTRY} -r /home/pyflask/requirements.txt

#  配置环境变量, 可以使用相关命令
ENV PATH "/home/pyflask/.local/bin:$PATH"

ARG PROJECT_NAME=${PROJECT_NAME}
WORKDIR /home/pyflask/py_projects/${PROJECT_NAME}

# 添加 gunicorn 配置文件
RUN mkdir -p /home/pyflask/logs
# ADD ./flask-app/gunicorn.conf.py /home/pyflask/gunicorn.conf.py 

EXPOSE 8000 

ENTRYPOINT [ "/bin/bash", "-c", "gunicorn -c /home/pyflask/gunicorn.conf.py server:app" ]

# ENTRYPOINT [ "/bin/bash", "-c", "gunicorn -c /home/pyflask/gunicorn.conf.py server:app & runuser -u pyflask -- celery --app=celery_app worker -l INFO" ]






# # 安装 gunicorn 
# # USER pyflask
# RUN /bin/bash -c "pip install flask gunicorn"


# RUN mkdir -p /home/pyflask/py_projects
# WORKDIR /home/pyflask/py_projects/${PROJECT_NAME}

# CMD gunicorn -c /home/pyflask/pygun.py run:app










