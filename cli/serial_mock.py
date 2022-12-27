from threading import Thread
from time import sleep

from colors import bcolors

# Constants
CHAR_COLON = 0x3A
CHAR_CR = 0x0D
CHAR_LF = 0x0A

####### MOCK DATA FOR TESTING #######
TEST_MSGS = [
  [0xFF, CHAR_COLON, 0x00, 0x02, 0x00, 0x40, ord('H'), ord('e'), ord('l'), 0xb9, 0x0a, 0xa4, 0xbd, CHAR_CR, CHAR_LF],
  [CHAR_COLON, 0x00, 0x02, 0xAF],
  [CHAR_COLON, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, CHAR_LF],
  [0xFF, CHAR_COLON, 0x00, 0x02, 0x00, 0x40, ord('l'), ord('o'), ord('\n'), 0x00, 0x00, 0x00, 0x00, CHAR_CR, CHAR_LF],
  [0xFF, CHAR_COLON, 0x00, 0x02, 0x00, 0x40, ord('w'), ord('h'), ord('e'), 0x00, 0x48, 0xfe, 0xa9, CHAR_CR, CHAR_LF],
  [0xFF, CHAR_COLON, 0x00, 0x02, 0x00, 0x40, ord('e'), ord('e'), ord('e'), 0x19, 0x7b, 0x81, 0x8f, CHAR_CR, CHAR_LF],
  [0xFF, CHAR_COLON, 0x00, 0x02, 0x00, 0x40, ord('!'), ord('!'), ord('\n'), 0x4a, 0x2c, 0x23, 0x9f, CHAR_CR, CHAR_LF],
]

class SerialHandler:
    def __init__(
        self,
        port,
        baud_rate,
        stop_bits
    ):
        self.test_msg_i, self.test_msg_j = 0, 0
        self.decoders = []
        self.thread_recv = Thread(target=self.recv, daemon=True)
        self.open_port(
            port=port,
            baud_rate=baud_rate,
            stop_bits=stop_bits
        )

    def open_port(
        self,
        port,
        baud_rate,
        stop_bits,
    ):
        print(f'{bcolors.HEADER}Opening port {port}{bcolors.ENDC}')

    def close_port(self):
        print(f'{bcolors.HEADER}Closing serial{bcolors.ENDC}')

    def recv(self):
        print(f'{bcolors.HEADER}Listening for data{bcolors.ENDC}')
        print()

        while True:
            # Receive new bytes
            b = self._mock_get_byte()
            if not b:
                continue

            for decoder in self.decoders:
                decoder.recv_bytes(b)

    def _mock_get_byte(self):
        if self.test_msg_j >= len(TEST_MSGS):
            return None
        if self.test_msg_i >= len(TEST_MSGS[self.test_msg_j]):
            self.test_msg_j += 1
            self.test_msg_i = 0
            sleep(0.3) # just sleep on increment to new rows
            return None

        b = TEST_MSGS[self.test_msg_j][self.test_msg_i]
        self.test_msg_i += 1
        # Return as an array to emulate pyserial responses
        return [b]

    def start(self):
        self.thread_recv.start()

    def join(self):
        self.thread_recv.join()
    
    def add_decoder(self, decoder):
        self.decoders.append(decoder)


class SerialTx:
    def __init__(
        self,
        serial_handler
    ):
        self.serial_handler = serial_handler
        self.thread = Thread(target=self.send, daemon=True)
    
    def start(self):
        self.thread.start()
    
    def send(self):
        while True:
            x = input()
            print(f'{bcolors.HEADER}Sending', repr(x), f'{bcolors.ENDC}')

    def join(self):
        self.thread.join()
