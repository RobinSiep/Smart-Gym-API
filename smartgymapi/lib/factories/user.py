from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.user import list_users, get_user


class UserFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        user = get_user(key)

        if user:
            user.set_lineage(UserFactory, 'user')
            return user

        raise KeyError()

    def get_users(self):
        return list_users()