import argparse
import signal
import socket
import struct
import sys
import time
import dpkt

# Default maximum number of hops for traceroute
MAX_HOP_DEFAULT = 30


def make_icmp_socket(ttl=64, timeout=5):
    # Create a raw socket for ICMP protocol with the specified TTL and timeout
    icmp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_RAW, proto=socket.IPPROTO_ICMP)
    icmp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
    icmp_socket.settimeout(timeout)
    return icmp_socket


def send_icmp_echo(socket_obj, payload, id=0, seq=0, destination='localhost'):
    # Create an ICMP Echo packet with the specified ID, sequence number, and payload
    echo = dpkt.icmp.ICMP.Echo()
    echo.id = id
    echo.seq = seq
    echo.data = bytes(payload, 'utf-8')

    # Create the ICMP packet with the Echo packet as data
    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO
    icmp.data = echo

    # Convert the packet to bytes for transmission
    packet = bytes(icmp)

    # Send the packet to the destination
    try:
        socket_obj.sendto(packet, (destination, 0))
    except socket.gaierror:
        print("Destination not found: exiting...")
        quit()


def recv_icmp_response():
    icmp_socket = make_icmp_socket()

    # Attempt to receive an ICMP response up to 3 times
    x = 0
    while x < 3:
        try:
            packet, addr = icmp_socket.recvfrom(1024)  # Buffer size of 1024 bytes
            return addr
        except socket.timeout:
            print("Hop timeout, trying again...")
            x += 1

    print("Timeout error. Exiting...")
    quit()


def signal_handler(sig, frame):
    # Handle termination signals (e.g., Ctrl+C) gracefully
    sys.exit(0)


def main():
    # Parse command-line arguments for destination IP and max hops
    parser = argparse.ArgumentParser(description="Simple implementation of the traceroute command.")
    parser.add_argument('-d', '--dest', metavar='', required=True, help='Destination IP address')
    parser.add_argument('-m', '--max_hops', metavar='', type=int, required=False,
                        help=f"Max number of hops; default = {MAX_HOP_DEFAULT}", default=MAX_HOP_DEFAULT)
    args = parser.parse_args()

    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Resolve the destination hostname to an IP address
    destination = args.dest
    destination = socket.gethostbyname(destination)

    # Perform traceroute from TTL=1 up to the maximum specified hops
    for ttl in range(1, args.max_hops + 1):
        start_time = time.time()  # Record the start time for RTT calculation

        # Create an ICMP socket with the current TTL
        hm_socket = make_icmp_socket(ttl=ttl)

        # Send an ICMP Echo request to the destination
        send_icmp_echo(socket_obj=hm_socket, payload='ping', destination=destination)

        # Receive the ICMP response and extract the IP address
        land_ip = recv_icmp_response()[0]

        end_time = time.time()  # Record the end time for RTT calculation

        # Check if the response was received or if it timed out
        if land_ip is None:
            print(f"destination = {destination}; hop {ttl} = *; rtt = Timeout")
        else:
            print(f"destination = {destination}; hop {ttl} = {land_ip}; rtt = {1000 * (end_time - start_time):.2f} ms")

            # If the destination was reached, end the traceroute
            if land_ip == destination:
                break


if __name__ == "__main__":
    main()
