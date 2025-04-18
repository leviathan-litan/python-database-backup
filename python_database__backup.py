# -*- coding: utf-8 -*-

# ==================================
# 模块
# ==================================

# ))))))))))))))))))))))))))))
# OS
# ))))))))))))))))))))))))))))

import os, sys

# ))))))))))))))))))))))))))))
# Time
# ))))))))))))))))))))))))))))

from datetime import datetime

# - pip install arrow
import arrow

# ))))))))))))))))))))))))))))
# YAML
# ))))))))))))))))))))))))))))

# - pip install pyyaml
import yaml

# ))))))))))))))))))))))))))))
# MinIO
# ))))))))))))))))))))))))))))

from python_database__minio import *

# ==================================
# YAML
# ==================================

# - 加载 YAML 文件
def yaml_load_file(config_file):

    read_file = open(
        file=config_file,
        mode='r',
        encoding='utf-8'
    )
    read_file_content = read_file.read()
    read_file.close()

    # yaml_data = yaml.load(
    #     stream=read_file_content,
    #     Loader=yaml.FullLoader
    # )
    yaml_data = yaml.safe_load(
        read_file_content
    )

    return yaml_data

def yaml_get_value(config_file_obj, variable_path, split_char='.'):
    
    data_target = config_file_obj

    for path_item in variable_path.split(split_char):
        if not path_item.isdigit():
            data_target = data_target[str(path_item)]
        else:
            data_target = data_target[int(path_item)]
    
    return data_target

# ==================================
# File and Directory
# ==================================

# 创建目录
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        # print(f"目标路径【{path}】已存在")
        pass
    except OSError as err:
        print(err)

# ==================================
# Date and Time
# ==================================

def display_current_datetime(message):
    print("")
    print(f"%%%%%%%%%%%%%%%%%%%%%%%%%% [{arrow.now()}] {message}")
    print("")

# ==================================
# Database: MySQL
# ==================================

# 备份 MySQL 数据库
def mysql_backup(vender, host, port, db_name, user, password, dir_backup_file, dir_minio_upload_base):

    # ##############################
    # 备份数据库 - 本地 / mysqldump
    # ##############################
    
    # -- 备份文件名称的后缀
    backup_file_suffix = "sql.gz"

    # -- 备份文件的名称
    file_backup = f"db_backup_file__{ vender }__{ host }__{ db_name }__{ current_date_YYYYMMDD_HHmmss }.{backup_file_suffix}"
    # -- 备份日志文件的名称
    file_backup_log = f"db_backup_file__{ vender }__{ host }__{ db_name }__{ current_date_YYYYMMDD_HHmmss }.log"

    # -- 备份文件完整路径
    full_path_backup_file = f"{dir_backup_file}/{file_backup}"
    # -- 备份日志文件完整路径
    full_path_backup_log_file = f"{dir_backup_file}/{file_backup_log}"

    # 显示
    print(f"------------")
    print(f"备份文件的名称：{file_backup}")
    print(f"备份文件的完整路径：{full_path_backup_file}")
    print(f"------------")

    # 备份的命令 / 预览
    command_backup = f"mysqldump -h {host} -u {user} -p{password} -P{port} --single-transaction --quick --databases {db_name} | gzip > {full_path_backup_file}"
    
    print(f"备份语句【{command_backup}】")
    print(f"------------")
    
    # 备份的命令 / 执行
    exit_code = os.system(command_backup)
    
    if exit_code == 0:
        display_current_datetime(
            message="数据库备份【成功】"
        )
    else:
        display_current_datetime(
            message="数据库备份【失败】"
        )

    # ##############################
    # 上传到 MinIO
    # ##############################

    print()
    print(f"MinIO 上传目录：{dir_minio_upload_base}")

    minio_upload_file(
        file_path_local=full_path_backup_file,
        file_path_minio=f"{dir_minio_upload_base}/{file_backup}",
    )

# ==================================
# 变量
# ==================================

# 配置文件
config_file = "python_database__backup.yml"
config_file_obj = yaml_load_file(
    config_file=config_file
)

# 解析配置文件获得配置项
backup_meta_dir_backup_base = yaml_get_value(
    config_file_obj=config_file_obj,
    variable_path="backup_meta.dir_backup_base"
)

backup_list = yaml_get_value(
    config_file_obj=config_file_obj,
    variable_path="backup_list"
)

# ==================================
# 运行
# ==================================

if backup_meta_dir_backup_base:
    make_sure_path_exists(backup_meta_dir_backup_base)

# =============================== 开始
display_current_datetime(
    message="执行【开始】"
)

# =============================== 执行

backup_list_item_cursor = 1
for backup_list_item in backup_list:

    # 开始阶段
    print(f"%%%%%%%%%%%%%%%%%%%%%%%%%% {backup_list_item_cursor}")

    # 显示
    # 原始信息
    # print(backup_list_item)
    # print(f"------------")

    # 变量
    # -- 时间信息
    current_date_YYYYMMDD = arrow.now().format('YYYYMMDD')
    current_date_YYYYMMDD_HHmmss = arrow.now().format('YYYYMMDD_HHmmss')

    # 时间
    print(f"当前时间【{current_date_YYYYMMDD}】")
    print(f"当前时间【{current_date_YYYYMMDD_HHmmss}】")
    print(f"------------")

    # 变量
    
    # -- 数据库信息
    vender = backup_list_item['vender']
    host = backup_list_item['host']
    port = backup_list_item['port']
    db_name = backup_list_item['db_name']
    user = backup_list_item['user']
    password = backup_list_item['password']
    dir_backup_base = backup_list_item['dir_backup_base']
    dir_minio_upload_base = backup_list_item['dir_minio_upload_base']

    # 当前数据库的备份起始目录（dir_backup_base）
    # 如果没有指定，则使用全局默认的备份起始目录
    if dir_backup_base == "":
        dir_backup_base = backup_meta_dir_backup_base

    # -- 备份文件所在的目录
    dir_backup_file = f"{dir_backup_base}/{vender}/{host}/{current_date_YYYYMMDD}"

    if dir_backup_file:
        make_sure_path_exists(dir_backup_file)

    # 格式化输出
    print(f"数据库类型：{vender}")
    print(f"备份文件所在目录：{dir_backup_file}")
    
    # -- 备份文件的名称
    file_backup = ""
    
    # 根据不同的 数据库类型（vender） 执行不同的备份策略
    # Python 3.10 之前：if ... elif ... else
    # Python 3.10 之后：match ... case

    if vender == "mysql":

        mysql_backup(
            vender=vender,
            host=host,
            port=port,
            db_name=db_name,
            user=user,
            password=password,
            dir_backup_file=dir_backup_file,
            dir_minio_upload_base=dir_minio_upload_base,
        )
        
    # 结束阶段
    print()

    backup_list_item_cursor += 1

# =============================== 结束
display_current_datetime(
    message="执行【完成】"
)

# ==================================
# 结束
# ==================================
