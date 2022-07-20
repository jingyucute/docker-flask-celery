## Docker-Flask-Celery

> 这个项目是采用docker部署的关于Flask框架的项目, 这是一个简单的模板，可以快速运行起来

### 架构说明
    1. 整体使用Flask框架作为web服务， 通过gunicorn来托管flask应用，可实现热加载
    2. 使用celery作为分布式异步消息队列，redis作为broker存储待执行的任务, mongodb作为backend存储处理结果
    3. 使用flower来可视化异步消息的处理进程和结果
    4. 配合 celery-once 可以实现消息队列不重复执行， 其简单原理就是利用redis分布式锁
    5. 使用nginx来实现反向代理到gunicorn，负载均衡(暂时只有一个服务)

### 运行方式
```
    docker-compose up -d
    bash deploy.sh
```
#### 1. 执行docker命令， 会启动以下几个容器
- redis
    存储消息队列待执行任务
    也可以用作缓存
- mongo
    存储消息队列任务执行结果
    项目的数据存储
- celery
    启动异步消息队列
- flower
    监听异步消息队列， 可视化
- flask-app
    启动项目web服务
- nginx
    反向代理
#### 2. 执行shell脚本
    这个会在容器中下载项目中需要的python包
    每次更新代码后，都需要执行这个脚本

### example
> 一个简单的示例，通过访问api, 来爬取豆瓣上的top250的电影和相关信息
```
    curl localhost:7787/get_top_movies
```
在mongo数据库中可以查看相关数据
也可以吧把爬取任务放在celery中，实现异步处理, 这儿就不演示了