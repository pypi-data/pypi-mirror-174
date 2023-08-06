#!/usr/bin/env python3

import socket
import sys
import time
import json
import datetime
import argparse
import select

try:
    from Cryptodome.Cipher import AES # provided by pycryptodome
    from Cryptodome.Random import get_random_bytes # pycryptodome
except:
    from Crypto.Cipher import AES # provided by pycryptodome
    from Crypto.Random import get_random_bytes # pycryptodome


def sendMsg(s, con, aes):
    print("Sending: " + s)
    plain = s.encode('utf-8')
    while len(plain) % 16:
        plain = plain + bytes([0x20])

    cipher = aes.encrypt(plain)

    while True:
        try:
            con.send(bytes([len(cipher) // 256, len(cipher) % 256, 0, 2]) + cipher)
            return
        except socket.timeout:
            print("Send timed out, retrying...")
            pass



class _HelpAction(argparse._HelpAction):

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()

        # retrieve subparsers from parser
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)]
        # there will probably only be one subparser_action,
        # but better save than sorry
        for subparsers_action in subparsers_actions:
            # get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                print("subcommand {}:".format(choice))
                print(subparser.format_help())

        parser.exit()

def set_thingsboard(args):
    tcp, udp = set_up_sockets(args)
    con, address = connect_sockets(tcp, udp)
    message_queue = [(json.dumps( { "type" : "backend", "link_enabled" :  (args.permission == "enable")}), 100)]
    send_message_queue(args, message_queue, con, address)
def set_ota(args):
    tcp, udp = set_up_sockets(args)
    con, address = connect_sockets(tcp, udp)
    message_queue = [(json.dumps( { "type" : "fw_update", "url" : args.url}), 300)]
    send_message_queue(args, message_queue, con, address)
def set_ping(args):
    tcp, udp = set_up_sockets(args)
    con, address = connect_sockets(tcp, udp)
    message_queue = [(json.dumps( { "type" : "ping" }), 800)]
    send_message_queue(args, message_queue, con, address)
def set_factory_reset(args):
    tcp, udp = set_up_sockets(args)
    con, address = connect_sockets(tcp, udp)
    message_queue = [(json.dumps( { "type" : "factory_reset" }), 500)]
    send_message_queue(args, message_queue, con, address)
def set_reboot(args):
    tcp, udp = set_up_sockets(args)
    con, address = connect_sockets(tcp, udp)
    message_queue = [(json.dumps( { "type" : "reboot" }), 100)]
    send_message_queue(args, message_queue, con, address)
def set_state_request(args):
    tcp, udp = set_up_sockets(args)
    con, address = connect_sockets(tcp, udp)
    get_dict = {"type":"request", "action":"get",}
    if args.power or args.all:
        get_dict["power"] = None
    if args.cleaning or args.all:
        get_dict["cleaning"] = None
    if args.beeping or args.all:
        get_dict["beeping"] = None
    if args.battery or args.all:
        get_dict["battery"] = None
    if args.sidebrush or args.all:
        get_dict["sidebrush"] = None
    if args.rollingbrush or args.all:
        get_dict["rollingbrush"] = None
    if args.filter or args.all:
        get_dict["filter"] = None
    if args.carpetbooster or args.all:
        get_dict["carpetbooster"] = None
    if args.area or args.all:
        get_dict["area"] = None
    if args.time or args.all:
        get_dict["time"] = None
    if args.calibrationtime or args.all:
        get_dict["calibrationtime"] = None
    if args.workingmode or args.all:
        get_dict["workingmode"] = None
    if args.workstatus or args.all:
        get_dict["workstatus"] = None
    if args.suction or args.all:
        get_dict["suction"] = None
    if args.water or args.all:
        get_dict["water"] = None
    if args.direction or args.all:
        get_dict["direction"] = None
    if args.errors or args.all:
        get_dict["errors"] = None
    if args.cleaningrec or args.all:
        get_dict["cleaningrec"] = None
    if args.equipmentmodel or args.all:
        get_dict["equipmentmodel"] = None
    if args.alarmmessages or args.all:
        get_dict["alarmmessages"] = None
    if args.commissioninfo or args.all:
        get_dict["commissioninfo"] = None
    if args.mcu or args.all:
        get_dict["mcu"] = None
    message_queue = [(json.dumps(get_dict), 1000)]
    send_message_queue(args, message_queue, con, address)
def set_set(args):
    tcp, udp = set_up_sockets(args)
    con, address = connect_sockets(tcp, udp)
    set_dict = {"type":"request",
                "action":"set"}
    if args.power is not None:
        set_dict["power"] = args.power
    if args.cleaning is not None:
        set_dict["cleaning"] = args.cleaning
    if args.beeping is not None:
        set_dict["beeping"] = args.beeping
    if args.carpetbooster is not None:
        set_dict["carpetbooster"] = args.carpetbooster
    if args.workingmode is not None:
        set_dict["workingmode"] = args.workingmode
    if args.suction is not None:
        set_dict["suction"] = args.suction
    if args.water is not None:
        set_dict["water"] = args.water
    if args.direction is not None:
        set_dict["direction"] = args.direction
    if args.commissioninfo is not None:
        set_dict["commissioninfo"] = args.commissioninfo
    if args.calibrationtime is not None:
        set_dict["calibrationtime"] = args.calibrationtime
    message_queue = [(json.dumps(set_dict), 1000)]
    send_message_queue(args, message_queue, con, address)
def set_reset(args):
    tcp, udp = set_up_sockets(args)
    con, address = connect_sockets(tcp, udp)
    reset_dict = { 
            "type" : "request",
            "action": "reset"
    }
    if args.sidebrush:
        reset_dict["sidebrush"] = None
    if args.rollingbrush:
        reset_dict["rollingbrush"] = None
    if args.filter:
        reset_dict["filter"] = None
    message_queue = [(json.dumps(reset_dict), 1000)]
    send_message_queue(args, message_queue, con, address)
def do_passive(args):
    print("Waiting for UDP broadcast")
    data, address = udp.recvfrom(4096)
    print("\n\n 2. UDP server received: ", data.decode('utf-8'), "from", address, "\n\n")

    print("3a. Sending UDP ack.\n")
    udp.sendto('QCX-ACK'.encode('utf-8'), address)
    time.sleep(1)
    print("3b. Sending UDP ack.\n")
    udp.sendto('QCX-ACK'.encode('utf-8'), address)
    pass

def set_up_sockets(args):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ("0.0.0.0", 3333)
    tcp.bind(server_address)
    tcp.listen(1)

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if args.myip is not None:
        server_address = (args.myip[0], 2222)
    else:
        server_address = ("0.0.0.0", 2222)
    udp.bind(server_address)
    return tcp, udp
def connect_sockets(tcp, udp):
    con = None
    while con is None:
        print("Broadcasting QCX-SYN Burst\n")
        udp.sendto('QCX-SYN'.encode('utf-8'), ('255.255.255.255', 2222))
        readable, _, _ = select.select([tcp], [], [], .1)
        if tcp in readable:
            con, address = tcp.accept()
            print("TCP layer connected")
    return con, address

def send_message_queue(args, message_queue_tx, con, address):
    state = 'WAIT_IV'
    localIv = get_random_bytes(8)
    sendingAES = None
    receivingAES = None
    data = []
    message_queue_tx.reverse()
    last_send = datetime.datetime.now()
    con.settimeout(.001)
    pause = datetime.timedelta(milliseconds=0)
    elapsed = datetime.datetime.now() - last_send
    if args.aes_key is not None:
        AES_KEY = bytes.fromhex(args.aes_key[0])
    else: 
        AES_KEY = bytes([0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF])
        
    timeout = datetime.timedelta(milliseconds=11000)
    started = datetime.datetime.now() 
    received_finish = False
    received_answer = True
    while ((not received_finish or not received_answer or len(message_queue_tx) > 0 or elapsed < pause)
    and datetime.datetime.now() - started < timeout):
        try:
            data = con.recv(4096)
            if len(data) == 0:
                print("EOF")
                break
        except socket.timeout:
            pass

        elapsed = datetime.datetime.now() - last_send

        if state == 'CONNECTED':
            send_next = elapsed >= pause
            if len(message_queue_tx) > 0 and send_next:
                msg, ts = message_queue_tx.pop()
                pause = datetime.timedelta(milliseconds=ts)
                sendMsg(msg, con, sendingAES)
                last_send = datetime.datetime.now()

        while len(data):
            print("TCP server received ", len(data), " bytes from ", address)
            print([hex(b) for b in data])

            pkgLen = data[0] * 256 + data[1]
            pkgType = data[3]

            pkg = data[4:4+pkgLen]
            if len(pkg) < pkgLen:
                print("Incomplete packet, waiting for more...")
                break

            data = data[4+pkgLen:]

            if state == 'WAIT_IV' and pkgType == 0:
                print("Plain: ", pkg)

                con.send(bytes([0, 8, 0, 1]) + localIv)

            if state == 'WAIT_IV' and pkgType == 1:
                remoteIv = pkg


                sendingAES = AES.new(AES_KEY, AES.MODE_CBC, iv=localIv + remoteIv)
                receivingAES = AES.new(AES_KEY, AES.MODE_CBC, iv=remoteIv + localIv)

                state = 'CONNECTED'

            elif state == 'CONNECTED' and pkgType == 2:
                received_finish = True
                received_answer = True
                cipher = pkg

                plain = receivingAES.decrypt(cipher)

                print("Decrypted: ", plain)
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="virtual App interface for the vc1", add_help=False)
    # Device independent 
    parser.add_argument('--myip', nargs=1, metavar=('ip'), help='specify own IP for broadcast sender')
    parser.add_argument('--aes_key', nargs=1, metavar=('aes_string'), help='specify aes key')
    parser.add_argument ('-h', '--help', action=_HelpAction, help='show this help message and exit')
    # grp = parser.add_mutually_exclusive_group(required=False)
    sub = parser.add_subparsers(title="subcommands", dest='command')
    
    tb = sub.add_parser('thingsboard', help='change thingsboard connection permission')
    tb.add_argument('permission', choices=['enable', 'disable'], help='whether it should be enabled or disabled')
    tb.set_defaults(func=set_thingsboard)
    pssv = sub.add_parser('passive', help='vApp will passively listen for UDP SYN from devices')
    pssv.set_defaults(func=do_passive)
    ota = sub.add_parser('ota', help='allows over the air programming of the device')
    ota.add_argument('url', help='specify http URL for ota')
    ota.set_defaults(func=set_ota)
    ping = sub.add_parser('ping', help='send a ping and nothing else')
    ping.set_defaults(func=set_ping)
    frs = sub.add_parser('factory-reset', help='trigger a factory reset on the device - the device has to be onboarded again afterwards)')
    frs.set_defaults(func=set_factory_reset)
    reb = sub.add_parser('reboot', help='trigger a reboot')
    reb.set_defaults(func=set_reboot)
    req = sub.add_parser('get', help='send state request')
    req.add_argument('--all', help='If this flag is set, the whole state will be requested', action='store_true')
    req.add_argument('--power', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--cleaning', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--beeping', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--battery', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--sidebrush', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--rollingbrush', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--filter', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--carpetbooster', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--area', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--time', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--calibrationtime', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--workingmode', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--workstatus', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--suction', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--water', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--direction', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--errors', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--cleaningrec', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--equipmentmodel', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--alarmmessages', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--commissioninfo', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--mcu', help='Ask if mcu is online', action='store_true')
    req.set_defaults(func=set_state_request)

    #device specific
    set_parser = sub.add_parser("set", help='enables use of the vc1 control arguments and will control vc1')
    set_parser.add_argument('--power', choices=['on', 'off'], help='turn power on/off')
    set_parser.add_argument('--cleaning', choices=['on', 'off'], help='turn cleaning on/off')
    set_parser.add_argument('--beeping', choices=['on', 'off'], help='enable/disable the find-vc function')
    set_parser.add_argument('--carpetbooster', metavar='strength', type=int, help='set the carpet booster strength (0-255)')
    set_parser.add_argument('--workingmode', choices=['STANDBY', 'SMART', 'MOP', 'WALL_FOLLOW', 'PARTIAL_BOW', 'SPIRAL', 'CHARGE_GO', 'SROOM'], help='set the working mode')
    set_parser.add_argument('--water', choices=['LOW', 'MID', 'HIGH'], help='set water quantity')
    set_parser.add_argument('--suction', choices=['LOW', 'MID', 'HIGH'], help='set suction power')
    set_parser.add_argument('--direction', choices=['FORWARDS','BACKWARDS', 'TURN_LEFT', 'TURN_RIGHT', 'STOP'], help='manually control movement')
    set_parser.add_argument('--commissioninfo', type=str, help='set up to 256 characters of commisioning info')
    set_parser.add_argument('--calibrationtime', metavar='time', type=int, help='set the calibration time (1-1999999999)')
    set_parser.set_defaults(func=set_set)

    reset_parser = sub.add_parser("reset", help='enables resetting consumables')
    reset_parser.add_argument('--sidebrush', help='resets the sidebrush life counter', action='store_true')
    reset_parser.add_argument('--rollingbrush', help='resets the rollingbrush life counter', action='store_true')
    reset_parser.add_argument('--filter', help='resets the filter life counter', action='store_true')
    reset_parser.set_defaults(func=set_reset)

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)

    


    # data, address = udp.recvfrom(4096)
    # print("\n\n 2. UDP server received: ", data.decode('utf-8'), "from", address, "\n\n")

    # state = 'WAIT_IV'
    # localIv = get_random_bytes(8)

    # sendingAES = None
    # receivingAES = None

    # message_queue_tx = []

    # if args.command == 'ota':
    #     message_queue_tx.append((json.dumps( { "type" : "fw_update", "url" : args.ota}), 3000))

    # elif args.command == 'ping':
    #     message_queue_tx.append((json.dumps( { "type" : "ping" }), 10000))

    # if args.command == 'thingsboard':
    #     message_queue_tx.append()

    # if args.factory_reset:
    #     message_queue_tx.append()

    # if args.routine_list:
    #     message_queue_tx.append((json.dumps( { "type" : "routine", "action": "list" }), 500))

    # if args.routine_put:
    #     message_queue_tx.append((json.dumps( {
    #         "type" : "routine", "action": "put",
    #         "id": args.routine_id, "scene": args.routine_scene,
    #         "commands":  args.routine_commands
    #     }), 500))

    # if args.routine_delete:
    #     message_queue_tx.append((json.dumps( {
    #         "type" : "routine", "action": "delete", "id": args.routine_id }), 500))
    # if args.routine_start:
    #     message_queue_tx.append((json.dumps( {
    #         "type" : "routine", "action": "start", "id": args.routine_id }), 500))    
            
    # if args.power:
    #     message_queue_tx.append((json.dumps( {
    #         "type" : "request", "status": args.power[0] }), 500))

    # if args.reboot:
    #     

