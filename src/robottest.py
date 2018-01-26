#!/usr/bin/python

# This file is part of RobotTest.  RobotTest is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.



import sys
from socket import *
import threading
from time import sleep
import select
from datetime import date

userNameLen = 9

hostname = "localhost"

userNames = {
    "mike"          : "password",
    "bob"           : "otherpassword",
    "kernelSanders" : "SecurPass",
    "admin"         : "sUp3rSecurPasSw0rd",
    "jim"           : "L33tP4sswrd"
}

def enable(obj, arg = None):
    obj.prompt = "#"

def printDate(obj, arg = None):
    obj.conn.sendall("Now is: %s\r\n" % date.today())

def setHostName(obj, arg = None):
    global hostname
    if arg != None:
        hostname = arg
    else:
        obj.conn.sendall("%s Requires an argument\r\n")

def setPasswd(obj, arg = None):
    global userNames

    if arg != None:
        for usr in userNames:
            userNames[usr] = arg
    else:
        obj.conn.sendall("%s Requires an argument\r\n")

def exitConnection(obj, arg = None):
    obj.conn.close()
    obj.exit = True

def showHelp(obj, arg = None):
    obj.conn.sendall("Available Commands:\r\n")
    for key in cmds:
        obj.conn.sendall("\t%s: %s\r\n" % (key, cmds[key]["help"]))

cmds = {
   "enable": {
        "help": "Enable Mode",
        "cb": enable
        },
    "date": {
        "help": "Get Date Time",
        "cb": printDate
        },
    "exit": {
        "help": "Close Connection",
        "cb": exitConnection
        },
    "hostname": {
        "help" : "Set hostname",
        "cb": setHostName
        },
    "help": {
        "help" : "Help Menu",
        "cb": showHelp
        },
    "password": {
        "help" : "Set Password",
        "cb": setPasswd
        }
    }

class ServiceD(threading.Thread):
    hostname = "localhost"
    def __init__(self, conn = None, addr = None):
        if conn == None or addr == None:
            raise Exception("Unexpected Connection")
        threading.Thread.__init__(self)

        self.conn = conn
        self.addr = addr

        self.prompt = ">"
        self.exit = False
        self.hostname = hostname

    def _getInput(self, timeout=60, size=64):
        read_sock = [self.conn]
        inputReady, ignore, ignore =  select.select( read_sock, [], [], 15)
        if inputReady == []:
            return None
        else:
            return self.conn.recv(size).rstrip().lower()


    def _auth(self, user, password):
        ret = True
        if password != None:
            try:
                if userNames[user] != password:
                    self.auth = False
                    ret = False
                else:
                    self.auth = True
                    ret = True

            except KeyError:
                ret = False
                pass

        return ret

    def banner(self):
        self.conn.send("Welcome to RobotTest Daemon\r\n")

    def motd(self):
        self.conn.send("\r\n\r\nToday is Good\r\n")

    def login(self):
        userNameLen = 8
        count = 0
        success = False
        self.auth = True
        while count < 3 and success == False:
            self.conn.sendall("Login: ")
            userName = self._getInput(15, userNameLen)
            if userName == None:
                self.conn.sendall("\r\nAuthentication Timeout\r\n")
                self.auth = False
                break
            else:
                self.conn.sendall("Passwd: ")
                password = self._getInput(15)

                status = self._auth(userName, password)
                if status == True:
                    success = True
                    self.auth = True
                else:
                    self.conn.sendall(
                            "\r\nAttempt(%d) Failed, try again.\r\n\r\n" % count)

            count += 1
        if count >= 3:
            self.auth=False

    def cli(self):
        self.conn.sendall("%s%s " % (self.hostname, self.prompt))
        cmd = self._getInput()
        while cmd != None and self.exit == False:
            self.cmd(cmd)

            if self.exit != True:
                self.conn.sendall("%s%s " % (self.hostname, self.prompt))
                cmd = self._getInput()

        if cmd == None:
           self.conn.sendall("\r\nSession Timeout\r\n")


    def cmd(self, cmd):
        try:
            cmd.index(" ")
            parts = cmd.split(" ")
            c = parts[0]
            a = parts[1]
        except ValueError:
            c = cmd
            a = None

        try:
            cb = cmds[c]["cb"]
            cb(self,a)
        except KeyError:
            self.conn.sendall("% Command Not Found\r\n")


    def run(self):
        self.banner()
        self.login()

        if self.auth != False:
            self.motd()
            self.cli()


        self.conn.close()


class TelnetD:
    def __init__(self, port=2059):
        self.port = port

    def start(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind(("localhost", self.port))
        print "telnet://%s:%d/" % ("localhost", self.port)
        self.s.listen(1)

        while True:
                try:
                    conn, addr = self.s.accept()
                    d = ServiceD( conn, addr )
                    d.start()
                except KeyboardInterrupt, e:
                    print "Keyboard Iteruprted exiting"
                    self.s.close()
                    sys.exit(0)
                except Exception, e:
                    print "Got an Exception %s" % e

        self.s.close()


def main():
    print "String RobotTestD"
    td = TelnetD()

    td.start()



if __name__ == "__main__":
    main()
