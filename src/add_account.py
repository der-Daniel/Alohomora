#!/usr/bin/python3

# ------------------------------------------------------------------------------

# Alohomora
import config
import db
import shell_io

# ------------------------------------------------------------------------------


def add(name):
    length, lowercase, uppercase, numbers, specials = config.get_settings()
    print('\n~*~*~*~*~*~*~*~*~*~*~* New Password ~*~*~*~*~*~*~*~*~*~*~*~\n')
    print('{0} is to be added to the database.'.format(name))
    print('')
    print('Your default configuratshell_ion looks like this:')
    print('  - length:\t{0}'.format(length))
    print('  - lowercase:\t{0}'.format(lowercase))
    print('  - uppercase:\t{0}'.format(uppercase))
    print('  - numbers:\t{0}'.format(numbers))
    print('  - specialsx:\t{0}'.format(specials))
    print('')
    print('However some web services have some ridiculous limitatshell_ions...')
    print('Keep the default configurations?')
    g = shell_io.key_input('(Y)es, (No): ', ['y', 'Y', 'n', 'N', ''])
    if(g == 'n' or g == 'N'):
        length = shell_io.get_length(length)
        lowercase = shell_io.get_lowercase(lowercase)
        uppercase = shell_io.get_uppercase(uppercase)
        numbers = shell_io.get_numbers(numbers)
        specials = shell_io.get_specials(specials)
    db.add_account(name, length, lowercase, uppercase, numbers, specials)
