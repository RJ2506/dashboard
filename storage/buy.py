from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class BuyingProducts(Base):
    """Buying Products"""

    __tablename__ = "buying_products"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(250), nullable=False)
    credit_card = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    purchased_date = Column(DateTime, nullable=False)
    date_created = Column(DateTime, nullable=False)
    transaction_number = Column(String(250), nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(
        self,
        customer_id,
        credit_card,
        price,
        purchased_date,
        transaction_number,
        trace_id,
    ):
        """Initializes a buy item """
        self.customer_id = customer_id
        self.credit_card = credit_card
        self.price = price
        self.purchased_date = datetime.datetime.now()
        self.date_created = datetime.datetime.now()
        self.transaction_number = transaction_number
        self.trace_id = trace_id

    def to_dict(self):
        """Dictionary Representation of a buy items"""
        dict = {}
        dict["id"] = self.id
        dict["customer_id"] = self.customer_id
        dict["credit_card"] = self.credit_card
        dict["price"] = self.price
        dict["purchased_date"] = self.purchased_date
        dict["date_created"] = self.date_created
        dict["transaction_number"] = self.transaction_number
        dict["trace_id"] = self.trace_id

        return dict
