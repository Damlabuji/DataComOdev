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
                # [cite_start]Paketi parçalara ayırma [cite: 57, 58]
                parts = packet.split('|')
                if len(parts) < 3:
                    raise ValueError("Packet missing control info")

                control_rx = parts[-1]
                method = parts[-2]
                data_rx = "|".join(parts[:-2])

            except ValueError:
                print(f"[ERROR] Malformed packet received: {packet}")
                continue

            # [cite_start]Yeniden kontrol bilgisi üretme [cite: 59, 60, 61, 62, 64]
            control_calc = "ERROR"

            if method == "PARITY":
                control_calc = ErrorDetector.calculate_parity(data_rx, 'even')
            elif method == "2DPARITY":
                control_calc = ErrorDetector.calculate_2d_parity(data_rx)
            elif method == "CRC16":
                control_calc = ErrorDetector.calculate_crc(data_rx, 'CRC16')
            elif method == "CHECKSUM":
                control_calc = ErrorDetector.calculate_checksum(data_rx)
            elif method == "HAMMING":
                control_calc = ErrorDetector.calculate_hamming(data_rx)
            else:
                print(f"[!] Unknown method received: {method}")
                control_calc = "UNKNOWN"

            # [cite_start]Karşılaştırma ve Sonuç Yazdırma [cite: 65, 67, 72, 73]
            status = "DATA CORRECT" if control_calc == control_rx else "DATA CORRUPTED"

            print(f"Received Data: {data_rx}")
            print(f"Method: {method}")
            print(f"Sent Check Bits: {control_rx}")
            print(f"Computed Check Bits: {control_calc}")
            print(f"Status: {status}")
            print("-" * 20)

        except Exception as e:
            print(f"Error processing packet: {e}")

    sock.close()

if __name__ == "__main__":
    run_receiver()
