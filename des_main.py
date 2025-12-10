# DES Main Program
print("=" * 50)
print("DES ENCRYPTION/DECRYPTION")
print("=" * 50)

# Import our DES functions
from des_keygen import make_keys
from des_encrypt import encrypt
from des_decrypt import decrypt

# Helper functions
def hex_to_bits(hex_str):
    """Convert hex like 'A3' to bits [1,0,1,0,0,0,1,1]"""
    bits = []
    for char in hex_str:
        num = int(char, 16)
        bits.append((num >> 3) & 1)
        bits.append((num >> 2) & 1)
        bits.append((num >> 1) & 1)
        bits.append(num & 1)
    return bits

def bits_to_hex(bits):
    """Convert bits to hex string"""
    hex_str = ""
    for i in range(0, len(bits), 4):
        val = (bits[i] << 3) | (bits[i+1] << 2) | (bits[i+2] << 1) | bits[i+3]
        hex_str += format(val, 'X')
    return hex_str

# Test data
plaintext = "0123456789ABCDEF"  # 64-bit data
key = "133457799BBCDFF1"        # 64-bit key

print(f"Plaintext: {plaintext}")
print(f"Key:       {key}")

# Convert to bits
pt_bits = hex_to_bits(plaintext)
key_bits = hex_to_bits(key)

# Encrypt
ct_bits = encrypt(pt_bits, key_bits)
ct_hex = bits_to_hex(ct_bits)
print(f"\nEncrypted: {ct_hex}")

# Decrypt
dt_bits = decrypt(ct_bits, key_bits)
dt_hex = bits_to_hex(dt_bits)
print(f"Decrypted: {dt_hex}")

# Check
if dt_hex == plaintext:
    print("\n✓ SUCCESS! Works correctly")
else:
    print("\n✗ FAILED")

print("=" * 50)