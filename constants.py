class MongoConstants:
    ADMIN_DB = 'admin'
    SYSTEM_USERS_COL = 'system.users'
    DEFAULT_PASSWORD = '123456'


DB_ROLES = [
    'read',
    'readWrite',
    'dbAdmin',
    'userAdmin',
    'dbOwner'
]

ALL_DB_ROLES = [
    'readAnyDatabase',
    'readWriteAnyDatabase',
    'userAdminAnyDatabase',
    'dbAdminAnyDatabase'
]

SUPERUSER_ROLES = [
    'root'
]
