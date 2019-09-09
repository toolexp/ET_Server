# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    data_type = Column(String)
    classification_id = Column(Integer, ForeignKey('classifications.id'))

    classification = relationship("Classification", backref=backref("sections", cascade="all, delete-orphan",
                                                                    single_parent=True))

    def __init__(self, name='', description='', data_type='', classification=None):
        self.name = name
        self.description = description
        self.data_type = data_type
        self.classification = classification
        if self.classification is not None:
            self.name = classification.name
            self.description = ''

    def __str__(self):
        cadena = '{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, self.data_type)
        return cadena
