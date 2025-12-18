import socket
import json

IP = '127.0.0.1'
PORT = 9002

# Zona .MX: Mapea dominios de segundo nivel a sus servidores Autoritativos
MX_ZONE = {
    "ipn.mx": {"ip": "127.0.0.1", "port": 9003},
    "google.mx": {"ip": "127.0.0.1", "port": 8888} # Ejemplo
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

print(f"[*] TLD SERVER (.mx) corriendo en {IP}:{PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    dominio = data.decode().strip()
    print(f"Consulta recibida por: {dominio}")

    # Lógica: Ver si conocemos el dominio de segundo nivel (ipn.mx)
    # Una forma simple es revisar si el string termina con "ipn.mx"
    encontrado = False
    response = {}
    
    for zona in MX_ZONE:
        if dominio.endswith(zona):
            response = {
                "status": "REFERRAL",
                "message": f"Yo no se la IP exacta, pregunta al servidor autoritativo de '{zona}'",
                "next_server": MX_ZONE[zona]
            }
            encontrado = True
            break
    
    if not encontrado:
        response = {"status": "ERROR", "message": "Dominio no registrado en .mx"}

    sock.sendto(json.dumps(response).encode(), addr)