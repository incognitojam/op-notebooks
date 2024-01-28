#!/usr/bin/env python3

from scapy.all import wrpcap
from scapy.layers.can import CAN

from openpilot.tools.lib.logreader import LogReader


def write_can_to_pcap(log_reader: LogReader, filename: str, bus: int, append=False):
  packets = []
  for msg in log_reader:
    if msg.which() != 'can':
      continue
    for can in msg.can:
      if (can.src % 64) not in [0, 1, 2]:
        print(can.src, can.src % 64)
      
    packets.extend(
      CAN(
        identifier=can.address,
        length=len(can.dat),
        data=can.dat,
      )
      for can in msg.can
      if (can.src % 64) == bus
    )
  wrpcap(filename, packets, append=append)


if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(description='Convert openpilot log to pcap')
  parser.add_argument('route_or_segment_name', type=str, help='The route or segment name to convert')
  parser.add_argument('bus', type=int, help='the can data bus to convert')
  parser.add_argument('pcap', type=str, help='path to pcap')
  parser.add_argument('--append', action='store_true', help='append to pcap')
  args = parser.parse_args()

  log_reader = LogReader(args.route_or_segment_name)
  write_can_to_pcap(log_reader, args.pcap, args.bus, append=args.append)
