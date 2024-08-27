from smartcard.System import readers
from smartcard.util import toHexString

# AID yang ditemukan pada kartu
AID = [0xA0, 0x00, 0x00, 0x06, 0x02, 0x10, 0x10]  # AID: A0000006021010

# APDU command to select application by AID
SELECT_AID_APDU = [0x00, 0xA4, 0x04, 0x00, len(AID)] + AID

# APDU command to delete file (contoh, ganti dengan ID file yang benar)
DELETE_FILE_APDU = [0x00, 0xE4, 0x00, 0x00, 0x02, 0x3F, 0x00]  # Contoh, ganti sesuai dengan ID file yang benar

# Command GET RESPONSE
GET_RESPONSE_APDU = [0x00, 0xC0, 0x00, 0x00]  # GET RESPONSE command skeleton

def send_apdu(connection, apdu):
    try:
        response, sw1, sw2 = connection.transmit(apdu)
        print(f'APDU: {toHexString(apdu)}, Response: {toHexString(response)}, SW1 SW2: {sw1:02X} {sw2:02X}')
        return response, sw1, sw2
    except Exception as e:
        print(f"Error transmitting APDU: {str(e)}")
        return None, None, None

def get_response(connection, length):
    apdu = GET_RESPONSE_APDU + [length]
    response, sw1, sw2 = send_apdu(connection, apdu)
    return response, sw1, sw2

def delete_files(connection):
    print("Attempting to delete files on the card...")
    response, sw1, sw2 = send_apdu(connection, DELETE_FILE_APDU)
    if sw1 == 0x90 and sw2 == 0x00:
        print("File deleted successfully")
    elif sw1 == 0x69 and sw2 == 0x82:
        print("Security status not satisfied, deletion failed")
    elif sw1 == 0x6A and sw2 == 0x82:
        print("File or application not found")
    else:
        print(f"Failed to delete file: SW1={sw1:02X}, SW2={sw2:02X}")

def select_application_by_aid(connection):
    print(f"Selecting application using AID: {toHexString(AID)}")
    response, sw1, sw2 = send_apdu(connection, SELECT_AID_APDU)
    
    if sw1 == 0x90 and sw2 == 0x00:
        print("Application selected successfully")
        delete_files(connection)  # Try to delete files after selecting application
    elif sw1 == 0x61:
        print(f"More data available: {sw2} bytes")
        response, sw1, sw2 = get_response(connection, sw2)
        print(f"GET RESPONSE: {toHexString(response)}, SW1 SW2: {sw1:02X} {sw2:02X}")
    elif sw1 == 0x6A and sw2 == 0x82:
        print("File or application not found")
    else:
        print(f"Failed to select application: SW1={sw1:02X}, SW2={sw2:02X}")

def main():
    r = readers()
    if len(r) == 0:
        print("No smart card readers found")
        return
    
    reader = r[0]
    connection = reader.createConnection()
    connection.connect()

    print("Connected to card")
    select_application_by_aid(connection)

if __name__ == "__main__":
    main()
