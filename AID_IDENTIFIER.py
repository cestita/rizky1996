from smartcard.System import readers
from smartcard.util import toHexString, toBytes

# Beberapa AID yang umum digunakan dalam EMV
KNOWN_AIDS = {
    "A0000000031010": "Visa Credit or Debit",
    "A0000000041010": "MasterCard Credit or Debit",
    "A00000002501": "American Express",
    "A0000000651010": "Discover",
    "A000000333010101": "JCB",
    # Tambahkan lebih banyak AID jika diperlukan
}

def send_apdu(connection, apdu_command):
    try:
        response, sw1, sw2 = connection.transmit(apdu_command)
        print(f"APDU Sent: {toHexString(apdu_command)}")
        print(f"Response: {toHexString(response)}, SW1: {hex(sw1)}, SW2: {hex(sw2)}\n")
        return response, sw1, sw2
    except Exception as e:
        print(f"Error transmitting APDU: {str(e)}")
        return None, None, None

def select_pse(connection):
    # SELECT 1PAY.SYS.DDF01
    pse_name = '1PAY.SYS.DDF01'
    pse_select_apdu = [0x00, 0xA4, 0x04, 0x00, len(pse_name)] + list(pse_name.encode('ascii')) + [0x00]
    response, sw1, sw2 = send_apdu(connection, pse_select_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        return response
    else:
        # Jika gagal, coba SELECT 2PAY.SYS.DDF01
        pse_name = '2PAY.SYS.DDF01'
        pse_select_apdu = [0x00, 0xA4, 0x04, 0x00, len(pse_name)] + list(pse_name.encode('ascii')) + [0x00]
        response, sw1, sw2 = send_apdu(connection, pse_select_apdu)
        if sw1 == 0x90 and sw2 == 0x00:
            return response
    return None

def parse_fci(response):
    aids = []
    i = 0
    while i < len(response):
        if response[i] == 0x4F:  # Tag '4F' indicates AID
            length = response[i+1]
            aid = response[i+2:i+2+length]
            aids.append(aid)
            i += 2 + length
        else:
            i += 1
    return aids

def select_aid(connection, aid):
    select_aid_apdu = [0x00, 0xA4, 0x04, 0x00, len(aid)] + aid + [0x00]
    response, sw1, sw2 = send_apdu(connection, select_aid_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        return response
    else:
        return None

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

    # Step 1: Select PSE
    pse_response = select_pse(connection)
    if not pse_response:
        print("Failed to select PSE.")
        return

    # Step 2: Parse FCI to get list of AIDs
    aids = parse_fci(pse_response)
    if not aids:
        print("No AIDs found in PSE.")
        return

    print("AIDs found:")
    for aid in aids:
        aid_str = toHexString(aid).replace(" ", "")
        description = KNOWN_AIDS.get(aid_str, "Unknown AID")
        print(f"AID: {aid_str} - {description}")

    # Step 3: Select each AID and retrieve application data
    for aid in aids:
        print(f"\nSelecting AID: {toHexString(aid).replace(' ', '')}")
        app_response = select_aid(connection, aid)
        if app_response:
            print(f"Application data for AID {toHexString(aid).replace(' ', '')}:")
            print(toHexString(app_response))
        else:
            print(f"Failed to select AID {toHexString(aid).replace(' ', '')}")

if __name__ == "__main__":
    main()
