# DES Encryption
from des_keygen import make_keys
from des_tables import IP, FP, E, P, S_BOX

def shuffle(bits, table):
    """Rearrange bits using table"""
    result = []
    for pos in table:
        result.append(bits[pos-1])
    return result

def xor(bits1, bits2):
    """XOR operation"""
    result = []
    for b1, b2 in zip(bits1, bits2):
        result.append(b1 ^ b2)
    return result

def encrypt(plaintext, key):
    """Encrypt 64-bit plaintext"""
    # Make 16 round keys
    keys = make_keys(key)
    
    # Initial permutation
    data = shuffle(plaintext, IP)
    
    # Split
    left = data[:32]
    right = data[32:]
    
    # 16 rounds
    for i in range(16):
        old_right = right.copy()
        
        # F function
        # 1. Expand
        expanded = shuffle(right, E)
        
        # 2. XOR with key
        mixed = xor(expanded, keys[i])
        
        # 3. S-box (simplified)
        sbox_out = []
        chunk = mixed[:6]  # Just first 6 bits for demo
        row = (chunk[0] << 1) | chunk[5]
        col = (chunk[1] << 3) | (chunk[2] << 2) | (chunk[3] << 1) | chunk[4]
        value = S_BOX[row][col]
        sbox_out.append((value >> 3) & 1)
        sbox_out.append((value >> 2) & 1)
        sbox_out.append((value >> 1) & 1)
        sbox_out.append(value & 1)
        sbox_out = sbox_out * 8  # Repeat to make 32 bits
        
        # 4. P-box
        f_result = shuffle(sbox_out, P)
        
        # 5. XOR with left
        right = xor(left, f_result)
        left = old_right
    
    # Combine and final permutation
    combined = right + left
    cipher = shuffle(combined, FP)
    
    return cipher

# Test
if __name__ == "__main__":
    pt = [0,1] * 32
    k = [1,0] * 32
    ct = encrypt(pt, k)
    print(f"Encryption test: {len(ct)} bits")