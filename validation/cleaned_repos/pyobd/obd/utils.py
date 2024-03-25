import errno
import glob
import logging
import string
import sys

import serial

logger = logging.getLogger(__name__)


class OBDStatus:
    """Values for the connection status flags"""

    NOT_CONNECTED = "Not Connected"
    ELM_CONNECTED = "ELM Connected"
    OBD_CONNECTED = "OBD Connected"
    CAR_CONNECTED = "Car Connected"


class BitArray:
    """
    Class for representing bitarrays (inefficiently)

    There's a nice C-optimized lib for this: https://github.com/ilanschnell/bitarray
    but python-OBD doesn't use it enough to be worth adding the dependency.
    But, if this class starts getting used too much, we should switch to that lib.
    """

    def __init__(self, _bytearray):
        self.bits = ""
        for b in _bytearray:
            v = bin(b)[2:]
            self.bits += ("0" * (8 - len(v))) + v  # pad it with zeros

    def __getitem__(self, key):
        if isinstance(key, int):
            if key >= 0 and key < len(self.bits):
                return self.bits[key] == "1"
            else:
                return False
        elif isinstance(key, slice):
            bits = self.bits[key]
            if bits:
                return [b == "1" for b in bits]
            else:
                return []

    def num_set(self):
        return self.bits.count("1")

    def num_cleared(self):
        return self.bits.count("0")

    def value(self, start, stop):
        bits = self.bits[start:stop]
        if bits:
            return int(bits, 2)
        else:
            return 0

    def __len__(self):
        return len(self.bits)

    def __str__(self):
        return self.bits

    def __iter__(self):
        return [b == "1" for b in self.bits].__iter__()


def bytes_to_int(bs):
    """converts a big-endian byte array into a single integer"""
    v = 0
    p = 0
    for b in reversed(bs):
        v += b * (2**p)
        p += 8
    return v


def bytes_to_hex(bs):
    h = ""
    for b in bs:
        bh = hex(b)[2:]
        h += ("0" * (2 - len(bh))) + bh
    return h


def twos_comp(val, num_bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (num_bits - 1))) != 0:
        val = val - (1 << num_bits)
    return val


def isHex(_hex):
    return all([c in string.hexdigits for c in _hex])


def contiguous(l, start, end):
    """checks that a list of integers are consequtive"""
    if not l:
        return False
    if l[0] != start:
        return False
    if l[-1] != end:
        return False

    # for consequtiveness, look at the integers in pairs
    pairs = zip(l, l[1:])
    if not all([p[0] + 1 == p[1] for p in pairs]):
        return False

    return True


def try_port(portStr):
    """returns boolean for port availability"""
    try:
        s = serial.Serial(portStr)
        s.close()  # explicit close 'cause of delayed GC in java
        return True

    except serial.SerialException as err:
        logging.error(err)
    except OSError as e:
        if e.errno != errno.ENOENT:  # permit "no such file or directory" errors
            raise e

    return False


def scan_serial():
    """scan for available ports. return a list of serial names"""
    available = []

    possible_ports = []

    if sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        possible_ports += glob.glob("/dev/rfcomm[0-9]*")
        possible_ports += glob.glob("/dev/ttyUSB[0-9]*")
        possible_ports += glob.glob("/dev/ttyS[0-9]*")
        # possible_ports += glob.glob("/dev/pts/[0-9]*")  # for obdsim

    elif sys.platform.startswith("win"):
        possible_ports += [
            "\\.\COM%d" % i for i in range(256)
        ]  # on win, the pseudo ports are also COM - harder to distinguish

    elif sys.platform.startswith("darwin"):
        exclude = ["/dev/tty.Bluetooth-Incoming-Port", "/dev/tty.Bluetooth-Modem"]
        # possible_ports += glob.glob("/dev/ttys00[0-9]*")  # for obdsim
        possible_ports += [
            port for port in glob.glob("/dev/tty.*") if port not in exclude
        ]

    # possible_ports += glob.glob('/dev/pts/[0-9]*') # for obdsim

    for port in possible_ports:
        if try_port(port):
            available.append(port)
    print("Available ports: " + str(available))
    return available
