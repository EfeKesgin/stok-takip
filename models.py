from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, default=0.0)
    
    # İndirim / Kampanya alanları
    discount_type = db.Column(db.String(20), nullable=True) # 'PERCENT', 'AMOUNT', 'BUY_X_PAY_Y'
    discount_value = db.Column(db.Float, default=0.0)
    campaign_buy_x = db.Column(db.Integer, default=0)
    campaign_pay_y = db.Column(db.Integer, default=0)
    discount_end_date = db.Column(db.DateTime, nullable=True)

    @property
    def current_price(self):
        if not self.discount_type or not self.discount_end_date:
            return self.price
            
        from datetime import datetime
        if self.discount_end_date <= datetime.now():
            return self.price
            
        if self.discount_type == 'PERCENT':
            return self.price * (1 - (self.discount_value / 100))
        elif self.discount_type == 'AMOUNT':
            return max(0, self.price - self.discount_value)
        elif self.discount_type == 'BUY_X_PAY_Y':
            if self.campaign_buy_x > 0:
                return (self.price * self.campaign_pay_y) / self.campaign_buy_x
            return self.price
            
        return self.price

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    
    unit_price = db.Column(db.Float, default=0.0)
    unit_purchase_price = db.Column(db.Float, default=0.0)
    unit_discount_loss = db.Column(db.Float, default=0.0)
    
    product = db.relationship('Product', backref=db.backref('transactions', lazy=True))
