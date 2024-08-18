import sys
from smartcard.System import readers
from smartcard.util import toHexString, toBytes

def get_atr(connection):
    atr = connection.getATR()
    print(f"ATR: {toHexString(atr)}")
    return atr

def select_application(connection):
    # AID untuk aplikasi EMV (contoh AID untuk aplikasi pembayaran umum)
    SELECT = [0x00, 0xA4, 0x04, 0x00, 0x07, 0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10, 0x00]
    data, sw1, sw2 = connection.transmit(SELECT)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Application selected successfully.")
    else:
        print(f"Failed to select application: {sw1:02X} {sw2:02X}")
    return data

def get_apdu_response(connection, apdu_command):
    response, sw1, sw2 = connection.transmit(apdu_command)
    print(f"APDU Command: {toHexString(apdu_command)}")
    print(f"Response: {toHexString(response)}")
    print(f"Status Word: {sw1:02X} {sw2:02X}")
    return response, sw1, sw2

def read_track_1_data(connection):
    # Perintah untuk membaca Track 1 data
    GET_TRACK_1 = [0x00, 0xB2, 0x01, 0x0C, 0x00]
    response, sw1, sw2 = get_apdu_response(connection, GET_TRACK_1)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Track 1 Data:")
        print(response)
    else:
        print(f"Failed to read Track 1 Data: {sw1:02X} {sw2:02X}")

def read_track_2_data(connection):
    # Perintah untuk membaca Track 2 data
    GET_TRACK_2 = [0x00, 0xB2, 0x02, 0x0C, 0x00]
    response, sw1, sw2 = get_apdu_response(connection, GET_TRACK_2)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Track 2 Data:")
        print(response)
    else:
        print(f"Failed to read Track 2 Data: {sw1:02X} {sw2:02X}")

def read_aqr(connection):
    # Perintah untuk mengambil Application Cryptogram (AC)
    GET_AQR = [0x80, 0xAE, 0x00, 0x00, 0x00]
    response, sw1, sw2 = get_apdu_response(connection, GET_AQR)
    if sw1 == 0x90 and sw2 == 0x00:
        print("AQR (Application Cryptogram Request):")
        print(response)
    else:
        print(f"Failed to get AQR: {sw1:02X} {sw2:02X}")

def main():
    # Mendapatkan daftar pembaca kartu
    r = readers()
    if len(r) == 0:
        print("No smart card readers found.")
        sys.exit()

    print("Available readers:", r)

    reader = r[0]  # Menggunakan pembaca pertama
    connection = reader.createConnection()
    connection.connect()

    atr = get_atr(connection)
    application_data = select_application(connection)

    # Membaca informasi Track 1, Track 2, dan AQR
    read_track_1_data(connection)
    read_track_2_data(connection)
    read_aqr(connection)

if __name__ == "__main__":
    main()
