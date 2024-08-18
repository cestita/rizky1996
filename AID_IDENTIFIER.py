from smartcard.System import readers
from smartcard.util import toHexString

KNOWN_AIDS = {
    "A0000000031010": "Visa Credit or Debit",
    "A0000000041010": "MasterCard Credit or Debit",
    "A00000002501": "American Express",
    "A0000000651010": "Discover",
    "A000000333010101": "JCB",
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

def select_aid(connection, aid):
    select_aid_apdu = [0x00, 0xA4, 0x04, 0x00, len(aid)] + aid + [0x00]
    response, sw1, sw2 = send_apdu(connection, select_aid_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        return response
    else:
        print(f"Failed to select AID: {toHexString(aid)}")
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

    # AID yang diketahui
    aids_to_try = [
        [0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10],  # Visa
        [0xA0, 0x00, 0x00, 0x00, 0x04, 0x10, 0x10],  # MasterCard
        [0xA0, 0x00, 0x00, 0x00, 0x25, 0x01],        # American Express
        [0xA0, 0x00, 0x00, 0x00, 0x65, 0x10, 0x10],  # Discover
        [0xA0, 0x00, 0x00, 0x33, 0x01, 0x01, 0x01],  # JCB
    ]

    for aid in aids_to_try:
        print(f"\nAttempting to select AID: {toHexString(aid).replace(' ', '')}")
        app_response = select_aid(connection, aid)
        if app_response:
            aid_str = toHexString(aid).replace(' ', '')
            description = KNOWN_AIDS.get(aid_str, "Unknown AID")
            print(f"Selected AID: {aid_str} - {description}")
            print(f"Application data for AID {aid_str}:")
            print(toHexString(app_response))
            break  # Stop after the first successful AID selection
        else:
            print(f"Failed to select AID: {toHexString(aid).replace(' ', '')}")

if __name__ == "__main__":
    main()
