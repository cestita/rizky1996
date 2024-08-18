from smartcard.System import readers
from smartcard.util import toHexString

# Beberapa AID yang umum digunakan dalam EMV
KNOWN_AIDS = {
    "A0000000031010": "Visa Credit or Debit",
    "A0000000041010": "MasterCard Credit or Debit",
    "A00000002501": "American Express",
    "A0000000651010": "Discover",
    "A000000333010101": "JCB",
    # Tambahkan lebih banyak AID jika diperlukan
}

def identify_aid(aid):
    # Mengubah AID ke format string
    aid_str = toHexString(aid).replace(" ", "")
    # Mencari AID dalam daftar yang diketahui
    description = KNOWN_AIDS.get(aid_str, "Unknown AID")
    return aid_str, description

def send_apdu(connection, apdu_command):
    try:
        response, sw1, sw2 = connection.transmit(apdu_command)
        print(f"APDU Sent: {toHexString(apdu_command)}")
        print(f"Response: {toHexString(response)}, SW1: {hex(sw1)}, SW2: {hex(sw2)}")
        return response, sw1, sw2
    except Exception as e:
        print(f"Error transmitting APDU: {str(e)}")
        return None, None, None

def main():
    r = readers()
    if len(r) == 0:
        print("No smart card readers detected.")
        return
    
    print(f"Using reader: {r[0]}")
    connection = r[0].createConnection()
    
    try:
        connection.connect()
    except Exception as e:
        print(f"Error connecting to the card: {str(e)}")
        return

    # APDU untuk SELECT AID (pilih aplikasi pada kartu)
    SELECT_AID_APDU = [0x00, 0xA4, 0x04, 0x00, 0x00]

    response, sw1, sw2 = send_apdu(connection, SELECT_AID_APDU)

    if sw1 == 0x6C:
        print(f"Correct length indicated by SW2: {sw2}. Retrying with the correct length.")
        SELECT_AID_APDU[4] = sw2
        response, sw1, sw2 = send_apdu(connection, SELECT_AID_APDU)

    if sw1 == 0x90 and sw2 == 0x00:
        print("AID Read Successfully")
        aid_str, aid_description = identify_aid(response)
        print(f"AID: {aid_str} - {aid_description}")
    else:
        print("Failed to read AID or no AID found.")

if __name__ == "__main__":
    main()
