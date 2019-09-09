# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    classification_id = Column(Integer, ForeignKey('classifications.id'))

    classification = relationship("Classification", backref=backref("categories", cascade="all, delete-orphan",
                                                                    single_parent=True))

    def __init__(self, name, classification):
        self.name = name
        self.classification = classification

    def __str__(self):
        cadena = '{}¥{}¥{}'.format(self.id, self.name, self.classification_id)
        return cadena
