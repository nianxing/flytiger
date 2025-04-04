import logging
import json
import azure.functions as func
from azure.data.tables import TableServiceClient, TableClient
from datetime import datetime
import os
import uuid

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('订单处理函数被触发')
    
    try:
        # 获取请求体
        req_body = req.get_json()
        logging.info(f'接收到订单数据: {req_body}')
        
        # 验证订单数据
        required_fields = ['customer_name', 'customer_phone', 'address', 'total', 'items']
        for field in required_fields:
            if field not in req_body:
                return func.HttpResponse(
                    json.dumps({"error": f"缺少必填字段: {field}"}),
                    status_code=400
                )
        
        # 生成订单ID
        if 'id' not in req_body:
            req_body['id'] = str(uuid.uuid4())
        
        # 添加订单状态和创建时间
        req_body['status'] = '新订单'
        req_body['created_at'] = datetime.now().isoformat()
        
        # 将订单保存到Azure Table
        save_order_to_table(req_body)
        
        # 发送订单确认邮件（实际应用中可以添加此功能）
        # send_confirmation_email(req_body)
        
        return func.HttpResponse(
            json.dumps({"message": "订单已成功处理", "order_id": req_body['id']}),
            status_code=200
        )
        
    except Exception as e:
        logging.error(f"处理订单时发生错误: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500
        )

def save_order_to_table(order):
    """保存订单到Azure Table"""
    try:
        # 获取连接字符串
        connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        table_name = os.environ.get('AZURE_TABLE_NAME', 'orders')
        
        # 创建表服务客户端
        table_service = TableServiceClient.from_connection_string(connection_string)
        
        # 确保表存在
        try:
            table_service.create_table(table_name)
            logging.info(f"表 {table_name} 已创建")
        except Exception as e:
            # 表可能已存在，这是正常的
            logging.info(f"表 {table_name} 可能已存在: {str(e)}")
        
        # 获取表客户端
        table_client = TableClient.from_connection_string(connection_string, table_name)
        
        # 准备实体数据
        items_json = json.dumps(order['items']) if isinstance(order['items'], list) else order['items']
        
        entity = {
            'PartitionKey': 'orders',
            'RowKey': order['id'],
            'customer_name': order['customer_name'],
            'customer_email': order.get('customer_email', ''),
            'customer_phone': order['customer_phone'],
            'address': order['address'],
            'total': float(order['total']),
            'items': items_json,
            'status': order['status'],
            'created_at': order['created_at'],
            'payment_method': order.get('payment_method', ''),
            'shipping_method': order.get('shipping_method', ''),
            'notes': order.get('notes', '')
        }
        
        # 保存到表
        table_client.create_entity(entity=entity)
        logging.info(f"订单 {order['id']} 已保存到表")
        
        return True
        
    except Exception as e:
        logging.error(f"保存订单到表时出错: {str(e)}")
        raise 