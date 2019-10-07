# OWASP 核心规则转存到 ES


## WEB 管理端须知。
```shell
docker run -itd --name=modops -p 8077:8077 \
-v /etc/localtime:/etc/localtime:ro \
-v $(pwd)/tengine/vhosts:/etc/nginx/vhosts \
-v /opt/owasp_crs_rules:/opt/owasp_crs_rules \
-v $(which docker):/usr/bin/docker \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /home/waf-phaser4/apps:/usr/src/apps \
-v ./collect_static:/usr/src/collect_static \
-v ./config.yml:/usr/src/config.yml \
-v registry.cn-hangzhou.aliyuncs.com/anglecv/modops:v1 \
/usr/local/bin/gunicorn website.wsgi:application -w 2 -b :8077
```