from azure.data.tables import TableServiceClient, TableClient, UpdateMode
from azure.storage.blob import BlobServiceClient, ContentSettings
from flask import current_app
import uuid
import os

def get_table_client():
    """获取Azure Table客户端"""
    connection_string = current_app.config['AZURE_STORAGE_CONNECTION_STRING']
    table_name = current_app.config['AZURE_TABLE_NAME']
    
    try:
        # 创建表服务客户端
        table_service = TableServiceClient.from_connection_string(connection_string)
        
        # 确保表存在
        try:
            table_service.create_table(table_name)
            print(f"表 {table_name} 已创建")
        except Exception as e:
            # 表可能已存在，这是正常的
            print(f"表 {table_name} 可能已存在: {str(e)}")
        
        # 返回表客户端
        return TableClient.from_connection_string(connection_string, table_name)
    except Exception as e:
        print(f"获取表客户端时出错: {str(e)}")
        raise

def get_blob_client():
    """获取Azure Blob客户端"""
    connection_string = current_app.config['AZURE_STORAGE_CONNECTION_STRING']
    container_name = current_app.config['AZURE_BLOB_CONTAINER']
    
    try:
        # 创建blob服务客户端
        blob_service = BlobServiceClient.from_connection_string(connection_string)
        
        # 确保容器存在
        try:
            blob_service.create_container(container_name)
            print(f"容器 {container_name} 已创建")
        except Exception as e:
            # 容器可能已存在，这是正常的
            print(f"容器 {container_name} 可能已存在: {str(e)}")
        
        return blob_service.get_container_client(container_name)
    except Exception as e:
        print(f"获取blob客户端时出错: {str(e)}")
        raise

def save_order_to_table(order):
    """保存订单到Azure Table"""
    try:
        table_client = get_table_client()
        
        # 准备实体数据
        entity = order.to_dict()
        
        # 添加分区键和行键
        entity['PartitionKey'] = 'orders'
        entity['RowKey'] = order.id
        
        # 保存到表
        table_client.create_entity(entity=entity)
        
        return True
    except Exception as e:
        print(f"保存订单到表时出错: {str(e)}")
        raise

def get_orders(status=None):
    """从Azure Table获取订单列表"""
    try:
        table_client = get_table_client()
        
        # 查询条件
        query_filter = "PartitionKey eq 'orders'"
        if status:
            query_filter += f" and status eq '{status}'"
        
        # 执行查询
        entities = table_client.query_entities(query_filter)
        
        # 转换为订单对象
        from app.models import Order
        orders = [Order.from_dict(entity) for entity in entities]
        
        return orders
    except Exception as e:
        print(f"获取订单列表时出错: {str(e)}")
        raise

def upload_image(file_data, filename=None):
    """上传图片到Azure Blob Storage"""
    try:
        blob_client = get_blob_client()
        
        # 生成唯一文件名
        if not filename:
            file_extension = os.path.splitext(file_data.filename)[1]
            filename = f"{uuid.uuid4()}{file_extension}"
        
        # 设置内容类型
        content_settings = ContentSettings(content_type=file_data.content_type)
        
        # 上传文件
        blob = blob_client.get_blob_client(filename)
        blob.upload_blob(file_data, content_settings=content_settings, overwrite=True)
        
        # 返回URL
        return blob.url
    except Exception as e:
        print(f"上传图片时出错: {str(e)}")
        raise 