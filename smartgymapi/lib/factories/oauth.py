import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.security import Allow, Everyone
from sqlalchemy.orm.exc import NoResultFound

from smartgymapi.lib.exceptions.oauth import (AuthorizationHeaderNotFound,
                                              InvalidAuthorizationMethod)
from smartgymapi.lib.factories import BaseFactory
from smartgymapi.lib.security import extract_client_authorization
from smartgymapi.lib.validation.oauth import OAuthClientSchema
from smartgymapi.models.oauth import get_client

log = logging.getLogger(__name__)


class OAuthFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self['token'] = TokenFactory(self, 'token')
        self['client'] = ClientFactory(self, 'client')


class TokenFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __acl__(self):
        return ((Allow, Everyone, 'token'),)

    def get_client(self, grant_type):
        try:
            client_credentials = extract_client_authorization(self.request)
            result, errors = OAuthClientSchema(
                strict=True, only=('client_id', 'client_secret')).load(
                    client_credentials)
        except (ValidationError, AuthorizationHeaderNotFound,
                InvalidAuthorizationMethod) as e:
            raise HTTPBadRequest(json=str(e))

        try:
            return get_client(**result)
        except NoResultFound:
            raise HTTPBadRequest


class ClientFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
