#!/usr/bin/python

import binascii
import os
import sys
import tempfile

from repoman_client.subcommand import SubCommand
from argparse import ArgumentParser
from repoman_client.imagessl import ver


class Verify(SubCommand):
    command_group = "advanced"
    command = "ver"
    alias = 'verify'
    description = 'verify a SHA1 hex digest'

    def get_parser(self):
        p = ArgumentParser(self.description)
        p.add_argument('-cert', help='The location of the certificate used \
        for verifying the file')
        p.add_argument('target', help='The location of the file to be\
         verified')
        p.add_argument('digest', help='The location of the digest of the\
         file')
        return p

    def __call__(self, args, extra_args=None):
        ver(args.target,args.cert,args.digest)
