import binascii
import os
import sys
import tempfile

from repoman_client.subcommand import SubCommand
from argparse import ArgumentParser


def swaphexbin(infile):
        hexfile = open(infile,"r")
        textblock = hexfile.read()
        try:
            hexrep = textblock.split()[1]
        except IndexError:
            hexrep = textblock.split()[0]
        except IndexError:
            sys.exit("Invalid signature file")
        binrep = binascii.unhexlify(hexrep)
        outloc = tempfile.mkstemp()[1] + ".sha1"
        outfile = open(outloc,"wb")
        outfile.write(binrep)
        outfile.close()
        hexfile.close()
        return outloc

def sign(infile,key):
    temphile = tempfile.mkstemp()[1]
    try:
        if key and os.path.isfile(os.path.expanduser(key)):
            keyloc = key
        else:
            keyloc = '~/.globus/userkey.pem'
    except Exception:
        keyloc = '~/.globus/userkey.pem'
    sign = "openssl dgst -sha1 -hex -sign " + os.path.expanduser(keyloc)\
     + " -out " + temphile + " " + infile + "; cat " + temphile + "; rm "\
     + temphile
    os.system(sign)

def ver(infile,cert,digest):
    if not cert:
        certloc = '~/.globus/usercert.pem'
    else:
        certloc = cert
    sigloc = swaphexbin(digest)
    tempkey = tempfile.mkstemp()[1]
    getkey = "openssl x509 -in " + os.path.expanduser(certloc) +" -pubkey\
     -noout > " + tempkey
    os.system(getkey)
    ver = "openssl dgst -sha1 -binary -verify " + tempkey + " -signature \
    " + sigloc + " " + infile
    os.system(ver)
    os.remove(sigloc)
    os.remove(tempkey)
