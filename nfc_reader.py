import nfc
import binascii

def on_connect(tag):
    """Callback function when a card is detected."""
    print("Kartu NFC terdeteksi")
    
    # Menampilkan UID kartu
    uid = tag.identifier
    print("UID Kartu:", binascii.hexlify(uid).decode('utf-8'))

    # Menampilkan informasi teknologi kartu
    print("Teknologi Kartu:", tag.tech)

    # Jika tag mendukung NDEF (misalnya link atau informasi kontak)
    if tag.ndef:
        print("\nKartu ini mendukung NDEF (NFC Data Exchange Format)")
        print("NDEF Tipe:", tag.ndef.type)
        print("Ukuran NDEF:", tag.ndef.capacity, "byte")
        print("Pesan NDEF:", tag.ndef.message)
        
        # Baca isi pesan NDEF
        for record in tag.ndef.records:
            print("\nTipe Record:", record.type)
            print("Data Record:", record.text or record.uri or record.data)

    # Jika kartu bukan NDEF, coba baca informasi lain yang ada di dalamnya
    else:
        print("\nKartu ini bukan NDEF, mencoba membaca data sektor...")

        if hasattr(tag, 'dump'):
            # Dump seluruh data kartu
            print("\nData lengkap dari kartu (dump):")
            tag.dump()
        else:
            # Jika kartu tidak memiliki metode dump, menampilkan informasi dasar
            print("\nInformasi dasar dari kartu:")
            print(tag)

    return True  # Menandakan pembacaan selesai dan berhasil

def read_nfc():
    """Menghubungkan ke pembaca NFC dan menunggu kartu ditempelkan."""
    try:
        clf = nfc.ContactlessFrontend('usb')  # Pastikan pembaca NFC terhubung melalui USB
        print("Tunggu kartu NFC ditempelkan...")
        clf.connect(rdwr={'on-connect': on_connect})  # Menunggu kartu NFC ditempelkan
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if clf:
            clf.close()

if __name__ == '__main__':
    read_nfc()
