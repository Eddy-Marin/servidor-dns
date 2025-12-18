import socket
import json

IP = '127.0.0.1'
PORT = 9003

# Zona IPN: Tiene las respuestas finales (RR A Records)
IPN_ZONE = {
    "www.ipn.mx": "148.204.103.43",
    "mail.ipn.mx": "148.204.103.50"
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

print(f"[*] AUTH SERVER (ipn.mx) corriendo en {IP}:{PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    dominio = data.decode().strip()
    print(f"Consulta recibida por: {dominio}")

    response = {}
    if dominio in IPN_ZONE:
        # RESPUESTA FINAL
        response = {
            "status": "ANSWER",
            "ip": IPN_ZONE[dominio],
            "message": "Aquí tienes la IP."
        }
    else:
        response = {"status": "ERROR", "message": "Host no encontrado en ipn.mx"}

    sock.sendto(json.dumps(response).encode(), addr)