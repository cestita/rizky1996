from smartcard.System import readers
from smartcard.util import toHexString

def send_apdu(connection, apdu_command):
    try:
        response, sw1, sw2 = connection.transmit(apdu_command)
        print(f"APDU Sent: {toHexString(apdu_command)}")
        print(f"Response: {toHexString(response)}, SW1: {hex(sw1)}, SW2: {hex(sw2)}\n")
        return response, sw1, sw2
    except Exception as e:
        print(f"Error transmitting APDU: {str(e)}")
        return None, None, None

def detect_card_type(connection):
    print("Detecting card type...")
    # Basic SELECT command to check for smartcard, javacard, or other
    apdu = [0x00, 0xA4, 0x04, 0x00, 0x00]  # Select MF or AID
    
    response, sw1, sw2 = send_apdu(connection, apdu)
    
    if sw1 == 0x6A and sw2 == 0x82:
        print("Card type: Smartcard")
    elif sw1 == 0x90 and sw2 == 0x00:
        print("Card type: Possibly JavaCard")
    else:
        print("Card type: Unknown or unsupported")
    
    return response, sw1, sw2

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

    # Detect the card type
    response, sw1, sw2 = detect_card_type(connection)
    
    if sw1 == 0x90 and sw2 == 0x00:
        print("Sending additional APDU commands for more information...\n")
        
        # Example APDU commands to retrieve card information
        get_data_apdu = [0x80, 0xCA, 0x9F, 0x7F, 0x00]  # Get processing options (example)
        select_apdu = [0x00, 0xA4, 0x04, 0x00, 0x07, 0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10, 0x00]  # Select Visa AID (example)
        
        send_apdu(connection, get_data_apdu)
        send_apdu(connection, select_apdu)
    else:
        print("Card type could not be determined or unsupported APDU response.")

if __name__ == "__main__":
    main()
