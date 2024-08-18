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

# Langsung memilih dan menghapus aplikasi berdasarkan AID tanpa memilih Master File
def format_emv():
    # Daftar beberapa AID umum yang bisa dicoba
    aids = [
        "A0000000031010",  # Visa
        "A0000000041010",  # MasterCard
        "A0000000250101",  # JCB
        "A0000003330101",  # American Express
        "A0000005271101"   # Discover
    ]
    
    for aid in aids:
        print(f"Mencoba AID: {aid}")

        # Pilih Aplikasi dengan AID
        select_application_command = [0x00, 0xA4, 0x04, 0x00, len(aid) // 2] + [int(aid[i:i+2], 16) for i in range(0, len(aid), 2)]
        response, sw1, sw2 = send_apdu(select_application_command)
        print(f"Select Application (AID: {aid}) Response:", toHexString(response))
        print("Status Word:", hex(sw1 << 8 | sw2))

        if sw1 << 8 | sw2 == 0x9000:  # 0x9000 = Success
            # Hapus File atau Aplikasi yang dipilih
            delete_file_command = [0x00, 0xE4, 0x00, 0x00, 0x00]  # DELETE FILE (Contoh)
            response, sw1, sw2 = send_apdu(delete_file_command)
            print(f"Delete File (AID: {aid}) Response:", toHexString(response))
            print("Status Word:", hex(sw1 << 8 | sw2))
        else:
            print(f"Gagal memilih aplikasi dengan AID {aid}.")

if __name__ == "__main__":
    # Langsung format ulang atau hapus data pada kartu EMV
    print("Langsung memformat ulang kartu EMV dan meng
