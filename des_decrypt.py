# DES Decryption
from des_keygen import make_keys
from des_tables import IP, FP
from des_encrypt import shuffle, xor

def decrypt(ciphertext, key):
    """Decrypt 64-bit ciphertext"""
    # Make keys
    keys = make_keys(key)
    
    # Use keys in reverse order
    rev_keys = keys[::-1]
    
    # Initial permutation
    data = shuffle(ciphertext, IP)
    
    # Split
    left = data[:32]
    right = data[32:]
    
    # Import F function from encrypt
    from des_encrypt import encrypt
    # We'll just reuse encrypt with reversed keys
    # Actually, we need to recreate the F function
    
    # Simple F function (same as encrypt.py)
    from des_tables import E, P, S_BOX
    
    def f_function(right_bits, round_key):
        expanded = shuffle(right_bits, E)
        mixed = xor(expanded, round_key)
        
        # S-box (simplified)
        sbox_out = []
        chunk = mixed[:6]
        row = (chunk[0] << 1) | chunk[5]
        col = (chunk[1] << 3) | (chunk[2] << 2) | (chunk[3] << 1) | chunk[4]
        value = S_BOX[row][col]
        sbox_out.append((value >> 3) & 1)
        sbox_out.append((value >> 2) & 1)
        sbox_out.append((value >> 1) & 1)
        sbox_out.append(value & 1)
        sbox_out = sbox_out * 8
        
        result = shuffle(sbox_out, P)
        return result
    
    # 16 rounds with reversed keys
    for i in range(16):
        old_right = right.copy()
        f_result = f_function(right, rev_keys[i])
        right = xor(left, f_result)
        left = old_right
    
    # Final permutation
    combined = right + left
    plain = shuffle(combined, FP)
    
    return plain

# Test
if __name__ == "__main__":
    from des_encrypt import encrypt
    pt = [0,1] * 32
    k = [1,0] * 32
    ct = encrypt(pt, k)
    dt = decrypt(ct, k)
    
    if pt == dt:
        print("✓ Decryption works!")
    else:
        print("✗ Decryption failed")