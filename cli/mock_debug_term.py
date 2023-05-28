#!/usr/bin/env python3
"""
Prints log data and debug data to terminal.
Sends debug messages.

# TODO dump state update data to files.
"""

from time import sleep
from argparse import ArgumentParser

from decode_common import MsgDecoder, MsgType, MSG_TYPE_LEN_VARIABLE
from encode_common import encode_message
from serial_mock import SerialHandler, SerialTx
from colors import bcolors

BAUD_RATE = 115200
STOP_BITS = 1

ADDR_PC = 0x02
# "Mock" log messages are shorter and have a different messagea type
MSG_TYPE_LOG = 0x40
MSG_LEN_LOG = 14
MSG_TYPE_DEBUGLOG = 0x09
# ECU -> PC debug messages are variable length
# PC -> ECU debug messages are fixed length of 8
MSG_LEN_TX_DEBUGLOG = 8
MSG_TYPE_STATE = 0x01
MSG_LEN_STATE = 18

FIELD_ID_NAMES = {
  0x0001: 'SDC',
  0x0002: 'PDM',
  0x0003: 'BMS Max cell voltage',
  0x0004: 'BMS Max cell voltage ID',
  0x0005: 'BMS Max cell temp',
  0x0006: 'BMS Max cell temp ID',
  0x0007: 'BMS DC current',
  0x0008: 'BMS Pack voltage',
  0x0009: 'BMS SOC',
  0x000A: 'BMS Counter',
  0x000B: 'BMS Fault',
}

OPT_RAW = False

"""
Handler method for log message data
"""
def handle_log_data(msg_info):
  msg_data = msg_info['payload']
  crc_correct = msg_info['crc_correct']
  msg_str = ''.join([chr(x) for x in msg_data])

  global OPT_RAW
  if OPT_RAW:
    msg_str = repr(msg_str)

  if crc_correct:
    print(f'{bcolors.OKBLUE}{msg_str}{bcolors.ENDC}', end='', flush=True)
  else:
    print(f'{bcolors.FAIL}{msg_str}{bcolors.ENDC}', end='', flush=True)


"""
Handler method for debug log message data
"""
def handle_debuglog_data(msg_info):
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


def tx_send_handler(serial_tx: SerialTx, tx_str):
  # Split tx_str into groups of 8
  chunks = [tx_str[i:i+MSG_LEN_TX_DEBUGLOG]
            for i in range(0, len(tx_str), MSG_LEN_TX_DEBUGLOG)]
  for chunk in chunks:
    # Convert chunk string into array of ASCII bytes
    chunk = [ord(c) for c in chunk]
    if len(chunk) != MSG_LEN_TX_DEBUGLOG:
      # needs to be padded to MSG_LEN_TX_DEBUGLOG
      missing_bytes = MSG_LEN_TX_DEBUGLOG - len(chunk)
      chunk += [0]*missing_bytes

    debug_msg = encode_message(
      target_addr=0x01,
      function=MSG_TYPE_DEBUGLOG,
      payload=chunk,
    )
    serial_tx.write_bytes(debug_msg)


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
  msg_debug_log_decoder = MsgDecoder(
    self_address=ADDR_PC,
    msg_type=MsgType(
      name="DEBUGLOG",
      type=MSG_TYPE_DEBUGLOG,
      len=MSG_TYPE_LEN_VARIABLE,
      handler=handle_debuglog_data,
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
  serial_handler.add_decoder(msg_debug_log_decoder)
  serial_handler.add_decoder(msg_state_decoder)

  serial_tx = SerialTx(
    serial_handler=serial_handler,
    send_handler=tx_send_handler,
  )

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
