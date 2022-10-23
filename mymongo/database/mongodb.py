from copy import copy

from pymongo import MongoClient
from mymongo.constants import MongoConstants


class Mongodb:
    def __init__(self, connection_uri: str) -> None:
        super().__init__()
        self._client = MongoClient(connection_uri, serverSelectionTimeoutMS=5000)
        self._db = self._client[MongoConstants.ADMIN_DB]
        self._users_col = self._db[MongoConstants.SYSTEM_USERS_COL]

        self.users = None
        self.dbs = self._get_database_names()
        self.get_users()

    def create_user(self, name: str, roles: list, password: str = MongoConstants.DEFAULT_PASSWORD):
        res = self._db.command('createUser', name, pwd=password, roles=roles)
        self.get_users()
        return res

    def drop_user(self, username: str) -> dict:
        res = self._db.command('dropUser', username)
        self.get_users()
        return res

    def change_password(self, username: str, new_password: str) -> dict:
        return self._db.command('updateUser', username, pwd=new_password)

    def add_roles(self, username: str, new_roles: list) -> dict:
        user_roles = self._get_user_roles(username)
        c_user_roles = copy(user_roles)

        for new_role in new_roles:
            if new_role not in user_roles:
                user_roles.append(new_role)

        if c_user_roles == user_roles:
            return {}  # Nothing changed

        res = self._db.command('updateUser', username, roles=user_roles)
        self.get_users()
        return res

    def remove_roles(self, username: str, roles: list) -> dict:
        user_roles = self._get_user_roles(username)
        c_user_roles = copy(user_roles)

        for role in roles:
            if role in user_roles:
                user_roles.remove(role)

        if user_roles == c_user_roles:
            return {}

        res = self._db.command('updateUser', username, roles=user_roles)
        self.get_users()
        return res

    def get_users(self, db_name: str = MongoConstants.ADMIN_DB) -> None:
        _filter = {'db': db_name}
        _projection = {'_id': 0, 'user': 1, 'roles': 1}
        users = list(self._users_col.find(filter=_filter, projection=_projection))
        result = {item['user']: item['roles'] for item in users}
        self.users = result

    def _get_user_roles(self, username: str) -> list:
        user_info = self._users_col.find_one(filter={'user': username})
        return user_info['roles']

    def _get_database_names(self) -> list:
        return self._client.list_database_names()




if __name__ == '__main__':
    connection_url = "mongodb://dev:local@loclhost:27017"
    db = Mongodb(connection_url)
    # print(db.create_user('mmmdawn', [{'role': 'root', 'db': 'admin'}], '123123123'))
    print(db.users)
