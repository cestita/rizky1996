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
    # Ini adalah contoh perintah untuk memilih Master File atau Application Directory
    select_file_command = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x3F, 0x00]  # SELECT MASTER FILE
    response, sw1, sw2 = send_apdu(select_file_command)
    print("Select File Response:", toHexString(response))
    print("Status Word:", hex(sw1 << 8 | sw2))
    
    if sw1 << 8 | sw2 != 0x9000:  # 0x9000 = Success
        print("Gagal memilih file master.")
        return

    # Langkah 2: Hapus Aplikasi atau File yang Ditemukan
    # Ini adalah contoh perintah untuk menghapus file atau aplikasi
    # Harap ganti dengan perintah yang sesuai untuk file atau aplikasi yang ingin dihapus
    delete_file_command = [0x00, 0xE4, 0x00, 0x00, 0x00]  # DELETE FILE (Contoh, sesuaikan jika perlu)
    response, sw1, sw2 = send_apdu(delete_file_command)
    print("Delete File Response:", toHexString(response))
    print("Status Word:", hex(sw1 << 8 | sw2))
    
    if sw1 << 8 | sw2 != 0x9000:  # 0x9000 = Success
        print("Gagal menghapus file.")
        return

    # Langkah 3: Pilih dan hapus direktori atau aplikasi lain jika perlu
    # Contoh untuk memilih dan menghapus direktori atau aplikasi lain
    # Sesuaikan dengan AID atau DF yang benar
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
