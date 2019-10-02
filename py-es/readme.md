# 通过syslog-ng发送日志，通过python处理发送到最终的ES上。


## python3 环境 ub1804
```
sudo apt-get -y install python3-pip python3-setuptools 
sudo /usr/bin/python3 -m pip install -U pylint --user --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 运行


## 运行 Redis
```
docker run -itd -p 6379:6379 \
--name=redis --restart=always \
-v /srv/docker/redis_cso:/var/lib/redis \
-v /etc/localtime:/etc/localtime \
-e REDIS_PASSWORD=sqsjywl123 \
registry.cn-hangzhou.aliyuncs.com/xxzhang/redis:4.0.9
```

## 运行
-= 
