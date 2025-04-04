import uuid
from datetime import datetime
import json

class Product:
    """产品类"""
    def __init__(self, id, name, description, specifications, price, image):
        self.id = id
        self.name = name
        self.description = description
        self.specifications = specifications
        self.price = price
        self.image = image
    
    @classmethod
    def from_dict(cls, source):
        """从字典创建产品对象"""
        return cls(
            id=source.get('id'),
            name=source.get('name'),
            description=source.get('description'),
            specifications=source.get('specifications'),
            price=source.get('price'),
            image=source.get('image')
        )
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'specifications': self.specifications,
            'price': self.price,
            'image': self.image
        }

class Order:
    """订单类"""
    def __init__(self, customer_name, customer_email, customer_phone, address, total, items, id=None, status='新订单', created_at=None):
        self.id = id or str(uuid.uuid4())
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone = customer_phone
        self.address = address
        self.total = total
        self.items = items
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
    
    @classmethod
    def from_dict(cls, source):
        """从字典创建订单对象"""
        items = source.get('items')
        if isinstance(items, str):
            try:
                items = json.loads(items)
            except json.JSONDecodeError:
                items = []
        
        return cls(
            id=source.get('id'),
            customer_name=source.get('customer_name'),
            customer_email=source.get('customer_email'),
            customer_phone=source.get('customer_phone'),
            address=source.get('address'),
            total=source.get('total'),
            items=items,
            status=source.get('status', '新订单'),
            created_at=source.get('created_at')
        )
    
    def to_dict(self):
        """转换为字典以便存储"""
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'address': self.address,
            'total': self.total,
            'items': json.dumps(self.items) if isinstance(self.items, list) else self.items,
            'status': self.status,
            'created_at': self.created_at
        } 