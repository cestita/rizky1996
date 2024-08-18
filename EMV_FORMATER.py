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
    apdu_command = command + data
    response, sw1, sw2 = connection.transmit(apdu_command)
    return response, sw1, sw2

# Format atau hapus file di dalam chip EMV
def format_emv():
    # Contoh perintah APDU untuk format
    # Ini adalah perintah umum dan mungkin tidak sesuai dengan spesifikasi EMV Anda
    # Pastikan untuk menggunakan perintah yang benar untuk perangkat Anda
    # Misalnya, perintah SELECT FILE diikuti dengan perintah DELETE FILE
    select_file_command = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x3F, 0x00]  # SELECT FILE (Contoh)
    response, sw1, sw2 = send_apdu(select_file_command)
    print("Select File Response:", toHexString(response))
    print("Status Word:", hex(sw1 << 8 | sw2))

    delete_file_command = [0x00, 0xE4, 0x00, 0x00, 0x00]  # DELETE FILE (Contoh)
    response, sw1, sw2 = send_apdu(delete_file_command)
    print("Delete File Response:", toHexString(response))
    print("Status Word:", hex(sw1 << 8 | sw2))

def delete_all_files():
    # Contoh perintah APDU untuk menghapus semua file
    # Biasanya, Anda perlu mengetahui struktur file dan direktori kartu EMV
    # Perintah di bawah ini adalah contoh umum
    select_command = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x3F, 0x00]  # SELECT FILE (Contoh)
    response, sw1, sw2 = send_apdu(select_command)
    print("Select File Response:", toHexString(response))
    print("Status Word:", hex(sw1 << 8 | sw2))

    delete_command = [0x00, 0xE4, 0x00, 0x00, 0x00]  # DELETE FILE (Contoh)
    response, sw1, sw2 = send_apdu(delete_command)
    print("Delete File Response:", toHexString(response))
    print("Status Word:", hex(sw1 << 8 | sw2))

if __name__ == "__main__":
    # Menjalankan format atau hapus file sesuai kebutuhan
    # Gunakan dengan hati-hati!
    print("Memformat kartu EMV...")
    format_emv()
    
    print("Menghapus semua file...")
    delete_all_files()


