import socket
import json

def resolver_dns_iterativo(dominio_buscado):
    # 1. Empezamos siempre preguntando al ROOT SERVER
    next_ip = '127.0.0.1'
    next_port = 9001
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"\n--- Iniciando resolución para: {dominio_buscado} ---")

    step = 1
    while True:
        try:
            print(f"\n[Paso {step}] Consultando a {next_ip}:{next_port}...")
            
            # Enviar consulta
            client_socket.sendto(dominio_buscado.encode(), (next_ip, next_port))
            
            # Recibir respuesta JSON
            data, _ = client_socket.recvfrom(4096)
            response = json.loads(data.decode())
            
            print(f"   Respuesta del servidor: {response['message']}")
            
            # ANALIZAR RESPUESTA
            if response['status'] == 'ANSWER':
                print(f"   ¡ÉXITO! IP encontrada: {response['ip']}")
                return response['ip']
            
            elif response['status'] == 'REFERRAL':
                # El servidor nos dio la dirección del siguiente
                next_server_info = response['next_server']
                next_ip = next_server_info['ip']
                next_port = next_server_info['port']
                print(f"   -> Redirigiendo al siguiente servidor...")
                step += 1
            
            elif response['status'] == 'ERROR':
                print("   Error: El dominio no existe.")
                return None

        except Exception as e:
            print(f"   Error de conexión: {e}")
            return None

if __name__ == "__main__":
    # Prueba
    ip_final = resolver_dns_iterativo("www.ipn.mx")