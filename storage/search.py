from pickle import FALSE
from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class SearchProducts(Base):
    """Search Products"""

    __tablename__ = "search_products"

    id = Column(Integer, primary_key=True)
    brand_name = Column(String(250), nullable=False)
    item_description = Column(String(250), nullable=False)
    price = Column(Float, nullable=False)
    date_created = Column(DateTime, nullable=False)
    product_name = Column(String(250), nullable=False)
    quantity_left = Column(Integer, nullable=False)
    sales_price = Column(Float, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(
        self,
        brand_name,
        item_description,
        price,
        product_name,
        quantity_left,
        sales_price,
        trace_id,
    ):
        """Initializes a blood pressure reading"""
        self.brand_name = brand_name
        self.item_description = item_description
        self.price = price
        self.date_created = datetime.datetime.now()
        self.product_name = product_name
        self.quantity_left = quantity_left
        self.sales_price = sales_price
        self.trace_id = trace_id

    def to_dict(self):
        """Dictionary Representation of a blood pressure reading"""
        dict = {}
        dict["id"] = self.id
        dict["brand_name"] = self.brand_name
        dict["item_description"] = self.item_description
        dict["product_name"] = self.product_name
        dict["price"] = self.price
        dict["quantity_left"] = self.quantity_left
        dict["sales_price"] = self.sales_price
        dict["date_created"] = self.date_created
        dict["trace_id"] = self.trace_id

        return dict
