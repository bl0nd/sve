# -*- coding: utf-8 -*-

import os
import sys

def color(message, clr='n'):
    """Color a message.

    :param message: Message to color.
    :param clr: Color to use.
    :return: Colored :param: `message`.
    :rtype: str
    """
    if clr == 'r':
        return f'\033[31;1m{message}\033[0m'
    elif clr == 'g':
        return f'\033[32;1m{message}\033[0m'
    elif clr == 'y':
        return f'\033[33;1m{message}\033[0m'
    elif clr == 'n':
        return f'\033[1m{message}\033[0m'
    else:
        sys.exit(f'error: unknown color: {clr}')


def header(title, clr='n', border_type='='):
    """Draw a header.

    ================= an example =================

    :param title: The header title.
    :param color: (optional) The first letter of the header's color (n is none).
    :param border_type: (optional) The character with which to compose the header.
    :return: A header String.
    :rtype: str
    """
    term_width = int(os.popen('stty size', 'r').read().split()[1])

    if term_width < len(title):
        sys.exit('error: terminal is too small')

    border_len = (term_width - len(title) - 2) // 2
    border = border_type * border_len

    if term_width % 2 == 0:
        extra = '' if len(title) % 2 == 0 else border_type
    else:
        extra = '' if len(title) % 2 != 0 else border_type

    return color(f'{border} {title} {border}{extra}', clr)
