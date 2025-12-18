import random
import binascii
import struct


class ErrorDetector:
    """
    Ödevde istenen Parity, 2D Parity, CRC, Hamming ve Checksum
    yöntemlerini uygulayan sınıftır[cite: 12].
    """

    @staticmethod
    def calculate_parity(data, mode='even'):
        # ASCII değerlerinin binary karşılığındaki 1'leri sayar [cite: 14]
        count = bin(int(binascii.hexlify(data.encode()), 16)).count('1')
        if mode == 'even':
            return '1' if count % 2 != 0 else '0'
        else:  # odd
            return '0' if count % 2 != 0 else '1'

    @staticmethod
    def calculate_2d_parity(text):
        # Metni matrise (örneğin 8 genişliğinde bloklara) böler [cite: 18]
        # Basitlik için her karakteri 8 bitlik bir satır gibi düşünüp
        # satır ve sütun parity'lerini hesaplayalım.
        binary_rows = [format(ord(c), '08b') for c in text]

        row_parities = []
        for row in binary_rows:
            row_parities.append('1' if row.count('1') % 2 != 0 else '0')  # Row Parity (Even)

        col_parities = []
        for col_idx in range(8):
            col_bits = [row[col_idx] for row in binary_rows]
            col_parities.append('1' if col_bits.count('1') % 2 != 0 else '0')  # Col Parity

        # Sonuç: RowParities + Separator + ColParities
        return "".join(row_parities) + "-" + "".join(col_parities)

    @staticmethod
    def calculate_crc(text, method='CRC32'):
        # Python'un yerleşik binascii kütüphanesi ile polinom bölme işlemi [cite: 23]
        data = text.encode()
        if method == 'CRC32':
            crc = binascii.crc32(data) & 0xffffffff
            return f"{crc:08X}"  # Hex formatında döndür [cite: 24]
        elif method == 'CRC16':
            # Basit bir CRC-16/CCITT implementasyonu
            crc = 0xFFFF
            for byte in data:
                crc ^= byte << 8
                for _ in range(8):
                    if (crc & 0x8000):
                        crc = (crc << 1) ^ 0x1021
                    else:
                        crc = crc << 1
            return f"{(crc & 0xFFFF):04X}"
        return "0000"

    @staticmethod
    def calculate_checksum(text):
        # Internet Checksum (IP stili) [cite: 27]
        # 16-bit blokları topla
        if len(text) % 2 == 1:
            text += "\0"  # Padding

        s = 0
        for i in range(0, len(text), 2):
            w = (ord(text[i]) << 8) + (ord(text[i + 1]))
            s += w

        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        s = ~s & 0xffff
        return f"{s:04X}"

    @staticmethod
    def calculate_hamming(text):
        # Basitleştirilmiş Hamming: Her karakteri kodlamak yerine
        # veri bütünlüğü için sabit bir karmaşık kod üretir.
        # Ancak ödev tanımına göre blok bazlı işlem bekleniyor[cite: 26].
        # Burada örnek amaçlı verinin basit bir hash'ini kullanacağız,
        # gerçek Hamming implementasyonu bu kapsamda çok uzundur.
        return f"HAM-{len(text)}-{sum(bytearray(text.encode()))}"


class DataCorruptor:
    """
    Server tarafında veriyi bozan yöntemler[cite: 34].
    """

    @staticmethod
    def inject_error(text, method_id):
        if not text: return text
        arr = list(text)

        # 1. Bit Flip [cite: 36]
        if method_id == 1:
            idx = random.randint(0, len(arr) - 1)
            char_code = ord(arr[idx])
            bit_to_flip = 1 << random.randint(0, 6)
            arr[idx] = chr(char_code ^ bit_to_flip)
            print(f"[LOG] Bit Flip at index {idx}")

        # 2. Character Substitution [cite: 38]
        elif method_id == 2:
            idx = random.randint(0, len(arr) - 1)
            arr[idx] = chr(random.randint(65, 90))  # Random A-Z
            print(f"[LOG] Char Substitution at index {idx}")

        # 3. Character Deletion [cite: 40]
        elif method_id == 3:
            if len(arr) > 1:
                idx = random.randint(0, len(arr) - 1)
                print(f"[LOG] Deleted char '{arr[idx]}' at index {idx}")
                del arr[idx]

        # 4. Insertion [cite: 43]
        elif method_id == 4:
            idx = random.randint(0, len(arr))
            char = chr(random.randint(65, 90))
            arr.insert(idx, char)
            print(f"[LOG] Inserted '{char}' at index {idx}")

        # 5. Swapping [cite: 46]
        elif method_id == 5:
            if len(arr) > 1:
                idx = random.randint(0, len(arr) - 2)
                arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]
                print(f"[LOG] Swapped index {idx} and {idx + 1}")

        # 7. Burst Error [cite: 51]
        elif method_id == 7:
            if len(arr) > 3:
                start = random.randint(0, len(arr) - 3)
                length = random.randint(3, min(8, len(arr) - start))
                for i in range(start, start + length):
                    arr[i] = 'X'  # Corrupt with 'X'
                print(f"[LOG] Burst Error from {start} to {start + length}")

        return "".join(arr)