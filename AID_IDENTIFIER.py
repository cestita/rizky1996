from smartcard.System import readers
from smartcard.util import toHexString

# Pertama, coba perintah SELECT AID APDU dengan Lc diatur ke panjang yang benar
SELECT_AID_APDU = [0x00, 0xA4, 0x04, 0x00, 0x02]  # Adjust Lc to 2 for testing

def read_aid_from_card(connection):
    # Coba mengirim perintah SELECT AID APDU dengan Lc tertentu
    response, sw1, sw2 = connection.transmit(SELECT_AID_APDU)
    print(f"SW1: {hex(sw1)}, SW2: {hex(sw2)}")
    
    if sw1 == 0x90 and sw2 == 0x00:
        print("AID Read Successfully")
        print("AID:", toHexString(response))
    elif sw1 == 0x6C:
        print(f"Correct length indicated by SW2: {sw2}. Retrying with the correct length.")
        SELECT_AID_APDU[4] = sw2
        response, sw1, sw2 = connection.transmit(SELECT_AID_APDU)
        if sw1 == 0x90 and sw2 == 0x00:
            print("AID Read Successfully after adjusting length.")
            print("AID:", toHexString(response))
        else:
            print("Failed to read AID after adjusting length.")
    else:
        print("Failed to read AID or no AID found.")

def main():
    # Mendeteksi pembaca kartu
    r = readers()
    if len(r) == 0:
        print("No smart card readers detected.")
        return
    
    print(f"Using reader: {r[0]}")
    connection = r[0].createConnection()
    connection.connect()

    # Membaca AID dari kartu
    read_aid_from_card(connection)

if __name__ == "__main__":
    main()
