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
MSG_TYPE_STATE = 0x01
MSG_LEN_STATE = 18

FIELD_ID_NAMES = {
  0x0001: 'SDC',
  0x0002: 'PDM',
}

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


"""
Handler method for state message data
"""
def handle_state_data(msg_info):
  msg_data = msg_info['payload']
  crc_correct = msg_info['crc_correct']
  if crc_correct:
    field_id = (msg_data[0] << 8) | msg_data[1]
    field_len = msg_data[2]
    value = 0
    for i in range(field_len):
      ith_byte = msg_data[6 - i]
      value |= ith_byte << (i*8)

    if field_id not in FIELD_ID_NAMES:
      print('Unexpected field ID', hex(field_id))
      return

    print('State Update', FIELD_ID_NAMES[field_id], hex(value))


def send_cmd_pdm(serial_handler: SerialHandler):
  print(f'{bcolors.HEADER}Sending PDM control{bcolors.ENDC}')
  payload = [
    0, 0,
    0, # PDM1
    0, # PDM2
    0, # PDM3
    0, # PDM4
    0, # PDM5
    0, # PDM6
  ]

  cmd_message = encode_message(
    target_addr=0x01,
    function=0x102,
    payload=payload,
  )

  serial_handler.serial.write(cmd_message)
  print(f'{bcolors.HEADER}Sent PDM control{bcolors.ENDC}')


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
  msg_state_decoder = MsgDecoder(
    self_address=ADDR_PC,
    msg_type=MsgType(
      name="STATE",
      type=MSG_TYPE_STATE,
      len=MSG_LEN_STATE,
      handler=handle_state_data,
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
  serial_handler.add_decoder(msg_state_decoder)

  serial_tx = SerialTx(serial_handler)

  try:
    serial_handler.start()
    serial_tx.start()

    sleep(1) # Defer to a bit after script start before sending command
    send_cmd_pdm(serial_handler)

    # Don't join serial_handler - this would block ctrl-C on windows
    serial_tx.join()
  except KeyboardInterrupt:
    print()
    print(f'{bcolors.HEADER}Quitting{bcolors.ENDC}')

  serial_handler.close_port()


if __name__ == '__main__':
  main()
