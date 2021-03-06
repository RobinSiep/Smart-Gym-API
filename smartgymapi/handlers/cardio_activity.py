import logging
from datetime import datetime

from marshmallow import ValidationError
from pyramid.httpexceptions import (HTTPBadRequest, HTTPInternalServerError,
                                    HTTPCreated, HTTPNoContent)
from pyramid.view import view_defaults, view_config

from smartgymapi.models import persist, commit, rollback, delete, flush
from smartgymapi.lib.factories.cardio_activity import (CardioActivityFactory,
                                                       is_cardio_activity_active)
from smartgymapi.lib.validation.cardio_activity import CardioActivitySchema
from smartgymapi.models.cardio_activity import CardioActivity

log = logging.getLogger(__name__)


@view_defaults(containment=CardioActivityFactory,
               permission='cardio_activity',
               renderer='json')
class RESTCardioActivty(object):
    def __init__(self, request):
        self.request = request

    @view_config(context=CardioActivityFactory, request_method='GET')
    def list(self):
        return CardioActivitySchema(many=True).dump(
            self.request.context.list_cardio_activities()).data

    @view_config(context=CardioActivity, request_method='GET')
    def get(self):
        return CardioActivitySchema().dump(self.request.context).data

    @view_config(context=CardioActivityFactory, request_method='POST')
    def post(self):
        try:
            if is_cardio_activity_active(
                    self.request.json_body['activity_id']):
                raise HTTPBadRequest(json={
                    'message': 'There is another cardio_acitivty active'})
        except KeyError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        cardio_activity = self.save(CardioActivity())
        raise HTTPCreated(json=cardio_activity)

    @view_config(context=CardioActivity, request_method='PUT')
    def put(self):
        cardio_activity = self.request.context
        if cardio_activity.end_date is None:
            cardio_activity.end_date = datetime.now()
        else:
            raise HTTPBadRequest(
                json={'message': 'Cardio activity is already ended'})

        self.save(cardio_activity)

    @view_config(context=CardioActivity, request_method='DELETE')
    def delete(self):
        try:
            delete(self.request.context)
        except:
            log.critical('Something went wrong deleting the cardio activity',
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()
            raise HTTPNoContent()

    def save(self, cardio_activity):
        try:
            result, errors = CardioActivitySchema(strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        cardio_activity.set_fields(result)

        try:
            persist(cardio_activity)
            flush()
            data = CardioActivitySchema().dump(cardio_activity).data
        except:
            log.critical('Something went wrong saving the cardio activity',
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

        return data
