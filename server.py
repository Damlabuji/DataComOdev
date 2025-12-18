import socket
from protocol_utils import DataCorruptor
import random


def start_server():
    HOST = '127.0.0.1'
    PORT = 65432

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Portu hemen serbest bırakması için
    server_sock.bind((HOST, PORT))
    server_sock.listen(2)

    print(f"[*] Server listening on {HOST}:{PORT}")
    print("[*] Waiting for Client 2 (Receiver) to connect first...")

    conn_receiver, addr_receiver = server_sock.accept()
    print(f"[+] Receiver connected: {addr_receiver}")

    print("[*] Waiting for Client 1 (Sender)...")
    conn_sender, addr_sender = server_sock.accept()
    print(f"[+] Sender connected: {addr_sender}")

    # --- KRITIK DEGISIKLIK: Sonsuz döngü try-except'i kapsıyor ---
    while True:
        try:
            # 1. Veriyi al
            packet = conn_sender.recv(1024).decode('utf-8')
            if not packet:
                print("[-] Sender disconnected.")
                break

            print(f"\n[INCOMING] Packet: {packet}")

            # Paketi parçala
            if "|" not in packet:
                print("[!] Invalid packet format (No separator)")
                continue

            parts = packet.split('|')
            if len(parts) < 3:
                print("[!] Invalid packet format (Missing parts)")
                continue

            data = parts[0]
            method = parts[1]
            ctrl = parts[2]

            # 2. Hata Enjekte Et
            error_method = random.choice([0, 1, 2, 3, 4, 5, 7])
            corrupted_data = DataCorruptor.inject_error(data, error_method)

            # 3. İlet
            forward_packet = f"{corrupted_data}|{method}|{ctrl}"
            conn_receiver.send(forward_packet.encode('utf-8'))
            print(f"[FORWARD] Sent to Receiver: {forward_packet}")

        except ConnectionResetError:
            print("[!] Connection lost.")
            break
        except Exception as e:
            # Hata olsa bile döngüyü kırma, sadece hatayı yaz
            print(f"[!] ERROR handled: {e}")
            # Devam et...

    conn_receiver.close()
    conn_sender.close()
    server_sock.close()


if __name__ == "__main__":
    start_server()