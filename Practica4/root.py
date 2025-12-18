import socket
import json

IP = '127.0.0.1'
PORT = 9001

# Zona Raíz: Mapea extensiones a direcciones de servidores TLD
ROOT_ZONE = {
    "mx": {"ip": "127.0.0.1", "port": 9002},
    "com": {"ip": "127.0.0.1", "port": 9090} # Ejemplo
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

print(f"[*] ROOT SERVER corriendo en {IP}:{PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    dominio = data.decode().strip()
    print(f"Consulta recibida por: {dominio}")

    # Lógica: Extraer la extensión (TLD)
    partes = dominio.split('.')
    tld = partes[-1] # Tomamos lo ultimo (.mx)

    response = {}
    if tld in ROOT_ZONE:
        # REFERENCIA: No te doy la IP final, te doy la dirección del servidor .MX
        response = {
            "status": "REFERRAL",
            "message": f"Yo no se, pregunta al servidor TLD '{tld}'",
            "next_server": ROOT_ZONE[tld]
        }
    else:
        response = {"status": "ERROR", "message": "TLD no soportado"}

    sock.sendto(json.dumps(response).encode(), addr)