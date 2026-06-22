import time
from typing import Callable
import hid

reset = "\033[0m"
receive = "\033[95m"
send = "\033[96m"
macro = "\033[91m"
keyboard = "\033[93m"

usage_page = 0xFF60
usage = 0x61
report_length = 32


class device:
    CM_PING = 0x02
    CM_OPEN = 0x03
    CM_CLOSE = 0x04
    CM_ACK = 0x05
    MSG_TYPE_FN_SEND = 0x10
    MSG_TYPE_FN_RECV = 0x11
    MSG_TYPE_DC_SEND = 0x12
    MSG_TYPE_DC_RECV = 0x13
    MSG_TYPE_XM_SEND = 0x14
    MSG_TYPE_XM_RECV = 0x15
    MSG_TYPE_CMD = 0x20
    MSG_TYPE_SET_BRIGHTNESS = 0x30

    def __init__(
        self,
        vid,
        pid,
        onClose: Callable[["device"], None] = lambda x: None,
        debug=False,
    ):
        self.onClose = onClose
        self.vid = vid
        self.pid = pid
        self.debug = debug
        self.path = self.getInterface()
        self.device = None  
        self.name = "Unknown"

    def getInterface(self) -> str | None:
        device_interfaces = hid.enumerate(self.vid, self.pid)
        raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

        if len(raw_hid_interfaces) == 0:
            return None

        path = raw_hid_interfaces[0]['path']
        interface = hid.Device(path=path)

        print(f"Manufacturer: {interface.manufacturer}")
        print(f"Product: {interface.product}")
        interface.close()
        return path

    def open(self):
        self.path = self.getInterface()
        if not self.path:
            raise IOError(f"path is unknown")
        self.device = hid.Device(path=self.path)
        self.device.nonblocking = True
        if not self.device:
            return False
        self.name = str(self.device.product)
        self.send(self.CM_OPEN)

    def close(self):
        try:
            try:
                self.onClose(self)
            except:
                pass
            self.send(self.CM_CLOSE)
            if self.device:
                self.device.close()
        except (hid.HIDException, IOError) as e:
            pass

    def send(self, type, data=[0x00]):
        if isinstance(data, int):
            data = [data]
        elif not isinstance(data, list):
            raise TypeError("data must be an int or a list of ints")
        if self.device is None:
            raise IOError("device is not open")
        msg = [type] + data[:31] + [0] * (31 - len(data))
        msg = bytes(msg[:32] + [0x00] * (32 - len(msg)))
        if self.debug:
            print(
                macro if "macro" in self.name.lower() else keyboard,
                self.name.ljust(35),
                send + "s" + reset,
                self.asText(msg).ljust(25),
                self.asByte(msg),
            )
        self.device.write(msg)
        start = time.time_ns()
        if type == self.CM_ACK:
            return True
        while time.time_ns() - start < 10_000_000:
            response = self.read()
            if response and response[0] == self.CM_ACK and response[1] == type:
                return True
        return False

    def read(self, size=32) -> bytes | None:
        if not self.device: 
            raise IOError("device is not open")
        response = self.device.read(size)
        if not response:
            return None
        if self.debug:
            print(
                macro if "macro" in self.name.lower() else keyboard,
                self.name.ljust(35),
                receive + "r" + reset,
                self.asText(response).ljust(25),
                self.asByte(response),
            )
        if response[0] != self.CM_ACK:
            self.send(self.CM_ACK, response[0])

        return response

    def asByte(self, bin):
        return "\\x" + "\\x".join(("00" + hex(i)[2::])[-2::] for i in bin)

    def asText(self, msg):
        for var, value in device.__dict__.items():
            if (var.startswith("MSG_TYPE_") or var.startswith("CM_")) and value == msg[
                0
            ]:
                return var
        return "Unknown"
