#!/usr/bin/env python3
"""
Prints log data to terminal.
"""

from time import sleep
from argparse import ArgumentParser
from threading import Thread
import serial
import zlib

# Options
VERBOSE = False
RAW = False
PRINT_BYTES = False

# Constants
CHAR_COLON = 0x3A
CHAR_CR = 0x0D
CHAR_LF = 0x0A

BAUD_RATE = 115200
STOP_BITS = serial.STOPBITS_ONE

ADDR_PC = 0x02
MSG_TYPE_LOG = 0x02
EXPECTED_LEN = 43
EXPECTED_DATA_LEN = EXPECTED_LEN - 7  # subtracting frame bytes (start, crc, addr, ...)


class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


def open_port(port):
  print(f'{bcolors.HEADER}Opening port {port}{bcolors.ENDC}')
  ser = serial.Serial(port, BAUD_RATE, stopbits=STOP_BITS, timeout=0.5)
  return ser


def close_port(s):
  print(f'{bcolors.HEADER}Closing serial{bcolors.ENDC}')
  s.close()


"""
Handler method for a log message data
"""
def handle_log_data(msg_data, crc_correct):
  msg_str = ''.join([chr(x) for x in msg_data])
  if RAW:
    msg_str = repr(msg_str)
  
  if crc_correct:
    print(f'{msg_str}', end='', flush=True)
  else:
    print(f'{bcolors.FAIL}{msg_str}{bcolors.ENDC}', end='', flush=True)


"""
Handler method for serial data
"""
def handle_data(msg):
  if msg['addr'] != ADDR_PC:
    if VERBOSE:
      addr = msg['addr']
      print(f'{bcolors.OKBLUE}Unexpected address {addr}{bcolors.ENDC}')
    return
  if VERBOSE:
    print(f'{bcolors.OKBLUE}Invoking message handler{bcolors.ENDC}')

  if msg['msg_type'] == MSG_TYPE_LOG:
    handle_log_data(msg['payload'], msg['crc_correct'])
  else:
    if VERBOSE:
      msg_type_hex = hex(msg['msg_type'])
      print(f'{bcolors.OKBLUE}Unkown message type {msg_type_hex}{bcolors.ENDC}')


"""
Returns None if no msg received
Returns dict summarizing received data.
"""
def try_decode(msg):
  if len(msg) != EXPECTED_LEN:
    return None
  
  expected_bytes = [
    msg[0] == CHAR_COLON,
    msg[-2] == CHAR_CR,
    msg[-1] == CHAR_LF,
  ]
  if not all(expected_bytes):
    return None
  
  # Get CRC from message
  msg_crc = 0
  offset = 24
  for byte in msg[-6:-2]:
    msg_crc = msg_crc | (byte << offset)
    offset -= 8
  
  msg[-6:-2] = 4*[0]

  calc_crc = zlib.crc32(bytes(msg))
  if VERBOSE:
    print(f'{bcolors.OKBLUE}CRC mismatch. Expecting', hex(calc_crc),
          'got', hex(msg_crc), f'{bcolors.ENDC}')
  
  crc_correct = calc_crc == msg_crc
  if not crc_correct and VERBOSE:
    print(f'{bcolors.OKBLUE}CRC mismatch. Expecting', hex(calc_crc),
          'got', hex(msg_crc), f'{bcolors.ENDC}')
  
  msg_type = (msg[1] << 8) | msg[2]
  addr = (msg[3] << 8) | msg[4]
  recv_data = msg[5:-6]

  ret = {
    'payload': recv_data,
    'msg_type': msg_type,
    'addr': addr,
    'crc_calc': calc_crc,
    'crc_recv': msg_crc,
    'crc_correct': crc_correct
  }
  return ret


"""
Wait for data and try to decode it.
"""
def recv(s):
  msg_buffer = []
  print(f'{bcolors.HEADER}Listening for data{bcolors.ENDC}')
  print()

  while True:
    # Receive new bytes
    b = s.read(10)
    if not b:
      continue

    # can receive multiple bytes at once
    n = len(b)
    b = int.from_bytes(b, 'little')
    for i in range(n):
      current_byte = (b >> (i*8)) & 0xFF
      msg_buffer.append(current_byte)

      if PRINT_BYTES:
        print(f'Received "{bcolors.OKCYAN}', hex(current_byte), f'{bcolors.ENDC}"')

    # Should always start with a ':' character, so pop all bytes that aren't that
    while len(msg_buffer) > 0 and msg_buffer[0] != CHAR_COLON:
      msg_buffer.pop(0)
    
    if VERBOSE:
      print(f'{bcolors.OKBLUE}Buffer contents:', msg_buffer, '({})'.format(len(msg_buffer)), f'{bcolors.ENDC}')
    
    # Wait until we have enough bytes
    if len(msg_buffer) >= EXPECTED_LEN:
      if VERBOSE:
        print(f'{bcolors.OKBLUE}Attempting decode{bcolors.ENDC}')
      msg_received = try_decode(msg_buffer[:EXPECTED_LEN])
      if msg_received:
        if VERBOSE:
          print(f'{bcolors.OKBLUE}Found valid message{bcolors.ENDC}')

        handle_data(msg_received)

        msg_buffer = msg_buffer[EXPECTED_LEN:]
      else:
        msg_buffer = msg_buffer[1:]


def send(s):
  while True:
    x = input()
    print(f'{bcolors.HEADER}Sending', repr(x), f'{bcolors.ENDC}')
    s.write(x.encode('utf-8'))


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

  if args.verbose:
    global VERBOSE
    VERBOSE = True
  
  if args.raw:
    global RAW
    RAW = True
  
  if args.bytes:
    global PRINT_BYTES
    PRINT_BYTES = True
  
  try:
    s = open_port(args.port)
    print(f'{bcolors.HEADER}Launching threads{bcolors.ENDC}')
    thread_recv = Thread(target=recv, args=(s,), daemon=True)
    thread_send = Thread(target=send, args=(s,), daemon=True)

    thread_recv.start()
    thread_send.start()

    thread_recv.join()
    thread_send.join()
  except KeyboardInterrupt:
    print()
    print(f'{bcolors.HEADER}Quitting{bcolors.ENDC}')
  
  close_port(s)


if __name__ == '__main__':
  main()
