from os import system, name


def get_roles_msg(username: str, roles: list):
    msg = f'Username: {username}\n' \
          f'Roles:'
    for role in roles:
        msg += f"\n\t{role['role']} - {role['db']}"
    msg += "\n------------------------------------------------------------------------------\n"
    return msg


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def press_any_key():
    input('\nPress any key to continue . . .')
