import socket
from protocol_utils import ErrorDetector


def run_receiver():
    HOST = '127.0.0.1'
    PORT = 65432

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except:
        print("Server not found. Make sure server.py is running and waiting.")
        return

    print("-" * 40)
    print("CLIENT 2: RECEIVER READY")
    print("-" * 40)

    while True:
        try:
            packet_bytes = sock.recv(1024)
            if not packet_bytes: break

            packet = packet_bytes.decode('utf-8')

            try:
                # Sadece ilk 2 ayırıcıyı dikkate al, geri kalan datanın parçası olabilir
                parts = packet.split('|')
                if len(parts) < 3:
                    raise ValueError("Packet missing control info")

                # Veri kısmında '|' karakteri olma ihtimaline karşı sondan başa alıyoruz
                control_rx = parts[-1]
                method = parts[-2]
                # Geri kalan her şey veridir (data içinde | varsa bozulmasın diye)
                data_rx = "|".join(parts[:-2])

            except ValueError:
                print(f"[ERROR] Malformed packet received: {packet}")
                continue

            # Yeniden Hesapla
            control_calc = ""
            if method == "PARITY":
                control_calc = ErrorDetector.calculate_parity(data_rx, 'even')
            elif method == "2DPARITY":
                control_calc = ErrorDetector.calculate_2d_parity(data_rx)
            elif method == "CRC16":
                control_calc = ErrorDetector.calculate_crc(data_rx, 'CRC16')
            elif method == "CHECKSUM":
                control_calc = ErrorDetector.calculate_checksum(data_rx)
            else:
                control_calc = "UNKNOWN_METHOD"

            status = "DATA CORRECT" if control_calc == control_rx else "DATA CORRUPTED"

            print(f"Received: {data_rx} | Method: {method} | Status: {status}")
            if status == "DATA CORRUPTED":
                print(f"   -> Expected: {control_rx}, Got: {control_calc}")

        except Exception as e:
            print(f"Error processing packet: {e}")

    sock.close()


if __name__ == "__main__":
    run_receiver()