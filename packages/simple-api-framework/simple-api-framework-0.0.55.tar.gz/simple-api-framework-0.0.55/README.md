<h1>Simple API Framework</h1>

This framework is based on Tornado, and it's used to simplify the development of small microservices.

To install it, just get the latest version from PyPi:

```shell
pip install simple-api-framework
```

To start you'll need to do this steps:

- Create an `.env` file and put this environment variables:

```shell
ENV=local
API_VERSION=1
SERVICE_HOST=127.0.0.1
SERVICE_PORT=50000

CORS_ENABLED=1
CORS_ALLOWED_ORIGINS=*

REDIS_URL=
REDIS_PREFIX=

MONGODB_URL=

DB_URL=
DB_TIMEOUT=15
DB_RESULTS_LIMIT=20
```

- Create a `run.py`:

```python
from simple_api_framework import Service, Endpoint


class TestEndpoint(Endpoint):
    methods = ['GET']
    
    async def get(self, *args, **kwargs):
        self.finish_with_ok_status()


class MyService(Service):
    NAME = 'service'

    def __init__(self):
        urls = [
            {'url': 'test', 'handler': TestEndpoint}
        ]
        super().__init__(urls=urls)


if __name__ == '__main__':
    MyService()

```

- Run this file and test `http://127.0.0.1:50000/api/v1/test/` endpoint - it should return you HTTP 200 status and 
response:

```json
{
  "ok": true
}
```

Database models (only PostgreSQL)

```python
class UserProfileModel(Model):
    TABLE_NAME = 'user_profiles'
    
    user_id = None
    first = None
    last = None


class UserModel(Model):
    TABLE_NAME = 'users'
    
    username = None
    password = None
    user_group_id = None
    
    profile = Relationship(UserProfileModel, 'user_id', 'id')
    query_field_example = QueryField(f"SELECT first FROM {UserProfileModel.TABLE_NAME} WHERE user_id=#field=id")

    
class UserGroupModel(Model):
    TABLE_NAME = 'user_groups'
    
    name = None
    users = Relationships(UserModel, 'user_group_id', 'id')
```

```python
user_group = UserGroupModel(name='Test Group')
await user_group.insert()

user = UserModel(username='test1@email.com', user_group_id=user_group.id)
await user.insert()
user_profile = UserProfileModel(user_id=user.id, first='Test1', last='User1')
await user_profile.insert()

user = UserModel(username='test2@email.com', user_group_id=user_group.id)
await user.insert()
user_profile = UserProfileModel(user_id=user.id, first='Test2', last='User2')
await user_profile.insert()

user = await UserModel.get(parameters={'username': 'test1@email.com'})
user.profile.first_name = 'Changed'
await user.profile.update()

for group in await UserGroupModel.all():
    print(group.frontend)
```
