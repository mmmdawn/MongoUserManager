from . import Mongodb
from . import DB_ROLES, ALL_DB_ROLES, SUPERUSER_ROLES
from . import get_roles_msg, clear, press_any_key
from . import endless_function

from InquirerPy import inquirer
from InquirerPy.base.control import Choice, Separator


class App:
    def __init__(self):
        self.db = None

    def connect(self):
        connection_uri = inquirer.text(message='Connection URI:').execute()
        self.db: Mongodb = Mongodb(connection_uri)
        print('Connection established')

    @endless_function
    def home(self) -> bool:
        clear()
        choice = inquirer.fuzzy(
            message="Select:",
            choices=[
                Choice(value=None, name="Create new account"),
                'Exit',
                *self.db.users,
            ],
            default=None,
        ).execute()
        clear()

        if choice == 'Exit':
            print('\nBye')
            return False

        if choice:
            username = choice
            roles = self.db.users[username]
            print(get_roles_msg(username, roles))
            action = inquirer.select(
                message='Choose action:',
                choices=[
                    'Add role',
                    'Remove role',
                    Separator(),
                    'Change password',
                    'Drop user',
                    Separator(),
                    'Back'
                ]
            ).execute()

            if action == 'Change password':
                print(self.change_password(username))
                press_any_key()
            if action == 'Add role':
                print(self.add_role(username))
                press_any_key()
            if action == 'Remove role':
                print(self.remove_role(username))
                press_any_key()
            if action == 'Drop user':
                print(self.drop_user(username))
                press_any_key()
        else:
            print(self.create_user())
            press_any_key()
        return True

    def create_user(self):
        try_time = 1
        password = ''
        username = ''
        while try_time <= 3:
            username = inquirer.text(message='Username:').execute()
            if username in self.db.users:
                print('\nUser already exists\n')
                try_time += 1
                continue

            password = inquirer.secret(message='Password:').execute()
            confirm_password = inquirer.secret(message='Confirm password:').execute()
            if password != confirm_password:
                print('\nNot match\n')
                try_time += 1
            else:
                break

        if try_time > 3:
            return "Cancelled"

        roles = self.get_roles()
        confirm = inquirer.confirm(
            message=f'Confirm add new user: {username} with role(s): {roles}',
            default=True
        ).execute()

        if confirm:
            return self.db.create_user(username, roles, password)
        else:
            return "Cancelled"

    def change_password(self, username: str):
        try_time = 1
        password = ''
        while try_time <= 3:
            password = inquirer.secret(message='New password:').execute()
            confirm_password = inquirer.secret(message='Confirm new password:').execute()
            if password != confirm_password:
                print('\nNot match\n')
                try_time += 1
            else:
                break

        if try_time > 3:
            return "Cancelled"
        return self.db.change_password(username, password)

    def get_roles(self):
        role = inquirer.select(
            message='Select role:',
            choices=[*DB_ROLES, Separator(), *ALL_DB_ROLES, Separator(), *SUPERUSER_ROLES]
        ).execute()

        if role in DB_ROLES:
            dbs = inquirer.select(message='💡 Press <Tab> to choose more than one!\nSelect database(s): ',
                                  choices=self.db.dbs, multiselect=True).execute()
            new_roles = [{'role': role, 'db': db} for db in dbs]
        else:
            new_roles = [role]
        return new_roles

    def add_role(self, username: str):
        new_roles = self.get_roles()
        confirm = inquirer.confirm(message=f'Confirm add new role(s): {new_roles}', default=True).execute()
        if confirm:
            return self.db.add_roles(username, new_roles)
        else:
            return "Cancelled"

    def remove_role(self, username: str):
        roles = inquirer.select(
            message='Select role(s) to remove:',
            choices=[str(role) for role in self.db.users[username]],
            multiselect=True
        ).execute()

        roles = [eval(role) for role in roles]

        confirm = inquirer.confirm(message=f'Confirm remove role(s): {roles}', default=False).execute()

        if confirm:
            return self.db.remove_roles(username, roles)
        else:
            return "Cancelled"

    def drop_user(self, username: str):
        confirm = inquirer.confirm(message=f'Confirm drop user "{username}"', default=False).execute()
        if confirm:
            return self.db.drop_user(username)
        else:
            return "Cancelled"

    def run(self):
        self.connect()
        self.home()
