# Copyright (c) 2017 by fauno <fauno@partidopirata.com.ar>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.    If not, see <http://www.gnu.org/licenses/>.

import weechat
import re
from random import choice

SCRIPT_NAME    = 'teleirc'
SCRIPT_AUTHOR  = 'fauno <fauno@partidopirata.com.ar>'
SCRIPT_VERSION = '0.3.0'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC    = 'Formats teleirc messages'

settings = {
    'username': 'EmmaGoldman',
    're': '^(?P<update>\w+)(?P<separator>\W+?)<(?P<username>[^>]+)> (?P<dent>.+)$',
    'me': '^(?P<update>\w+)(?P<separator>\W+?)<(?P<username>[^>]+)> \/me (?P<dent>.+)$',

    'hashtag_color': 'blue',

    'mention_re': '(@)([a-zA-Z0-9]+)',
    'hashtag_re': '(#)([a-zA-Z0-9]+)'
}

USERS = {}

def colorize (message):
    """Colorizes mentions and hashtags"""

    for identifier in ['mention','hashtag']:
        identifier_re = re.compile(weechat.config_get_plugin('%s_re' % identifier), re.UNICODE)

        for found in identifier_re.findall(message):
            found_full = ''.join(found)
            if identifier == 'mention':
                replace = color(nick_color(found[1]), found_full)
            else:
                replace = color(weechat.config_get_plugin('%s_color' % identifier), found_full)

            message = message.replace(found_full, replace)

    return message

# TODO respect nick_color_force
def random_nick_color ():
    colors = weechat.config_string(weechat.config_get('weechat.color.chat_nick_colors')).split(',')

    return choice(colors).replace(':', ',')

def nick_color (nick):
    if USERS.has_key(nick) and USERS[nick].has_key('color'):
        pass
    else:
        USERS[nick] = {}
        USERS[nick]['color'] = random_nick_color()

    return USERS[nick]['color']

def color (color, string):
    return ''.join([weechat.color(color), string, weechat.color('reset')])

def parse (server, modifier, data, the_string):
    flags = data.split(';')[2].split(',')

    # This is the user we should be parsing messages from, with
    # nick_ prepended
    username = 'nick_' + weechat.config_get_plugin('username')

    if username in flags:
        matcher = re.compile(weechat.config_get_plugin('re'), re.UNICODE)
        m       = matcher.search(weechat.string_remove_color(the_string, ""))

        if m:
            dent = colorize(m.group('dent'))
            username = color(nick_color(m.group('username')), m.group('username'))
            the_string = ''.join([ username, m.group('separator'), dent ])
    return the_string

def nicklist(data, completion_item, buffer, completion):
    for username in list(USERS.keys()):
        weechat.hook_completion_list_add(completion, username, 1, weechat.WEECHAT_LIST_POS_SORT)
        weechat.hook_completion_list_add(completion, '@' + username, 1, weechat.WEECHAT_LIST_POS_SORT)
    return weechat.WEECHAT_RC_OK

# init

if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
    for option, default_value in settings.iteritems():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, default_value)

    weechat.hook_modifier('weechat_print', 'parse', '')
    weechat.hook_completion('telegram_nicklist', 'list of Telegram users', 'nicklist', '')
