import os,logging
from pyraklib import PyRakLib
from pyraklib.protocol import OPEN_CONNECTION_REQUEST_1
from pyraklib.protocol import OPEN_CONNECTION_REQUEST_2
from pyraklib.protocol import DATA_PACKET_0
from pyraklib.protocol import DATA_PACKET_4
from pyraklib.protocol import EncapsulatedPacket
from pyraklib.protocol import CLIENT_CONNECT_DataPacket
from pyraklib.protocol import SERVER_HANDSHAKE_DataPacket
from pyraklib.protocol import CLIENT_HANDSHAKE_DataPacket
from pyraklib.protocol import ACK
from pyraklib.server import UDPServerSocket

src_port = 19133
dest_ip = "127.0.0.1"
dest_port = 19132

ClientId = 1234567

sock = UDPServerSocket(logging.getLogger("PyRakLib"), src_port, '0.0.0.0')
sock.socket.setblocking(True)

#OPEN_CONNECTION_REQUEST_1
print("OPEN_CONNECTION_REQUEST_1")
request1 = OPEN_CONNECTION_REQUEST_1()
request1.mtuSize = 1464
request1.encode()
sock.writePacket(request1.buffer, dest_ip, dest_port)

#OPEN_CONNECTION_REPLY_1
print("OPEN_CONNECTION_REPLY_1")
sock.readPacket()

#OPEN_CONNECTION_REQUEST_2
print("OPEN_CONNECTION_REQUEST_2")
request2 = OPEN_CONNECTION_REQUEST_2()
request2.clientID = ClientId
request2.serverAddress = (dest_ip, dest_port, 4)
request2.mtuSize = 1464
request2.encode();
sock.writePacket(request2.buffer, dest_ip, dest_port)

#OPEN_CONNECTION_REPLY_2
print("OPEN_CONNECTION_REPLY_2")
sock.readPacket()

#CLIENT_CONNECT_DataPacket
print("CLIENT_CONNECT_DataPacket")
pk = CLIENT_CONNECT_DataPacket()
pk.clientID = ClientId
pk.sendPing = 1000
pk.encode()

sendPk = EncapsulatedPacket()
sendPk.messageIndex = 0
sendPk.reliability = 0
sendPk.buffer = pk.buffer

packet = DATA_PACKET_4()
packet.seqNumber = 0
packet.packets.append(sendPk.toBinary())
packet.encode()
sock.writePacket(packet.buffer, dest_ip, dest_port)

#SERVER_HANDSHAKE_DataPacket or ACK (or NACK)
print("SERVER_HANDSHAKE_DataPacket")
while True:
    buf, src = sock.readPacket()
    if buf[0] == DATA_PACKET_0.getPID():
        dpk = DATA_PACKET_0()
        dpk.buffer = buf
        dpk.decode()
        ack = ACK()
        ack.packets = [ dpk.seqNumber ]
        ack.encode()
        sock.writePacket(ack.buffer, dest_ip, dest_port)
        break

#CLIENT_HANDSHAKE_DataPacket
print("CLIENT_HANDSHAKE_DataPacket")
pk2 = CLIENT_HANDSHAKE_DataPacket()
pk2.address = dest_ip
pk2.port = dest_port
pk2.systemAddresses = (
    ('0.0.0.0', 0, 4),
    ('0.0.0.0', 0, 4),
    ('0.0.0.0', 0, 4),
    ('0.0.0.0', 0, 4),
    ('0.0.0.0', 0, 4),
    ('0.0.0.0', 0, 4),
    ('0.0.0.0', 0, 4),
    ('0.0.0.0', 0, 4),
    ('0.0.0.0', 0, 4),
    ('0.0.0.0', 0, 4)
)
pk2.sendPing = 1000
pk2.sendPong = 2000
pk2.encode()

sendPk2 = EncapsulatedPacket()
sendPk2.messageIndex = 1
sendPk2.reliability = 0
sendPk2.buffer = pk2.buffer

packet2 = DATA_PACKET_4()
packet2.seqNumber = 2;
packet2.packets.append(sendPk2.toBinary())
packet2.encode()
sock.writePacket(packet2.buffer, dest_ip, dest_port)

print("###########  Finish!!  ###########");
