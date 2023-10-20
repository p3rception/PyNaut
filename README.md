# PyNaut - Python Port Scanner

PyNaut is a simple Python port scanner designed to scan a range of ports on a target IP address or URL to detect open ports. It utilizes multi-threading for faster scanning.

## Features

- Scan a range of ports on a target IP or URL.
- Multi-threaded scanning for improved speed.
- Detect and report open ports on the target.

## Getting Started

### Prerequisites

- Python 3.x
- No external dependencies (Standard library only)

### Installation

1. Clone or download this repository to your local machine.
  
2. Run the script using Python 3


## Usage

1. Launch the script.

2. Enter a valid IP address or URL when prompted.

3. Enter a port range to scan in proper format, e.g. `0-100`.

4. The script will start scanning the specified range of ports on the target.

5. The script will display a summary of open ports found.

## Example

```plaintext
[Input] Please enter a valid IP address or URL: example.com

[Input] Please enter the port range to scan in valid format [e.g 0-100]: 80-100

[Info] Scanning ports 80-100 on example.com

[✔] Port 80 is open
[✔] Port 88 is open

[Summary] Open ports on example.com: 80, 88
```
## Author

Dimitris Pergelidis ([p3rception](https://github.com/p3rception))

## License

This project is licensed under the MIT License - see the LICENSE file for details.