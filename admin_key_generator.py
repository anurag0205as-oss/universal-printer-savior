import hashlib

def generate_key(hwid):
    # This matches the logic in the main resetter tool
    key = hashlib.sha256((hwid + "SAVIOR_SECRET").encode()).hexdigest()[:10].upper()
    return key

if __name__ == "__main__":
    print("--- 💰 Universal Printer Savior: Admin Key Generator ---")
    customer_hwid = input("\nEnter Customer Hardware ID: ").strip()
    if customer_hwid:
        activation_key = generate_key(customer_hwid)
        print(f"\nSUCCESS! Activation Key: {activation_key}")
        print("Provide this key to the customer after payment.")
    else:
        print("Invalid HWID.")
