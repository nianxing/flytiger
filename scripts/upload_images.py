#!/usr/bin/env python3
import os
from azure.storage.blob import BlobServiceClient

def upload_images():
    """上传图片到Azure Blob存储"""
    print("开始上传产品图片到Azure Blob存储...")
    
    # 获取Azure存储连接字符串
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("未设置AZURE_STORAGE_CONNECTION_STRING环境变量")
    
    # 设置容器名称
    container_name = "productimages"
    
    # 创建BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # 获取容器客户端
    try:
        container_client = blob_service_client.get_container_client(container_name)
        # 检查容器是否存在，不存在则创建
        try:
            container_client.get_container_properties()
        except Exception:
            print(f"容器 {container_name} 不存在，正在创建...")
            container_client = blob_service_client.create_container(container_name)
    except Exception as e:
        print(f"创建容器客户端时出错: {str(e)}")
        raise
    
    # 图片目录路径
    images_dir = "app/static/images"
    
    # 确保目录存在
    if not os.path.exists(images_dir):
        print(f"图片目录 {images_dir} 不存在")
        return
    
    # 上传图片
    uploaded_count = 0
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            blob_name = filename
            file_path = os.path.join(images_dir, filename)
            
            print(f"正在上传 {filename}...")
            try:
                # 获取blob客户端
                blob_client = container_client.get_blob_client(blob_name)
                
                # 上传文件
                with open(file_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                
                uploaded_count += 1
                print(f"成功上传 {filename}")
            except Exception as e:
                print(f"上传 {filename} 时出错: {str(e)}")
    
    print(f"上传完成，共上传 {uploaded_count} 个图片文件")

if __name__ == "__main__":
    upload_images() 