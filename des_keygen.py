# DES Key Generation
from des_tables import PC1, PC2, SHIFT

def make_keys(main_key):
    """Make 16 round keys from main key"""
    # Apply PC1 (64 bits -> 56 bits)
    key56 = []
    for pos in PC1:
        key56.append(main_key[pos-1])
    
    # Split into halves
    left = key56[:28]
    right = key56[28:]
    
    all_keys = []
    
    # Make 16 keys
    for i in range(16):
        # Shift both halves
        shift = SHIFT[i]
        left = left[shift:] + left[:shift]
        right = right[shift:] + right[:shift]
        
        # Combine and apply PC2 (56 bits -> 48 bits)
        combined = left + right
        round_key = []
        for pos in PC2:
            round_key.append(combined[pos-1])
        
        all_keys.append(round_key)
    
    return all_keys

# Test
if __name__ == "__main__":
    test_key = [0,1] * 32  # 64 test bits
    keys = make_keys(test_key)
    print(f"Made {len(keys)} keys")
    print(f"First key: {keys[0][:8]}")