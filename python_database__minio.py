# -*- coding: utf-8 -*-

# ==================================
# 模块
# ==================================

# ))))))))))))))))))))))))))))
# OS
# ))))))))))))))))))))))))))))

import os, sys, subprocess

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

# MINIO
# - pip install minio
from minio import Minio
from minio.error import S3Error
# from minio.commonconfig import Tags

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
# 变量
# ==================================

# 配置文件
config_file = "python_database__minio.yml"
config_file_obj = yaml_load_file(
    config_file=config_file
)

# ==================================
# MinIO
# ==================================

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 获得 MinIO 客户端对象

# MINIO 获得连接对象
def minio_get_connection():

    endpoint = yaml_get_value(
        config_file_obj=config_file_obj,
        variable_path="minio.client.endpoint"
    )
    accesskey = yaml_get_value(
        config_file_obj=config_file_obj,
        variable_path="minio.client.accesskey"
    )
    secretkey = yaml_get_value(
        config_file_obj=config_file_obj,
        variable_path="minio.client.secretkey"
    )

    connection = Minio(
        endpoint=endpoint,
        access_key=accesskey,
        secret_key=secretkey,
        secure=False
    )

    return connection

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% MinIO 查找

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% MinIO【检验 / MinIO 与 下载到本地后的大小进行比较】
def minio_file_size_diff__minio_local(minio_connection, bucket_name, file_path_minio, file_path_local):
    
    # 本地文件
    # file_path__local = f"{save_path}/{file_path_minio}"
    file_path__local = f"{file_path_local}"
    file_size__local = os.stat(file_path__local).st_size

    # MinIO文件
    file__minio = minio_connection.get_object(
        bucket_name,
        file_path_minio,
    )
    file_size__minio = int(
        file__minio.headers.get('content-length')
    )

    print(f"############## 本地文件【{file_path__local}】大小：{file_size__local}")
    print(f"############## MinIO文件【{file_path_minio}】大小：{file_size__minio}")

    if file_size__local == file_size__minio:
        # 大小相同
        return True
    else:
        # 大小不同
        return False


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% MinIO 创建路径

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% MinIO 上传文件

# 单次上传文件
# 参数：
# - file_path_local: 本地文件路径
# - file_path_minio: MinIO 中的文件对象的路径：需要根据配置文件 与 当前文件 进行生成
# - minio_bucket: 目标桶，在 xxx__minio.yml 的配置文件中指定

def minio_upload_file(
   file_path_local,
   file_path_minio,
):
    # MinIO 连接对象
    minio_connection = minio_get_connection()

    # xxx__minio.yml 中的配置项

    # 目标桶
    minio_bucket = yaml_get_value(
        config_file_obj=config_file_obj,
        variable_path="minio.client.bucket"
    )

    # 函数参数：显示
    print()
    print(f"%%%%%%%%% MinIO 上传文件 %%%%%%%%%")
    print(f"本地文件路径：{file_path_local}")
    print(f"MinIO 中的文件路径：{file_path_minio}")
    print(f"MinIO 中的目标桶：{minio_bucket}")

    # 执行上传
    display_current_datetime(
        message=f"MinIO / 上传文件 / 当前【{file_path_minio}】"
    )
    # 执行上传
    minio_connection.fput_object(
        bucket_name=minio_bucket,
        object_name=file_path_minio,
        file_path=file_path_local
    )

    upload_result_isOk = minio_file_size_diff__minio_local(
        minio_connection=minio_connection,
        bucket_name=minio_bucket,
        file_path_minio=file_path_minio,
        file_path_local=file_path_local,
    )

    if upload_result_isOk:
        display_current_datetime(
            message=f"MinIO / 上传文件 / 成功【{file_path_minio}】"
        )
    else:
        display_current_datetime(
            message=f"MinIO / 上传文件 / 失败【{file_path_minio}】"
        )

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% MinIO 下载文件

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% MinIO 删除

