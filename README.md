# python-database-backup
Python：数据库备份脚本

## Python 版本
Python 3.6.8+

## 依赖包
```
pip install pyyaml
pip install arrow
```

## 操作系统
- Linux
Linux 本地 需要安装 mysql-client，有 mysqldump
```
[root@mysql01 ~]# mysqldump -V
mysqldump  Ver 9.1.0-commercial for Linux on x86_64 (MySQL Enterprise Server - Commercial)
[root@mysql01 ~]# 
```

## 备份的数据文件

解压：
```
gunzip xxx.sql.gz
```
