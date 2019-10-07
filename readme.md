# 第二代 nginx_modsecurity 管理日志
- 上一个版本 [tengine-mosecruity-logdev](https://github.com/xx-sec/tengine-mosecruity-logdev)

## 本版本修复上面版本的不足
- 1, 上面版本是 txt 日志非json格式。
- 2, 上个版本日志是到 mongo 再到 mysql; 本版本一步 es

## 2019-9-27 
- 开发过程

### 安装 modsecurity 
```
docker run -itd --net=host --name=modsec --restart=always \
-v /etc/localtime:/etc/localtime:ro \
-v /spool/log/:/spool/log/ \
-v $(pwd)/tengine/nginx.conf:/etc/nginx/nginx.conf \
-v $(pwd)/tengine/help.conf:/etc/nginx/help.conf \
-v $(pwd)/tengine/vhosts:/etc/nginx/vhosts \
registry.cn-hangzhou.aliyuncs.com/rapid7/modsecurity:v1 \
supervisord -c /etc/supervisord.conf 
``` 

## 部署安装 fluent 
- registry.cn-hangzhou.aliyuncs.com/rapid7/fluentd:v1
```
docker run -itd --net=host --name=flt \
    -v /spool/log/:/spool/log/ \
    -v /etc/localtime:/etc/localtime:ro \
    -v $(pwd)/fluentd/fluent.conf:/fluentd/etc/fluent.conf \
    actanble/fluentd:1.4
```


## 部署安装 es
```
mkdir -p /srv/docker/es/config/; 

docker run \
--name es \
-p 19200:9200 -p 19300:9300 \
-e ES_JAVA_OPTS="-Xmx1024m -Xms1024m" \
-e "discovery.type=single-node" \
-v /srv/docker/es/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
-v /srv/docker/es/es_data:/usr/share/elasticsearch/data \
-d elasticsearch:5.6.11
```
## ES 部署使用 way2king/docker-elk  
- 略

## 安装 syslog-ng with py-elesticsearch 
- https://www.syslog-ng.com/community/b/blog/posts/python-destination-getting-started
```
docker run -itd --name=sloges --net=host --restart=always \
-v /spool/:/spool/ \
-v $(pwd)/py-es/xetl:/software/xetl \
-v $(pwd)/py-es/syslog-ng.conf:/software/syslog-ng/etc/syslog-ng.conf \
registry.cn-hangzhou.aliyuncs.com/rapid7/syslog-es:v1 \
/bin/bash /entrypoint.sh 
```

## 安装
- -v $(which docker):/usr/bin/docker -v /var/run/docker.sock:/var/run/docker.sock
