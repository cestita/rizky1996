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

def select_application(connection, aid):
    select_apdu = [0x00, 0xA4, 0x04, 0x00, len(aid)] + aid
    response, sw1, sw2 = send_apdu(connection, select_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Application selected successfully.")
    else:
        print(f"Failed to select application. SW1: {hex(sw1)}, SW2: {hex(sw2)}")

def format_application_data(connection):
    # Example APDU command to format data; adjust according to your specific application requirements
    format_apdu = [0x00, 0xE4, 0x00, 0x00, 0x00]  # This is an example and may not be valid for all cards
    response, sw1, sw2 = send_apdu(connection, format_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Data formatted successfully.")
    else:
        print(f"Failed to format data. SW1: {hex(sw1)}, SW2: {hex(sw2)}")

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

    # Example AID for application
    example_aid = [0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10]  # Adjust AID as needed
    select_application(connection, example_aid)

    format_application_data(connection)

if __name__ == "__main__":
    main()
