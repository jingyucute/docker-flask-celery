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

# USER pyflask

ADD ./requirements.txt /home/pyflask/requirements.txt

ARG PIP_REGISTRY=${PIP_REGISTR}
RUN pip install -i ${PIP_REGISTRY} -r /home/pyflask/requirements.txt

#  配置环境变量, 可以使用相关命令
ENV PATH "/home/pyflask/.local/bin:$PATH"

ARG PROJECT_NAME=${PROJECT_NAME}
WORKDIR /home/pyflask/py_projects/${PROJECT_NAME}

# root 指定pyflask用户启动进程
ENTRYPOINT [ "/bin/bash", "-c", "runuser -u pyflask -- celery --app=celery_app worker -l INFO"]