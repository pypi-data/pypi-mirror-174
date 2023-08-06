from django.contrib.auth.models import AbstractBaseUser

class Rol():
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

class TokenUser(AbstractBaseUser):
    def from_json(self, data):
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.is_active = data['is_active']
        self.email = data['email']
        self.google_id = data['google_id']

        self.roles = []
        for rol in data['roles']:
            self.roles.append(Rol(id=rol['id'], name=rol['name']))

    class Meta:
        managed = False
