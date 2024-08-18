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

def select_pse(connection):
    pse = [0x31, 0x50, 0x41, 0x59, 0x2E, 0x53, 0x59, 0x53, 0x2E, 0x44, 0x44, 0x46, 0x30, 0x31]  # '1PAY.SYS.DDF01'
    select_pse_apdu = [0x00, 0xA4, 0x04, 0x00, len(pse)] + pse + [0x00]
    response, sw1, sw2 = send_apdu(connection, select_pse_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        return response
    else:
        print("Failed to select PSE")
        return None

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

    print("Attempting to select PSE (1PAY.SYS.DDF01)...")
    pse_response = select_pse(connection)
    if pse_response:
        print(f"PSE selected successfully.")
        # Analyze the response if needed to extract AIDs
        
    else:
        print("PSE selection failed. Attempting to select known AIDs directly.")
        known_aid = [0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10]  # Visa AID for example
        app_response = select_aid(connection, known_aid)
        if app_response:
            print(f"AID Selected: {toHexString(known_aid)}")
            print(f"Application data: {toHexString(app_response)}")
        else:
            print("Failed to select known AID")

if __name__ == "__main__":
    main()
