from smartcard.System import readers
from smartcard.util import toHexString

# Perintah untuk SELECT PSE (Payment System Environment)
SELECT_PSE = [0x00, 0xA4, 0x04, 0x00, 0x0E] + [0x31, 0x50, 0x41, 0x59, 0x2E, 0x53, 0x59, 0x53, 0x2E, 0x44, 0x44, 0x46, 0x30, 0x31]  # 1PAY.SYS.DDF01

def send_apdu(connection, apdu):
    try:
        response, sw1, sw2 = connection.transmit(apdu)
        print(f'APDU: {toHexString(apdu)}, Response: {toHexString(response)}, SW1 SW2: {sw1:02X} {sw2:02X}')
        return response, sw1, sw2
    except Exception as e:
        print(f"Error transmitting APDU: {str(e)}")
        return None, None, None

def parse_aid(response):
    aids = []
    i = 0
    while i < len(response):
        if response[i] == 0x4F:  # 0x4F adalah tag AID
            aid_length = response[i+1]
            aid = response[i+2:i+2+aid_length]
            aids.append(aid)
            i += 2 + aid_length
        else:
            i += 1
    return aids

def select_pse_and_list_aids(connection):
    print("Selecting Payment System Environment (PSE)...")
    response, sw1, sw2 = send_apdu(connection, SELECT_PSE)
    
    if sw1 == 0x90 and sw2 == 0x00:
        print("PSE selected successfully, listing AIDs...")
        aids = parse_aid(response)
        if aids:
            for idx, aid in enumerate(aids):
                print(f"AID {idx+1}: {toHexString(aid)}")
        else:
            print("No AIDs found in PSE.")
    else:
        print(f"Failed to select PSE: SW1={sw1:02X}, SW2={sw2:02X}")

def main():
    r = readers()
    if len(r) == 0:
        print("No smart card readers found")
        return
    
    reader = r[0]
    connection = reader.createConnection()
    connection.connect()

    print("Connected to card")
    select_pse_and_list_aids(connection)

if __name__ == "__main__":
    main()
