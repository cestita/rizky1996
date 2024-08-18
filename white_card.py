import json
from smartcard.System import readers
from smartcard.util import toHexString

# Fungsi untuk menulis data ke kartu chip menggunakan APDU
def write_data_to_card(connection, data):
    for record in data:
        apdu_command = record['apdu_command']
        apdu_data = record['data']
        apdu = apdu_command + apdu_data
        response, sw1, sw2 = connection.transmit(apdu)
        print(f"APDU Sent: {toHexString(apdu)}")
        print(f"Response: {toHexString(response)}, SW1={hex(sw1)}, SW2={hex(sw2)}")
        if sw1 != 0x90 or sw2 != 0x00:
            print(f"Error writing to card: SW1={hex(sw1)}, SW2={hex(sw2)}")
            break

# Membaca file data yang disimpan dari Cardpeek
with open('card_data.json', 'r') as f:
    card_data = json.load(f)

# Memilih pembaca kartu
r = readers()
if len(r) == 0:
    print("No smart card readers detected.")
    exit()

print(f"Using reader: {r[0]}")
connection = r[0].createConnection()
connection.connect()

# Menulis data ke kartu
write_data_to_card(connection, card_data)

print("Data writing completed.")
