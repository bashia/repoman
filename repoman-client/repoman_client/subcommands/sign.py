#!/usr/bin/python

import binascii
import os
import sys
import tempfile

from repoman_client.subcommand import SubCommand
from argparse import ArgumentParser
from repoman_client.imagessl import sign


class SignImage(SubCommand):
    command_group = "advanced"
    command = "sign"
    alias = None
    description = 'Sign a virtual machine image'

    def get_parser(self):
        p = ArgumentParser(self.description)
        p.add_argument('-key', help='The location of the private key used for\
         signing the file')
        p.add_argument('target', help='The location of the file to be signed')
        return p

    def __call__(self, args, extra_args=None):
        sign(args.target,args.key)
