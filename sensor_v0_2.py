import sys
import os
from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP

LOG_FILE = "network_traffic.log"
LOG_HEADER = "timestamp,protocol,src_ip,dst_ip,dst_port\n"

# Check if log file exists, if not, create it and write the header
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write(LOG_HEADER)

def process_packet(packet):
    """
    Analyzes a single packet and writes it to a log file.
    """
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        timestamp = datetime.now().isoformat()
        
        proto = ""
        dst_port = ""

        if TCP in packet:
            proto = "TCP"
            dst_port = packet[TCP].dport
        
        elif UDP in packet:
            proto = "UDP"
            dst_port = packet[UDP].dport
        
        if proto:
            # Format: 2023-10-27T10:30:01.123,TCP,192.168.1.10,1.1.1.1,443
            log_line = f"{timestamp},{proto},{src_ip},{dst_ip},{dst_port}\n"
            
            # Append to the log file
            try:
                with open(LOG_FILE, "a") as f:
                    f.write(log_line)
                
                # Print to console as well to confirm it's working
                print(f"Logged: {log_line.strip()}")

            except Exception as e:
                print(f"[!] Error writing to log: {e}")

# --- Main part of the script ---
print(f"🚀 Starting network sensor v0.2... (logging to {LOG_FILE})")
print("Press Ctrl+C to stop.")

try:
    sniff(filter="ip and (tcp or udp)", prn=process_packet, store=0)
except KeyboardInterrupt:
    print("\n[!] Sensor stopped by user.")
    sys.exit(0)
except Exception as e:
    print(f"\n[!] An error occurred: {e}")