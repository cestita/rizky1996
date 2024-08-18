from smartcard.System import readers
from smartcard.util import toHexString

# Perintah APDU untuk SELECT FILE untuk mendapatkan AID
SELECT_AID_APDU = [0x00, 0xA4, 0x04, 0x00, 0x00]  # Select AID command with P1, P2, and Lc fields

def read_aid_from_card(connection):
    # Mengirimkan perintah SELECT AID APDU
    response, sw1, sw2 = connection.transmit(SELECT_AID_APDU)
    print(f"SW1: {hex(sw1)}, SW2: {hex(sw2)}")
    
    if sw1 == 0x90 and sw2 == 0x00:
        print("AID Read Successfully")
        print("AID:", toHexString(response))
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
