# -*- coding: utf-8 -*-
import sys

__version__ = "2.1.17"

from ChatRoom.main import Room, User
from ChatRoom.net import Server, Client
from ChatRoom.net import hash_encryption
# from ChatRoom.gui import RunRoom as _RunRoom

log = encrypt = main = net = sys = gui = MessyServerHardware = None
del log, encrypt, main, net, sys, gui, MessyServerHardware