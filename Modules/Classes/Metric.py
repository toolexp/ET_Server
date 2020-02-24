from sqlalchemy import Column, Integer, String
from Modules.Config.base import Base


class Metric(Base):
    """
    A class used to represent a metric. A metric object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param name: name of the metric
    :type name: str
    :param description: description of the metric
    :type description: str
    """

    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, id, name, description):
        """
        Constructor of the class
        """
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}'.format(self.id, self.name, self.description)
