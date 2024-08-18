from smartcard.System import readers
from smartcard.util import toHexString

def send_apdu(connection, apdu_command):
    try:
        response, sw1, sw2 = connection.transmit(apdu_command)
        print(f"APDU Sent: {toHexString(apdu_command)}")
        print(f"Response: {toHexString(response)}, SW1: {hex(sw1)}, SW2: {hex(sw2)}")
        return response, sw1, sw2
    except Exception as e:
        print(f"Error transmitting APDU: {str(e)}")
        return None, None, None

def get_atr(connection):
    atr = connection.getATR()
    print(f"ATR: {toHexString(atr)}")

def select_application(connection, aid):
    select_apdu = [0x00, 0xA4, 0x04, 0x00, len(aid)] + aid
    response, sw1, sw2 = send_apdu(connection, select_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Application selected successfully.")
    else:
        print(f"Failed to select application. SW1: {hex(sw1)}, SW2: {hex(sw2)}")

def read_data(connection):
    # Example APDU command to read file; adjust according to your specific application requirements
    read_apdu = [0x00, 0xB0, 0x00, 0x00, 0x00]  # Example command for reading
    response, sw1, sw2 = send_apdu(connection, read_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Data read successfully.")
        print(f"Data: {toHexString(response)}")
    else:
        print(f"Failed to read data. SW1: {hex(sw1)}, SW2: {hex(sw2)}")

def read_track2(connection):
    # Assuming track data can be read with specific APDU
    # This is an example; track data reading method might differ
    track2_apdu = [0x00, 0xB2, 0x00, 0x00, 0x00]  # Example command for reading Track 2
    response, sw1, sw2 = send_apdu(connection, track2_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Track 2 data read successfully.")
        print(f"Track 2 Data: {toHexString(response)}")
    else:
        print(f"Failed to read Track 2 data. SW1: {hex(sw1)}, SW2: {hex(sw2)}")

def extract_aid_and_application(connection):
    # Example APDU command to get AID from the card
    aid_apdu = [0x00, 0xA4, 0x00, 0x00, 0x00]  # Example command to get AID
    response, sw1, sw2 = send_apdu(connection, aid_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        print("AID read successfully.")
        print(f"AID: {toHexString(response)}")
    else:
        print(f"Failed to read AID. SW1: {hex(sw1)}, SW2: {hex(sw2)}")

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

    get_atr(connection)

    # Example AID for application; adjust as needed
    example_aid = [0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10]
    select_application(connection, example_aid)

    read_data(connection)
    read_track2(connection)
    extract_aid_and_application(connection)

if __name__ == "__main__":
    main()
