from segments import Ethernet, Ip, Tcp, Http

class Sequencer:
    def __init__(self):
        self.ether_seg = Ethernet("00cb51d0aa8cc8d3ff4498380800")
        self.ip_seg    = Ip("45000208dc104000800605b2c0a801396813ed38")
        self.tcp_seg   = Tcp("dd0a00509e5a0edbc12c15ee50180404b7150000")
        self.http_seg  = Http("00cb51d0aa8cc8d3ff4498380800")

    def sequence(self):
        print(self.ether_seg.getOutput())
        print(self.ip_seg.getOutput())
        print(self.tcp_seg.getOutput())
        print(self.http_seg.getOutput())