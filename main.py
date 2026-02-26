import win32print
import time
import json

# Database of reset sequences for different models
# Header: 1B 28 52 08 00 00 52 45 4D 4F 54 45 31
# Exit: 1B 00 00 00
# DT Sequence: DT + Length + Header + Address + Data
RESET_DB = {
    "L3110": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L3115": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L3150": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L1110": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L1210": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L1250": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L3210": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L3250": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L3251": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L3252": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L3256": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L3260": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L5190": {"main_pad": 0x2f, "platen_pad": 0x38},
    "L5290": {"main_pad": 0x2f, "platen_pad": 0x38},
    # Canon G-Series (Expansion)
    "G1010": {"main_pad": 0x3c, "platen_pad": 0x40},
    "G2010": {"main_pad": 0x3c, "platen_pad": 0x40},
    "G3010": {"main_pad": 0x3c, "platen_pad": 0x40},
    "G4010": {"main_pad": 0x3c, "platen_pad": 0x40},
    "G1000": {"main_pad": 0x3c, "platen_pad": 0x40},
    "G2000": {"main_pad": 0x3c, "platen_pad": 0x40},
}

import hashlib
import uuid

# License Security
def get_hwid():
    return str(uuid.getnode())

def check_activation(key):
    # Simple hash-based activation for MVP
    # Key = SHA256(HWID + "SAVIOR_SECRET")
    expected = hashlib.sha256((get_hwid() + "SAVIOR_SECRET").encode()).hexdigest()[:10].upper()
    return key.upper() == expected

def run_reset(printer_name, model_key, license_key):
    if not check_activation(license_key):
        return "ERROR: Invalid Activation Key. Purchase one at: https://anurag0205as-oss.github.io/universal-printer-savior/"

    try:
        offsets = RESET_DB.get(model_key)
        if not offsets:
            return "Model not supported."

        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Global Reset", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            
            # Enter Remote
            win32print.WritePrinter(hPrinter, b'\x1b(R\x08\x00\x00REMOTE1')
            time.sleep(0.5)
            
            # Reset Main Pad
            win32print.WritePrinter(hPrinter, b'\x44\x54\x00\x12\x00\x00' + bytes([offsets["main_pad"]]) + (b'\x00' * 16))
            time.sleep(0.2)
            
            # Reset Platen Pad
            win32print.WritePrinter(hPrinter, b'\x44\x54\x00\x12\x00\x00' + bytes([offsets["platen_pad"]]) + (b'\x00' * 16))
            time.sleep(0.2)
            
            # Exit Remote
            win32print.WritePrinter(hPrinter, b'\x1b\x00\x00\x00')
            
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
            return "Reset commands sent successfully."
        finally:
            win32print.ClosePrinter(hPrinter)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("--- Universal Printer Savior (Core) ---")
    # This will be integrated with a GUI or Web Key
