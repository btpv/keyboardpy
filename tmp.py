# #!/usr/bin/env python3
# import glob
# import threading
# import time
# import os

# def read_hidraw(path):
#     try:
#         print(f"[+] Opening {path}")
#         with open(path, "rb", buffering=0) as f:
#             while True:
#                 data = f.read(64)  # HID reports are often 8–64 bytes, varies by device
#                 if data:
#                     print(f"[{path}] {data.hex(' ')}")
#                 else:
#                     time.sleep(0.01)

#     except PermissionError:
#         print(f"[-] Permission denied: {path}")
#     except FileNotFoundError:
#         print(f"[-] Disappeared: {path}")
#     except Exception as e:
#         print(f"[-] Error on {path}: {e}")

# def main():
#     devices = sorted(glob.glob("/dev/hidraw*"))

#     if not devices:
#         print("No hidraw devices found.")
#         return

#     threads = []

#     for dev in devices:
#         t = threading.Thread(target=read_hidraw, args=(dev,), daemon=True)
#         t.start()
#         threads.append(t)

#     print(f"[+] Started {len(threads)} threads.")

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("\n[+] Exiting...")

# if __name__ == "__main__":
#     main()


import sys
import hid

vendor_id     = 0x32AC
product_id    = 0x0013

usage_page    = 0xFF60
usage         = 0x61
report_length = 32

def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])

    print(f"Manufacturer: {interface.manufacturer}")
    print(f"Product: {interface.product}")

    return interface

def send_raw_report(data):
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        sys.exit(1)

    request_data = [0x00] * (report_length + 1) # First byte is Report ID
    request_data[1:len(data) + 1] = data
    request_report = bytes(request_data)

    print("Request:")
    print(request_report)

    try:
        interface.write(request_report)

        response_report = interface.read(report_length, timeout=1000)

        print("Response:")
        print(response_report)
    finally:
        interface.close()

if __name__ == '__main__':
    send_raw_report([
        0x41
    ])