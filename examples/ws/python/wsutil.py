import hashlib
import base64

OP_CONT=0
OP_TEXT=1
OP_BIN=2
OP_CLOSE=8
OP_PING=9
OP_PONG=10
def _HWORD(x):
    return chr(x>>8)+chr(x&0xff)
CLOSE_NORMAL=_HWORD(1000)
CLOSE_GOING_AWAY=_HWORD(1001)
CLOSE_PROTOCOL_ERROR=_HWORD(1002)
CLOSE_BAD_TYPE=_HWORD(1003)
CLOSE_BAD_DATA=_HWORD(1007)
CLOSE_POLICY_VIOLATION=_HWORD(1008)
CLOSE_TOO_BIG=_HWORD(1009)
CLOSE_EXTENSION_NEEDED=_HWORD(1010)
CLOSE_UNEXPECTED_CONDITION=_HWORD(1011)

opcodes = (OP_CONT,OP_TEXT,OP_BIN,OP_CLOSE,OP_PING,OP_PONG)

def challenge(v):
    try:
        x=hashlib.sha1(v+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11")
        return base64.b64encode(x.digest())
    except:
        return ""

def frame(data,opcode=1,rsvd=0):
    header=''
    header+=chr(0x80|opcode|rsvd<<4)
    realLength=len(data)
    #print 'realLength',realLength
    if realLength < 126:
        dummyLength=realLength
    elif realLength < 2**16:
        dummyLength = 126
    else:
        dummyLength=127
    header+=chr(dummyLength)
    if dummyLength == 127:
        header += chr(realLength >> 56 &0xff)
        header += chr(realLength >> 48 &0xff)
        header += chr(realLength >> 40 &0xff)
        header += chr(realLength >> 32 &0xff)
        header += chr(realLength >> 24 & 0xff)
        header += chr(realLength >> 16 & 0xff)
    if dummyLength == 126 or dummyLength == 127:
        header += chr(realLength >> 8 & 0xff)
        header += chr(realLength & 0xff)
    return header+data
