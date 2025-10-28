import sys
from scapy.all import sniff, IP, TCP, UDP

# This function will be called for each packet
def process_packet(packet):
    """
    Analyzes a single packet and prints relevant information.
    """
    # Check if it's an IP packet
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        # Check for TCP (for port info)
        if TCP in packet:
            dst_port = packet[TCP].dport
            print(f"[TCP] {src_ip} -> {dst_ip}:{dst_port}")
        
        # Check for UDP (for port info)
        elif UDP in packet:
            dst_port = packet[UDP].dport
            print(f"[UDP] {src_ip} -> {dst_ip}:{dst_port}")

# --- Main part of the script ---
print("🚀 Starting network sensor v0.1...")
print("Press Ctrl+C to stop.")

try:
    # Start sniffing. 
    # 'prn' specifies the callback function to run for each packet.
    # 'store=0' means we don't keep packets in memory, saving resources.
    # 'filter' uses BPF syntax to only capture IP packets (TCP or UDP).
    sniff(filter="ip and (tcp or udp)", prn=process_packet, store=0)

except KeyboardInterrupt:
    print("\n[!] Sensor stopped by user.")
    sys.exit(0)
except Exception as e:
    print(f"\n[!] An error occurred: {e}")