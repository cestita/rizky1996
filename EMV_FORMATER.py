from smartcard.System import readers
from smartcard.util import toHexString

# Pilih reader yang terhubung
def select_reader():
    r = readers()
    if not r:
        print("No smart card readers available.")
        return None
    return r[0]

# Kirim perintah APDU ke kartu
def send_apdu(command, data=b''):
    reader = select_reader()
    if reader is None:
        return None
    
    connection = reader.createConnection()
    connection.connect()

    # Kirim APDU
    apdu_command = command + list(data)
    response, sw1, sw2 = connection.transmit(apdu_command)
    return response, sw1, sw2

# Hapus atau format semua data di kartu EMV
def format_emv():
    # Langkah 1: Pilih File Aplikasi atau Master File
    select_file_command = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x3F, 0x00]  # SELECT FILE (Contoh)
    response, sw1, sw2 = send_apdu(select_file_command)
    print("Select File Response:", toHexString(response))
    print("Status Word:", hex(sw1 << 8 | sw2))

    # Langkah 2: Hapus File atau Aplikasi
    delete_file_command = [0x00, 0xE4, 0x00, 0x00, 0x00]  # DELETE FILE (Contoh)
    response, sw1, sw2 = send_apdu(delete_file_command)
    print("Delete File Response:", toHexString(response))
    print("Status Word:", hex(sw1 << 8 | sw2))

    # Langkah 3: Pilih Aplikasi atau Direktori Lain dan Hapus File
    # Sesuaikan dengan aplikasi dan struktur kartu Anda
    # Misalnya, pilih dan hapus semua aplikasi
    select_command = [0x00, 0xA4, 0x00, 0x00, 0x02, 0xDF, 0x01]  # Ganti dengan AID atau DF yang sesuai
    response, sw1, sw2 = send_apdu(select_command)
    print("Select Application Response:", toHexString(response))
    print("Status Word:", hex(sw1 << 8 | sw2))

    delete_command = [0x00, 0xE4, 0x00, 0x00, 0x00]  # Ganti dengan perintah hapus yang sesuai
    response, sw1, sw2 = send_apdu(delete_command)
    print("Delete Application Response:", toHexString(response))
    print("Status Word:", hex(sw1 << 8 | sw2))

if __name__ == "__main__":
    # Format ulang atau hapus semua data pada kartu EMV
    print("Memformat ulang kartu EMV dan menghapus semua data...")
    format_emv()
