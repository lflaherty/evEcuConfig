#!/usr/bin/env python3
"""
Prints log data to terminal.
"""

from time import sleep
from argparse import ArgumentParser
import serial

from decode_common import MsgDecoder, MsgType
from encode_common import encode_message
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
def handle_log_data(msg_data, crc_correct):
  msg_str = ''.join([chr(x) for x in msg_data])

  global OPT_RAW
  if OPT_RAW:
    msg_str = repr(msg_str)
  
  if crc_correct:
    print(f'{msg_str}', end='', flush=True)
  else:
    print(f'{bcolors.FAIL}{msg_str}{bcolors.ENDC}', end='', flush=True)


def send_cmd_pdm(serial_handler: SerialHandler):
  payload = [
    0, 0,
    0, # PDM1
    0, # PDM2
    0, # PDM3
    0, # PDM4
    0, # PDM5
    1, # PDM6
  ]

  cmd_message = encode_message(
    target_addr=0x01,
    function=0x102,
    payload=payload,
  )

  serial_handler.serial.write(cmd_message)


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

    sleep(1) # Defer to a bit after script start before sending command
    send_cmd_sdc(serial_handler)

    serial_handler.join()
    serial_tx.join()
  except KeyboardInterrupt:
    print()
    print(f'{bcolors.HEADER}Quitting{bcolors.ENDC}')
  
  serial_handler.close_port()


if __name__ == '__main__':
  main()
