from smartcard.System import readers
from smartcard.util import toHexString

# Daftar APDU yang disesuaikan untuk menghindari kesalahan P1/P2
CLEAR_APDU_COMMANDS = [
    [0x00, 0xA4, 0x04, 0x00, 0x02, 0x3F, 0x00],  # Pilih Master File (ID: 3F00) dengan P1=0x04, P2=0x00
    [0x00, 0xE4, 0x00, 0x00, 0x00],              # Hapus File (Contoh APDU dengan P1=0x00, P2=0x00)
    [0x00, 0xD6, 0x00, 0x00, 0x10] + [0x00]*16,  # Update Biner dengan data 0 (P1=0x00, P2=0x00)
]

def send_apdu(connection, apdu):
    try:
        response, sw1, sw2 = connection.transmit(apdu)
        print(f'APDU: {toHexString(apdu)}, Response: {toHexString(response)}, SW1 SW2: {sw1:02X} {sw2:02X}')
        return sw1, sw2
    except Exception as e:
        print(f"Error transmitting APDU: {str(e)}")
        return None, None

def clear_emv_card(connection):
    for apdu in CLEAR_APDU_COMMANDS:
        sw1, sw2 = send_apdu(connection, apdu)
        
        if sw1 is None or sw2 is None:
            print("Failed to send APDU command")
            break
        
        if sw1 == 0x90 and sw2 == 0x00:
            print("Command executed successfully")
        elif sw1 == 0x6A and sw2 == 0x86:
            print("Incorrect P1 or P2 parameter: Check the command structure.")
            break
        elif sw1 == 0x6A and sw2 == 0x82:
            print("File not found: The file you are trying to select or modify does not exist.")
            break
        elif sw1 == 0x69 and sw2 == 0x82:
            print("Security status not satisfied: Authentication may be required.")
            break
        else:
            print(f"Failed to execute command: SW1={sw1:02X}, SW2={sw2:02X}")
            break

def main():
    r = readers()
    if len(r) == 0:
        print("No smart card readers found")
        return
    
    reader = r[0]
    connection = reader.createConnection()
    connection.connect()

    print("Connected to card")
    clear_emv_card(connection)

if __name__ == "__main__":
    main()
