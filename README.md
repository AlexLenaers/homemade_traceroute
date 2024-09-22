
# Traceroute Script

This is a simple Python implementation of the `traceroute` command.
It sends ICMP echo requests to trace the path packets take to reach a specified destination,
measuring round-trip times (RTTs) at each hop.

## Features

- Sends ICMP Echo requests using raw sockets.
- Measures and displays the RTT for each hop.
- Allows specification of the maximum number of hops.
- Handles interruptions (e.g., Ctrl+C) gracefully.

## Requirements

- **Python 3.x**
- `dpkt` library for creating and parsing ICMP packets
- Administrator/root privileges (required to send ICMP packets)

You can install the required `dpkt` library using:
```bash
pip install dpkt
```

## Usage

```bash
sudo python traceroute.py -d <destination> [-m <max_hops>]
```

### Arguments

- `-d, --dest` : **(Required)** The destination IP address or hostname to trace.
- `-m, --max_hops` : (Optional) The maximum number of hops to trace. Defaults to `30`.

### Example

To trace the route to `google.com` with the default 30 hops:
```bash
sudo python traceroute.py -d google.com
```

To trace the route to `google.com` with a maximum of 15 hops:
```bash
sudo python traceroute.py -d google.com -m 15
```

## Important Notes

- **Root/administrator privileges** are required because this script uses raw sockets to send ICMP packets.
- This script is intended for educational purposes and may not work on all networks, as some networks or devices might block ICMP traffic.

## License

This script is provided under the MIT License.
