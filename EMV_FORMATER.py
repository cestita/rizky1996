from smartcard.System import readers
from smartcard.util import toHexString

# Contoh AID untuk aplikasi EMV (seperti Visa atau Mastercard)
AID = [0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10]  # Visa AID sebagai contoh

# APDU commands
SELECT_AID_APDU = [0x00, 0xA4, 0x04, 0x00, len(AID)] + AID  # Pilih aplikasi berdasarkan AID

def send_apdu(connection, apdu):
    try:
        response, sw1, sw2 = connection.transmit(apdu)
        print(f'APDU: {toHexString(apdu)}, Response: {toHexString(response)}, SW1 SW2: {sw1:02X} {sw2:02X}')
        return sw1, sw2
    except Exception as e:
        print(f"Error transmitting APDU: {str(e)}")
        return None, None

def select_aid(connection):
    print("Selecting application using AID...")
    sw1, sw2 = send_apdu(connection, SELECT_AID_APDU)
    
    if sw1 == 0x90 and sw2 == 0x00:
        print("Application selected successfully")
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
    select_aid(connection)

if __name__ == "__main__":
    main()
