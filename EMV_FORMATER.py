from smartcard.System import readers
from smartcard.util import toHexString

# AID untuk Visa dan MasterCard
AID_VISA_CREDIT = [0xA0, 0x00, 0x00, 0x03, 0x10, 0x10]  # Visa Credit
AID_VISA_DEBIT = [0xA0, 0x00, 0x00, 0x03, 0x20, 0x10]  # Visa Debit
AID_VISA_ELECTRON = [0xA0, 0x00, 0x00, 0x03, 0x30, 0x10]  # Visa Electron

AID_MC_CREDIT = [0xA0, 0x00, 0x00, 0x04, 0x10, 0x10]  # MasterCard Credit
AID_MC_DEBIT = [0xA0, 0x00, 0x00, 0x04, 0x20, 0x10]  # MasterCard Debit
AID_MC_MAESTRO = [0xA0, 0x00, 0x00, 0x04, 0x30, 0x10]  # MasterCard Maestro

# Pilih AID yang diinginkan
AID_OPTIONS = {
    '1': AID_VISA_CREDIT,
    '2': AID_VISA_DEBIT,
    '3': AID_VISA_ELECTRON,
    '4': AID_MC_CREDIT,
    '5': AID_MC_DEBIT,
    '6': AID_MC_MAESTRO
}

# APDU command untuk memilih aplikasi dengan AID
def get_select_apdu(aid):
    return [0x00, 0xA4, 0x04, 0x00, len(aid)] + aid

# APDU command untuk DELETE FILE atau CLEAR FILE
DELETE_FILE_APDU = [0x00, 0xE4, 0x00, 0x00, 0x02, 0x3F, 0x00]  # Contoh, ganti sesuai dengan ID file yang benar jika diketahui

# Perintah untuk format ulang aplikasi (jika kartu mendukung)
FORMAT_APDU = [0x00, 0xE0, 0x00, 0x00, 0x00]  # Format ulang, jika didukung oleh kartu

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

def format_card(connection):
    print("Attempting to format the card...")
    response, sw1, sw2 = send_apdu(connection, FORMAT_APDU)
    if sw1 == 0x90 and sw2 == 0x00:
        print("Card formatted successfully")
    elif sw1 == 0x69 and sw2 == 0x82:
        print("Security status not satisfied, formatting failed")
    elif sw1 == 0x6A and sw2 == 0x82:
        print("Format not supported or application not found")
    else:
        print(f"Failed to format card: SW1={sw1:02X}, SW2={sw2:02X}")

def select_application_by_aid(connection, aid):
    apdu = get_select_apdu(aid)
    print(f"Selecting application using AID: {toHexString(aid)}")
    response, sw1, sw2 = send_apdu(connection, apdu)
    
    if sw1 == 0x90 and sw2 == 0x00:
        print("Application selected successfully")
        delete_files(connection)  # Try to delete files after selecting application
        format_card(connection)   # Attempt to format the card
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

    while True:
        print("\nSelect AID to test:")
        print("1: Visa Credit")
        print("2: Visa Debit")
        print("3: Visa Electron")
        print("4: MasterCard Credit")
        print("5: MasterCard Debit")
        print("6: MasterCard Maestro")
        print("Q: Quit")

        choice = input("Enter choice: ").strip().upper()
        
        if choice == 'Q':
            print("Exiting...")
            break

        aid = AID_OPTIONS.get(choice)
        if aid:
            select_application_by_aid(connection, aid)
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
