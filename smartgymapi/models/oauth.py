import datetime
import logging
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from smartgymapi.lib.encrypt import get_secure_token
from smartgymapi.models.meta import Base, DBSession as session

log = logging.getLogger(__name__)


class OAuthClient(Base):
    __tablename__ = 'oauth_client'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUIDType(binary=False), default=uuid.uuid4)
    client_secret = Column(String(64), default=get_secure_token)
    client_type = Column(Enum("confidential", "public"), default="public")
    active = Column(Boolean, default=True)
    name = Column(String(100))

    def set_fields(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class OAuthAccessToken(Base):
    __tablename__ = 'oauth_access_token'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    client_id = (Column(UUIDType(binary=False),
                        ForeignKey('oauth_client.id')))
    access_token = Column(String(64), default=get_secure_token, unique=True)
    token_type = Column(Enum("Bearer"), default="Bearer")
    expiry_date = Column(DateTime(timezone=True))

    client = relationship('OAuthClient')

    @property
    def expires_in(self):
        seconds_left = (self.expiry_date - datetime.datetime.now(
            datetime.timezone.utc)
        ).total_seconds()
        return seconds_left if seconds_left > 0 else 0


def get_client(client_id, client_secret):
    return session.query(OAuthClient).filter(
        OAuthClient.client_id == client_id,
        OAuthClient.client_secret == client_secret).one()


def get_token_by_token(access_token):
    return session.query(OAuthAccessToken).filter(
        OAuthAccessToken.access_token == access_token).one()
