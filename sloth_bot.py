import sys
import socket
import string
import re
import find_sloth
import imgup

HOST="irc.freenode.net"
PORT=6667
NICK="sloth_bot"
IDENT="sloth_bot"
REALNAME="sloth_both"
CHAN= # INSERT CHANNEL HERE
readbuffer=""

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("JOIN :%s\r\n" % CHAN)

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)
        print line

        if (len(line) != 0 and line[1] == 'PRIVMSG'):
            text = line.pop() # last element
            if (len(re.findall(r'<sloth>',text)) != 0):
                img_name = find_sloth.find_sloth()
                url = imgup.upload_sloth(img_name)
                s.send("PRIVMSG %s :%s\r\n" % (CHAN, url))

