import uuid

from sqlalchemy import Column, String, ForeignKey, relationship, DateTime, func
from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base, LineageBase, DBSession as session


class Device(Base, LineageBase):
    __tablename__ = 'device'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    device_address = Column(String(17))
    device_class = Column(String(100))
    user_id = Column(UUIDType, ForeignKey('user.id'))
    last_used = Column(DateTime(timezone=True), default=func.now())

    user = relationship("User")

    def set_fields(self, data):
        for key, value in data.items():
            setattr(self, key, value)


def get_device_by_device_address(device_address):
    return session.query(Device).filter(
        Device.device_address == device_address).one()


def get_device(id_):
    return session.query(Device).get(id_)