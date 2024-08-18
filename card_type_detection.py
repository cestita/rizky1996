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
    pse_aid = [0x1F, 0x01]  # PSE AID: 1PAY.SYS.DDF01
    select_pse_apdu = [0x00, 0xA4, 0x04, 0x00, len(pse_aid)] + pse_aid + [0x00]
    response, sw1, sw2 = send_apdu(connection, select_pse_apdu)
    if sw1 == 0x90 and sw2 == 0x00:
        return response
    elif sw1 == 0x6A and sw2 == 0x82:
        print("PSE AID not found. Trying different AID...")
        # Try another PSE AID
        alternate_pse_aid = [0x2F, 0x01]  # Example alternative PSE AID
        select_alternate_pse_apdu = [0x00, 0xA4, 0x04, 0x00, len(alternate_pse_aid)] + alternate_pse_aid + [0x00]
        response, sw1, sw2 = send_apdu(connection, select_alternate_pse_apdu)
        if sw1 == 0x90 and sw2 == 0x00:
            return response
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

    # Attempt to select PSE
    print("Attempting to select PSE (1PAY.SYS.DDF01)...")
    pse_response = select_pse(connection)
    if pse_response:
        print("PSE selected successfully.")
        
        # Example AID for Visa
        visa_aid = [0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10]  # Visa AID
        app_response = select_aid(connection, visa_aid)
        if app_response:
            print(f"Visa AID Selected: {toHexString(visa_aid)}")
            print(f"Application data: {toHexString(app_response)}")
            
            # Read application data
            print("Reading application data...")
            read_data_response = read_application_data(connection)
            if read_data_response:
                print(f"Application data read: {toHexString(read_data_response)}")
        else:
            print("Failed to select Visa AID")
    else:
        print("PSE selection failed.")

if __name__ == "__main__":
    main()
