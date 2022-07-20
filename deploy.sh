#! /bin/bash

docker-compose exec flask-app pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
docker-compose exec celery pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt 

# 重启celery 会让任务先执行完
# 不用重启 flask-app, 做了热加载
docker-compose restart celery flower
