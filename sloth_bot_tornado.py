import find_sloth
import imgup

import tornado.ioloop
import tornado.iostream
import socket
import string
import re

HOST="irc.freenode.net"
PORT=6667
NICK="sloth_bot"
IDENT="sloth_bot"
REALNAME="sloth_both"
CHAN=  # Channel


def join_irc():
    stream.write("NICK {}\r\n".format(NICK))
    stream.write("USER {} {} bla :{}\r\n".format(
                 IDENT, HOST, NICK))
    stream.write("JOIN :{}\r\n".format(CHAN))
    print "joined {}".format(CHAN)

    stream.read_until('\r\n', read)

def read(data):
    # irc msg format =   :<prefix> <command> <params> :<trailing>

    # regex created from: http://calebdelnay.com/blog/2010/11/parsing-the-irc-message-format-as-a-client
    match = re.search(r'^(:(?P<prefix>\S+) )?(?P<command>\S+)(?: (?!:)(?P<params>.+?))?( :(?P<trail>.+))?$', data)

    prefix = match.group('prefix')
    command = match.group('command')
    params = match.group('params')
    trail = match.group('trail')

    # user message: prefix = username, command = PRIMSG, trail = msg
    if command == 'PRIVMSG':
        m = re.search(r'^{}: kill (\w+)'.format(NICK), trail)
        if m:
            read.kill_user = m.groups()[0]
            print read.kill_user

        if read.kill_user and read.kill_user in prefix:
            stream.write("PRIVMSG {} :{}: fuck you\r\n".format(CHAN, read.kill_user))

        if '<sloth>' in trail:
            try:
                search_terms = re.findall(r'<sloth> (\w+\S*)*', trail)
                if search_terms:
                    search_terms = search_terms[0]
                img_name = find_sloth.find_sloth(search_terms)
                url = imgup.upload_sloth(img_name)
                stream.write("PRIVMSG {} :{}\r\n".format(CHAN, url))
            except:
                pass
    elif command == 'PING':
        # don't kick the sloth :(
        stream.write("PONG {}\r\n".format(trail))

    stream.read_until('\r\n', read)

read.kill_user = ""

def shutdown_app():
    tornado.ioloop.IOLoop.instance().stop()

socket = socket.socket()
stream = tornado.iostream.IOStream(socket)
stream.connect ((HOST, PORT), join_irc)
stream.set_close_callback(shutdown_app)

tornado.ioloop.IOLoop.instance().start()
