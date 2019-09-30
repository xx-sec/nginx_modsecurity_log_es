# syslog-ng with es 
- [重要参考](https://www.syslog-ng.com/community/b/blog/posts/syslog-ng-and-elasticsearch-7-getting-started-on-rhel-centos)
- https://www.syslog-ng.com/technical-documents/doc/syslog-ng-open-source-edition/3.22/administration-guide/2#TOPIC-1209069


## 2019-8-12


```
cd /etc/yum.repos.d/
	wget https://copr.fedorainfracloud.org/coprs/czanik/syslog-ng321/repo/epel-7/czanik-syslog-ng321-epel-7.repo
	yum install syslog-ng
	yum install syslog-ng-http
	systemctl enable syslog-ng
	systemctl start syslog-ng
```