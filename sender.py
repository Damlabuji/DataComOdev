import socket
from protocol_utils import ErrorDetector


def run_sender():
    HOST = '127.0.0.1'
    PORT = 65432

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Error: Server is not running. Start server.py first.")
        return

    print("-" * 40)
    print("CLIENT 1: SENDER CONNECTED")
    print("-" * 40)

    while True:
        # 1. Kullanıcıdan Text Al [cite: 10]
        text = input("\nEnter text to send (or 'exit'): ")
        if text.lower() == 'exit': break

        print("\nSelect Error Detection Method:")
        print("1. Parity Bit (Even)")
        print("2. 2D Parity")
        print("3. CRC-16")
        print("4. Checksum (Internet)")
        print("5. Hamming Code")  # Yeni seçenek [cite: 7, 25]

        choice = input("Selection (1-5): ")

        if choice == '1':
            method_name = "PARITY"
            control_info = ErrorDetector.calculate_parity(text, 'even')
        elif choice == '2':
            method_name = "2DPARITY"
            control_info = ErrorDetector.calculate_2d_parity(text)
        elif choice == '3':
            method_name = "CRC16"
            control_info = ErrorDetector.calculate_crc(text, 'CRC16')
        elif choice == '4':
            method_name = "CHECKSUM"
            control_info = ErrorDetector.calculate_checksum(text)
        elif choice == '5':  # Hamming Blok İşlemi [cite: 26]
            method_name = "HAMMING"
            control_info = ErrorDetector.calculate_hamming(text)

        # 3. Paketi Oluştur: DATA|METHOD|CONTROL [cite: 29]
        packet = f"{text}|{method_name}|{control_info}"

        client_socket.send(packet.encode('utf-8'))
        print(f"[SENT] {packet}")

    client_socket.close()


if __name__ == "__main__":
    run_sender()
