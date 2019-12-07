import pyshark


# all the UDP streams were exfiltrating to port 22
capture = pyshark.FileCapture("capture.pcap", display_filter="udp.port eq 22")

flag = ""

for packet in capture:
    # iterating through all packets from the matching UDP streams
    # the source port of each packet is used to
    # exfiltrate each character of the flag
    flag += chr(int(packet.udp.srcport) - 5000)

print(flag)
