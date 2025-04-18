# python-database-backup
Python：数据库备份脚本

## Python 版本
Python 3.6.8+

## 依赖包
```
pip install pyyaml
pip install arrow
pip install minio
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

## 脚本使用

1. 安装 Python 3
2. 安装依赖包
3. 配置 YAML文件：python_database__backup.yml / python_database__minio.yml
4. 执行脚本：python3 python_database_backup.py
