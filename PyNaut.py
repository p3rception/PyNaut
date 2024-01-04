#!/usr/bin/env python3
#
# Author: Dimitris Pergelidis (p3rception)

from time import sleep
import shutil
import threading
import socket
from queue import Queue


# ---------------- Colors ---------------- #

MAIN = '\033[38;5;50m'
LGREEN = '\033[38;5;119m'
GREEN = '\033[38;5;47m'
BLUE = '\033[0;38;5;12m'
ORANGE = '\033[0;38;5;214m'
RED = '\033[1;31m'
END = '\033[0m'
BOLD = '\033[1m'

# ----------- Message Prefixes ----------- #

INPUT = f'{MAIN}Input{END}'
WARN = f'{RED}Warning{END}'
INFO = f'{ORANGE}Info{END}'
ERROR = f'{RED}Error{END}'
SUMMARY = f'{LGREEN}Summary{END}'


# ---------------- Banner ---------------- #

def haxor_print(text, leading_spaces=0):
   text_chars = list(text)
   current, mutated = '', ''

   for i in range(len(text)):
      original = text_chars[i]
      current += original
      mutated += f'\033[1;38;5;82m{text_chars[i].upper()}\033[0m'
      print(f'\r{" " * leading_spaces}{mutated}', end='')
      sleep(0.07)
      print(f'\r{" " * leading_spaces}{current}', end='')
      mutated = current

   print(f'\r{" " * leading_spaces}{text}\n')

def print_banner(): 
   print('\r')
   padding = '  '

   P = [['┌', '─','┐'], ['├', '─', '┘'],['┴', ' ', ' ']]
   Y = [[' ', '┬', ' ','┬'], [' ', '└', '┬', '┘'],[' ', ' ', '┴', ' ']]
   N = [[' ', '┌','┐','┌'], [' ', '│','│','│'], [' ', '┘','└','┘']]
   A = [[' ', '┌','─','┐'], [' ', '├','─','┤'], [' ', '┴',' ','┴']]
   U = [[' ', '┬', ' ','┬'], [' ', '│', ' ', '│'],[' ', '└', '─', '┘']]
   T = [[' ', '┌', '┬','┐'], [' ', ' ', '│', ' '],[' ', ' ', '┴', ' ']]

  

   banner = [P,Y,N,A,U,T]
   final = []
   init_color = 43
   txt_color = init_color
   cl = 0

   for charset in range(0, 3):
      for pos in range(0, len(banner)):
         for i in range(0, len(banner[pos][charset])):
            clr = f'\033[38;5;{txt_color}m'
            char = f'{clr}{banner[pos][charset][i]}'
            final.append(char)
            cl += 1
            txt_color = txt_color + 36 if cl <= 3 else txt_color

         cl = 0

         txt_color = init_color
      init_color += 1

      if charset < 2:
         final.append('\n   ')

   print(f"   {''.join(final)}{END}")
   haxor_print('by p3rception', 17)

   # Dynamic horizontal line
   terminal_width = shutil.get_terminal_size().columns
   dynamic_line = '─' * terminal_width
   print(f"{dynamic_line}\n")



# -------------- Main functions -------------- #

def validate_port_range(port_range_input):
   if port_range_input.lower() == "all":
      return 0, 65535
   try:
      port_min, port_max = map(int, port_range_input.split('-'))
      if 0 <= port_min <= 65535 and 0 <= port_max <= 65535 and port_min <= port_max:
         return port_min, port_max
      else:
         return None, None # Return None for invalid range
   except ValueError:
      return None, None # Return None for invalid input format

def scan_port(target_ip, port, print_lock, open_ports):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      # Attempt to connect to the target IP and port
      portx = s.connect((target_ip, port))
      with print_lock:
         print(f"{END}[{GREEN}✔{END}] Port {port} is open")
         open_ports.append(str(port))
      portx.close()
   except (ConnectionRefusedError, AttributeError, OSError):
      pass

def threader(q, target_ip, print_lock, open_ports):
   while True:
      worker = q.get()
      scan_port(target_ip, worker, print_lock, open_ports)
      q.task_done()


def main():
   print_banner()
   
   # Less than 2 seconds increases the risk of false negatives
   socket.setdefaulttimeout(2)
   print_lock = threading.Lock()
   open_ports = []

   while True:
      target = input(f"{END}[{INPUT}] Please enter a valid {BOLD}IP address{END} or {BOLD}URL{END}: {MAIN}").strip()

      try:
         target_ip = socket.gethostbyname(target)
         break # Break if a valid address is obtained
      except (UnboundLocalError, socket.gaierror):
         print(f"\n{END}[{WARN}] Invalid format. Please use a correct IP or Web Address.\n")

   while True:
      port_range_input = input(f"\n{END}[{INPUT}] Please enter the {BOLD}port range{END} to scan in valid format [e.g 0-100]: {MAIN}")
      port_min, port_max = validate_port_range(port_range_input)
      
      if port_min is not None and port_max is not None:
         port_range = f"{port_min}-{port_max}"
         start_port, end_port = map(int, port_range.split('-'))
         break  # Break if a valid port range is obtained
      else:
         print(f"\n{END}[{WARN}] Invalid port range format. Please provide a valid range [0-65535].")

   q = Queue()

   for i in range(200):
      t = threading.Thread(target=threader, args=(q, target_ip, print_lock, open_ports))
      t.daemon = True
      t.start()

   print(f"\n{END}[{INFO}] Scanning ports {port_min}-{port_max} on {target_ip}\n")

   for worker in range(start_port, end_port + 1):
      q.put(worker)
   
   q.join()

   # Scan summary
   if open_ports:
      print(f"\n{END}[{SUMMARY}] Open ports on {target_ip}: {BOLD}{', '.join(map(str, open_ports))}{END}")
   else:
      print(f"{END}[{SUMMARY}] No open ports found on {target_ip}")

if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      print(f"\n{END}[{INFO}] PyNaut was terminated.")
      quit()