import datetime
import logging
import requests

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config, view_defaults

from smartgymapi.lib.exceptions.validation import NotUniqueException
from smartgymapi.lib.validation.device import DeviceSchema
from smartgymapi.models import commit, persist, rollback, delete
from smartgymapi.models.device import Device
from smartgymapi.models.gym import get_gym_by_MAC_address
from smartgymapi.models.user_activity import UserActivity
from smartgymapi.models.weather import Weather

log = logging.getLogger(__name__)


@view_defaults(containment='smartgymapi.lib.factories.device.DeviceFactory',
               context='smartgymapi.lib.factories.device.DeviceFactory',
               permission='device',
               renderer='json')
class DeviceHandler(object):

    def __init__(self, request):
        self.request = request
        self.settings = self.request.registry.settings

    @view_config(request_method='POST', permission='checkin', name='checkin')
    def checkin(self):
        schema = DeviceSchema(strict=True)
        try:
            result, errors = schema.load(self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        device = self.request.context.get_checkin_device(
            result['device_address'])
        device.last_used = datetime.datetime.now()

        activity = device.user.active_activity
        response = {
            "user": "{} {}".format(
                device.user.first_name, device.user.last_name)
        }

        # if there's an active activy for the user the user needs to be checked
        # out
        if activity:
            activity.end_date = datetime.datetime.now()
            response["status"] = "checked out"

        else:
            activity = UserActivity()
            activity.start_date = datetime.datetime.now()
            activity.user = device.user
            activity.gym = get_gym_by_MAC_address(result['client_address'])
            response["status"] = "checked in"

            # we give units: metric for the api to return celcius
            r_params = {"q": activity.gym.city,
                        "appid": self.settings['open_weather_api_key'],
                        "units": "metric"}
            r = requests.get(
                self.settings['open_weather_url_current'],
                params=r_params).json()
            weather = Weather()
            if r.get('rain'):
                weather.raining_outside = True
            try:
                weather.temperature = r['main']['temp']
            except KeyError:
                log.WARN('Temparature not found')

            activity.weather = weather

        try:
            persist(device)
            persist(activity)
        except:
            log.critical("Something went wrong checking in",
                         exc_info=True)
            rollback()
        finally:
            commit()

        return response

    @view_config(request_method='GET')
    def list(self):
        return DeviceSchema(
            many=True,
            only=('name', 'device_address', 'device_class')
        ).dump(self.request.context.get_devices())

    @view_config(request_method='POST')
    def post(self):
        schema = DeviceSchema(strict=True, only=('name', 'device_address',
                                                 'device_class'))
        try:
            # The device address should first be validated to check if no
            # device already exists with the same address.
            schema.validate_device_address(self.request.json_body)
            result, errors = schema.load(self.request.json_body)
        except (ValidationError, NotUniqueException) as e:
            raise HTTPBadRequest(json={'message': str(e)})

        device = Device()
        device.set_fields(result)

        try:
            persist(device)
        except:
            log.critical("Something went wrong saving the device",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

    @view_config(context=Device, request_method='DELETE')
    def delete(self):
        try:
            delete(self.request.context)
        except:
            log.critical("Something went wrong deleting the device",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()
