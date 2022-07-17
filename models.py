from sqlalchemy import orm, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from config import DataBaseURI

engine = create_engine(DataBaseURI)

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    asin = Column(String(length=10))
    title = Column(String(length=200))
    reviews = relationship("Review", back_populates='product')

    @classmethod
    def create(cls, **kwargs):
        product = cls.get(**kwargs)
        if product is None:
            product = cls(**kwargs)
            product.save()

    @classmethod
    def convert_row_to_columns(cls, **kwargs):
        kwargs = {key.lower(): value for key, value in kwargs.items()}
        return kwargs

    @classmethod
    def get(cls, **kwargs):
        return session.query(cls).filter_by(**kwargs).first()

    def save(self):
        session.add(self)
        session.commit()

    def to_dict(self, **kwargs):
        page = kwargs['page']
        page_size = kwargs['page_size']
        start = page_size * (page - 1)
        end = page * page_size
        s = slice(start, end)
        del kwargs['page']
        del kwargs['page_size']
        len_reviews = len(self.reviews)
        return dict(
            Asin=self.asin, Title=self.title, Reviews=[review.to_dict(**kwargs) for review in self.reviews[s]],
            has_prev=bool(start > 0 and len_reviews), has_next=end < len_reviews
        )


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    title = Column(String(length=200))
    text = Column(String(length=65535))
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates='reviews')

    @classmethod
    def create(cls, **kwargs):
        review = cls(**kwargs)
        review.save()

    @classmethod
    def convert_row_to_columns(cls, **kwargs):
        kwargs = {key.lower(): value for key, value in kwargs.items()}
        kwargs['text'] = kwargs['review']
        kwargs['product'] = Product.get(asin=kwargs['asin'])
        del kwargs['review']
        del kwargs['asin']
        return kwargs

    def save(self):
        session.add(self)
        session.commit()

    def to_dict(self):
        return dict(Title=self.title, Text=self.text)


Session = orm.sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
