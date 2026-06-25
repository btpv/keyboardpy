# # #!/usr/bin/env python3
# # import glob
# # import threading
# # import time
# # import os

# # def read_hidraw(path):
# #     try:
# #         print(f"[+] Opening {path}")
# #         with open(path, "rb", buffering=0) as f:
# #             while True:
# #                 data = f.read(64)  # HID reports are often 8–64 bytes, varies by device
# #                 if data:
# #                     print(f"[{path}] {data.hex(' ')}")
# #                 else:
# #                     time.sleep(0.01)

# #     except PermissionError:
# #         print(f"[-] Permission denied: {path}")
# #     except FileNotFoundError:
# #         print(f"[-] Disappeared: {path}")
# #     except Exception as e:
# #         print(f"[-] Error on {path}: {e}")

# # def main():
# #     devices = sorted(glob.glob("/dev/hidraw*"))

# #     if not devices:
# #         print("No hidraw devices found.")
# #         return

# #     threads = []

# #     for dev in devices:
# #         t = threading.Thread(target=read_hidraw, args=(dev,), daemon=True)
# #         t.start()
# #         threads.append(t)

# #     print(f"[+] Started {len(threads)} threads.")

# #     try:
# #         while True:
# #             time.sleep(1)
# #     except KeyboardInterrupt:
# #         print("\n[+] Exiting...")

# # if __name__ == "__main__":
# #     main()


# import sys
# import hid

# vendor_id     = 0x32AC
# product_id    = 0x0013

# usage_page    = 0xFF60
# usage         = 0x61
# report_length = 32

# def get_raw_hid_interface():
#     device_interfaces = hid.enumerate(vendor_id, product_id)
#     raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

#     if len(raw_hid_interfaces) == 0:
#         return None

#     interface = hid.Device(path=raw_hid_interfaces[0]['path'])

#     print(f"Manufacturer: {interface.manufacturer}")
#     print(f"Product: {interface.product}")

#     return interface

# def send_raw_report(data):
#     interface = get_raw_hid_interface()

#     if interface is None:
#         print("No device found")
#         sys.exit(1)

#     request_data = [0x00] * (report_length + 1) # First byte is Report ID
#     request_data[1:len(data) + 1] = data
#     request_report = bytes(request_data)

#     print("Request:")
#     print(request_report)

#     try:
#         interface.write(request_report)

#         response_report = interface.read(report_length, timeout=1000)

#         print("Response:")
#         print(response_report)
#     finally:
#         interface.close()

# if __name__ == '__main__':
#     send_raw_report([
#         0x41
#     ])

import json

# width = 4
with open("/home/btpv/qmk_firmware/keyboards/framework/macropad/keyboard.json") as f:
    jsonfile = ""
    for line in f.readlines():
        if "//" in line:
            if "\"" in line:
                quotesOpen = False
                lastchar = ''
                for i,char in enumerate(line):
                    if char == '"':
                        quotesOpen = not quotesOpen
                    if not quotesOpen and lastchar+char == "//":
                        line = line[0:i-1]
                        break
                    lastchar = char
            else:
                line = line[0:line.index("//")]
        jsonfile += line
    info = json.loads(jsonfile)
layout = info["layouts"]["LAYOUT"]["layout"]
leds = info["rgb_matrix"]["layout"]
mappingOrder: list[list[int]] = [[255 for _ in range(4)] for _ in range(8)]
for index,key in enumerate(layout):
    mappingOrder[key["matrix"][0]][key["matrix"][1]] = index
print("{",end="")
for row in mappingOrder:
    print("\n    {",end="")
    for item in row:
        print(f"{item:3}",end=",")
    print("\b},",end="")
print("\b \n}")    
# exit()
ledMap: list[list[list[int]]] = [[[] for _ in range(4)] for _ in range(8)]
for key in layout:
    for index,led in enumerate(leds):
        if led["matrix"] == key["matrix"]:
            ledMap[key["matrix"][0]][key["matrix"][1]].append(index)
length = 8
print("{",end="")
for row in ledMap:
    print("\n    {",end="")
    for item in row:
        print("\n        {",end="")
        for i in range(length):
            if i < len(item):
                print(f"{item[i]:3}",end=",")
            else:
                print("255",end=",")
        print("\b},",end="")
    print("\b \n    },",end="")
print("\b \n}")

exit()   
# layoutIDs = [
#     [int(i[1::]) for i in row.split(",")]
#     for row in """ K110,  K112,  K113,  K114,  K115,  K116,  K117,  K118,  K119,  K120,  K121,  K122,  K123,   K76
#         K1,    K2,    K3,    K4,    K5,    K6,    K7,    K8,    K9,   K10,   K11,   K12,   K13,   K15
#         K16,   K17,   K18,   K19,   K20,   K21,   K22,   K23,   K24,   K25,   K26,   K27,   K28,   K29
#         K30,   K31,   K32,   K33,   K34,   K35,   K36,   K37,   K38,   K39,   K40,   K41,      K43    
#         K44,   K46,   K47,   K48,   K49,   K50,   K51,   K52,   K53,   K54,   K55,        K57         
#         K58,   K59,  K127,   K60,                    K61,       K62,   K64,   K79,    K83, K84,    K89""".replace(
#         " ", ""
#     ).split(
#         "\n"
#     )
# ]
# print(layout)
# matrixBase = [
#     [int(i[1::]) if i != "KC_NO" else None for i in row.split(",")]
#     for row in """ K48,   K76,   K17,   K62,  KC_NO,  K47,   K49,   K52,   K54,   K57,  K53,  KC_NO,   K64,   K55,   K41, KC_NO
#         KC_NO, KC_NO, KC_NO,   K60,   K61,   K46,   K50,   K51,   K84,   K44, KC_NO, KC_NO,   K58,   K83,   K43,  K119
#         KC_NO, KC_NO,   K59, KC_NO,   K19,  K113,   K35,   K36,   K29, KC_NO,  K118, KC_NO, KC_NO,   K12, KC_NO,   K89
#         KC_NO,  K127,   K16, KC_NO,  K115,  K112,   K21,   K22,   K25, KC_NO,  K117,  K120, KC_NO,  K123, KC_NO, KC_NO
#         KC_NO, KC_NO,    K1, KC_NO,   K30,   K32,    K6,    K7,  K121, KC_NO,  K116, KC_NO, KC_NO,   K11,   K13, KC_NO
#         KC_NO, KC_NO,    K2, KC_NO,    K4,    K3,    K5,    K8,   K10, KC_NO,    K9, KC_NO, KC_NO,   K26,   K15, KC_NO
#         KC_NO, KC_NO, KC_NO, KC_NO,  K114,   K18,   K20,   K23,  K122, KC_NO,   K24,   K79, KC_NO,   K27,   K28, KC_NO
#         KC_NO, KC_NO,  K31,  KC_NO, KC_NO,  K110,   K34,   K37,   K39, KC_NO,   K38, KC_NO, KC_NO,   K40,   K33, KC_NO""".replace(
#         " ", ""
#     ).split(
#         "\n"
#     )
# ]

# print(matrixBase)
# x,y = 0,0

# lastY = layout[0]["y"]  
# for item in layout:
#     if item["y"] != lastY and item["label"] != "↓":
#         y += 1
#         x = 0
#         lastY = item["y"]
#     id = layoutIDs[y][x]
#     mx,my = None,None
#     for my,matrixRow in enumerate(matrixBase):
#         if id in matrixRow:
#             mx = matrixRow.index(id)
#             break
#     if mx is None:
#         raise Exception(f"Could not find {id} in matrix")
#     if my is None:
#         raise Exception(f"Could not find {id} in matrix")
#     matrix = [mx,my]
#     print(json.dumps({"matrix":matrix,**item})+",")
#     x += 1
        
        


# # print(json.dumps(layout).replace("}, {","},\n{"))

















removeChars = "├┴┬─┼┤└┘┌┐"
rgbMatrix = """
┌─────┬───┬───┬───┬───┬───┬───┬───┬                                ┬───┬───┬───┬────┬───┬─────┐
│43 31│20 │ 8 │ 2 │14 │26 │37 │49 │                                │ 8 │14 │20 │2 38│32 │445 0│
├───┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬                              ┴─┬─┴─┬─┴─┬─┴─┬──┴┬──┴─────┤
│42 │30 │19 │ 7 │ 1 │13 │25 │36 │48 │                                │26 │25 │37 │31 │43  49  │
├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴                              ┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬──────┤
│41 29│18 │ 6 │ 0 │12 │24 │35 │47 │                                │ 7 │13 │19 │ 1 │36 │ 42   │
├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴                             ┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴──────┤
│334522│10 │ 4 │16 │28 │39 │51 │                                │ 6 │12 │18 │ 0 │24 │ 30   48 │
├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴                              ┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─────────┤
│32 21 9 │ 3 │15 │27 │38 │50 │                                │ 9 │15 │21 │ 3 │27 │33 45 51 52│
├────┬───┼───┼───┼───┴───┴───┴        ┬───┼       ┼───┴───┴───┴───┴───┼───┼───┼───┴┬───┬──────┤
"""
# def remove_empty_lists(obj):
#     if isinstance(obj, list):
#         result = [remove_empty_lists(item) for item in obj if item != []]
#         return [item for item in result if item != []]
#     return obj
# # │    │   │   │   │                    │   │       │                   │   │   │    │39 │      │
# # │44 5│   │11 │17 │                    │ 5 │       │11 17 23 10  16  22│ 4 │28 │ 34 ├───┤ 46   │
# # │    │   │   │   │                    │   │       │                   │   │   │    │40 │      │
# # └────┴   ┴───┴───┴─                   ┴───┴───┴───┴───────────────────┴───┴───┴────┴───┴──────┘                         
# # correctOrder = [None for i in range(len(layout))]
# for i in removeChars:
#     rgbMatrix = rgbMatrix.replace(i, "")
# rgbMatrixIndexes = [[[[int(l) for l in k.split(" ") if l != ''] for k in j.split("│") if k != ""]for j in i.split("           ")] for i in rgbMatrix.split("\n")]
# rgbMatrixIndexes = remove_empty_lists(rgbMatrixIndexes)
# matrixLocations = [{}]
# for rowIndex, row in enumerate(rgbMatrixIndexes):
#     for colIndex, keys in enumerate(row):
#         for key in keys:
#             matrixLocations[key] = layout[rowIndex][colIndex]["matrix"]
# for driver in matrixLocations:
#     for i,v in sorted(driver.items()):
#         print(f"{i:>2} {v}")
    
# pass
# exit()

offset = 0
notincluded = []
driver = "1"
leds = ""   
for i in range(66 + 1):
    print(f"#define LED_{driver}_{i:<2} {{0x0{driver},0x{i*3+2:02x},0x{i*3+1:02x},0x{i*3+0:02x}}}")
    leds += f"    LED_{driver}_{i},\n"
print(leds[:-2])
# for i,v in enumerate(rgbMatrixIndexes):
#     correctOrder[v] = layout[i]
#     correctOrder[v]["flags"] = 4
# print(json.dumps(correctOrder).replace("}, {","},\n{"))
