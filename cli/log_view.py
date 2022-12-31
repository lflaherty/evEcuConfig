#!/usr/bin/env python3
"""
Prints log data to terminal.
"""

from time import sleep
from argparse import ArgumentParser
import serial

from decode_common import MsgDecoder, MsgType
from serial_common import SerialHandler, SerialTx
from colors import bcolors

BAUD_RATE = 115200
STOP_BITS = serial.STOPBITS_ONE

ADDR_PC = 0x02
MSG_TYPE_LOG = 0x02
MSG_LEN_LOG = 43

OPT_RAW = False

"""
Handler method for a log message data
"""
def handle_log_data(msg_info):
  msg_data = msg_info['payload']
  crc_correct = msg_info['crc_correct']
  msg_str = ''.join([chr(x) for x in msg_data])

  global OPT_RAW
  if OPT_RAW:
    msg_str = repr(msg_str)
  
  if crc_correct:
    print(f'{msg_str}', end='', flush=True)
  else:
    print(f'{bcolors.FAIL}{msg_str}{bcolors.ENDC}', end='', flush=True)


def main():
  parser = ArgumentParser()
  parser.add_argument('port', help='Serial port to open')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                      help='Verbose decoding logging')
  parser.add_argument('-r', '--raw', action='store_true',
                      help='View output data without formatting')
  parser.add_argument('-b', '--bytes', dest='bytes', action='store_true',
                      help='Print each byte as it is read')
  args = parser.parse_args()
  
  if args.raw:
    global OPT_RAW
    OPT_RAW = True

  print(f'{bcolors.HEADER}Launching threads{bcolors.ENDC}')

  msg_log_decoder = MsgDecoder(
    self_address=ADDR_PC,
    msg_type=MsgType(
      name="LOG",
      type=MSG_TYPE_LOG,
      len=MSG_LEN_LOG,
      handler=handle_log_data,
    ),
    print_bytes=args.bytes,
    verbose=args.verbose
  )

  serial_handler = SerialHandler(
      port=args.port,
      baud_rate=BAUD_RATE,
      stop_bits=STOP_BITS,
  )
  serial_handler.add_decoder(msg_log_decoder)

  serial_tx = SerialTx(serial_handler)

  try:
    serial_handler.start()
    serial_tx.start()

    # Don't join serial_handler - this would block ctrl-C on windows
    serial_tx.join()
  except KeyboardInterrupt:
    print()
    print(f'{bcolors.HEADER}Quitting{bcolors.ENDC}')
  
  serial_handler.close_port()


if __name__ == '__main__':
  main()
