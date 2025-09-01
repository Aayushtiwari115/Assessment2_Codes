#question_1_Solution12345

from pathlib import Path
from typing import Tuple

# ------------------------- Global Constants ----------------------------------

# Define alphabets and partitions for classification
ALPHA_LOWER = "abcdefghijklmnopqrstuvwxyz"
ALPHA_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Partition lowercase alphabet into two halves
LOWER_FIRST = set(ALPHA_LOWER[:13])   # a–m
LOWER_SECOND = set(ALPHA_LOWER[13:])  # n–z

# Partition uppercase alphabet into two halves
UPPER_FIRST = set(ALPHA_UPPER[:13])   # A–M
UPPER_SECOND = set(ALPHA_UPPER[13:])  # N–Z


# ----------------------------- Core Helpers ----------------------------------

def _shift_char(ch: str, k: int, alphabet: str) -> str:
    """
    Perform a cyclic shift of a single character 'ch' within a given 'alphabet'.
    The shift magnitude is k (can be positive or negative).
    Characters not in the alphabet remain unchanged.
    """
    if ch not in alphabet:
        return ch
    idx = alphabet.index(ch)  # current index
    return alphabet[(idx + k) % 26]  # apply shift with wraparound


def encrypt_with_meta(text: str, shift1: int, shift2: int) -> Tuple[str, str]:
    """
    Encrypt text using the assignment’s rules. Returns:
        (cipher_text, metadata_string)

    Rules based on character class:
        '0' = non-letter (unchanged)
        '1' = lowercase a–m  → shifted by +(shift1 * shift2)
        '2' = lowercase n–z  → shifted by -(shift1 + shift2)
        '3' = uppercase A–M  → shifted by -shift1
        '4' = uppercase N–Z  → shifted by +(shift2 ** 2)

    Metadata ensures that decryption can reverse each transformation.
    """
    k1 = shift1 * shift2
    k2 = shift1 + shift2
    kU2 = shift2 ** 2

    out_chars = []   # encrypted characters
    meta_chars = []  # metadata (tracking which rule applied)

    for ch in text:
        if ch.islower():
            if ch in LOWER_FIRST:  # lowercase a–m
                out_chars.append(_shift_char(ch, k1, ALPHA_LOWER))
                meta_chars.append('1')
            elif ch in LOWER_SECOND:  # lowercase n–z
                out_chars.append(_shift_char(ch, -k2, ALPHA_LOWER))
                meta_chars.append('2')
            else:
                out_chars.append(ch)  # non-standard char (unchanged)
                meta_chars.append('0')
        elif ch.isupper():
            if ch in UPPER_FIRST:  # uppercase A–M
                out_chars.append(_shift_char(ch, -shift1, ALPHA_UPPER))
                meta_chars.append('3')
            elif ch in UPPER_SECOND:  # uppercase N–Z
                out_chars.append(_shift_char(ch, kU2, ALPHA_UPPER))
                meta_chars.append('4')
            else:
                out_chars.append(ch)
                meta_chars.append('0')
        else:
            # Non-alphabetic characters (digits, punctuation, whitespace)
            out_chars.append(ch)
            meta_chars.append('0')

    return "".join(out_chars), "".join(meta_chars)


def decrypt_with_meta(cipher: str, meta: str, shift1: int, shift2: int) -> str:
    """
    Decrypt text using metadata to apply exact inverse operations.
    Ensures full reversibility regardless of shift parameters.
    """
    if len(cipher) != len(meta):
        raise ValueError("Metadata length does not match ciphertext length.")

    k1 = shift1 * shift2
    k2 = shift1 + shift2
    kU2 = shift2 ** 2

    out_chars = []
    for ch, m in zip(cipher, meta):
        if m == '0':       # Non-letter (unchanged)
            out_chars.append(ch)
        elif m == '1':     # inverse of +(shift1 * shift2)
            out_chars.append(_shift_char(ch, -k1, ALPHA_LOWER))
        elif m == '2':     # inverse of -(shift1 + shift2)
            out_chars.append(_shift_char(ch, +k2, ALPHA_LOWER))
        elif m == '3':     # inverse of -shift1
            out_chars.append(_shift_char(ch, +shift1, ALPHA_UPPER))
        elif m == '4':     # inverse of +(shift2 ** 2)
            out_chars.append(_shift_char(ch, -kU2, ALPHA_UPPER))
        else:
            # Unexpected metadata symbol – safeguard fallback
            out_chars.append(ch)

    return "".join(out_chars)


def verify_files(a: Path, b: Path):
    """
    Compare two files byte-by-byte.
    Returns (True, None) if identical,
    else (False, index_of_first_difference).
    """
    A = a.read_text(encoding="utf-8")
    B = b.read_text(encoding="utf-8")
    if A == B:
        return True, None
    for i, (ca, cb) in enumerate(zip(A, B)):
        if ca != cb:
            return False, i
    return False, min(len(A), len(B))


def _prompt_int(msg: str) -> int:
    """
    Prompt the user until a valid integer is entered.
    Provides robustness against invalid inputs.
    """
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Please enter an integer.")


# ----------------------------- Main Program ----------------------------------

def main() -> None:
    print("=== HIT137 Q1: Encrypt → Decrypt → Verify (lossless with metadata) ===")

    # Define file paths relative to current script
    base = Path(__file__).parent
    raw_path = base / "raw_text.txt"        # original input text
    enc_path = base / "encrypted_text.txt"  # encrypted text output
    meta_path = base / "encrypted_text.meta" # metadata output
    dec_path = base / "decrypted_text.txt"  # decrypted text output

    # Ensure raw input file exists before proceeding
    if not raw_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {raw_path.resolve()}.\n"
            "Please create 'raw_text.txt' in the same folder."
        )

    # User input: shift parameters
    shift1 = _prompt_int("Enter shift1 (integer): ")
    shift2 = _prompt_int("Enter shift2 (integer): ")

    # 1) Encrypt raw → encrypted + metadata
    raw = raw_path.read_text(encoding="utf-8")
    cipher, meta = encrypt_with_meta(raw, shift1, shift2)
    enc_path.write_text(cipher, encoding="utf-8")
    meta_path.write_text(meta, encoding="utf-8")
    print(f"[OK] Encrypted  → {enc_path.name}")
    print(f"[OK] Metadata   → {meta_path.name}")

    # 2) Decrypt encrypted using metadata → decrypted
    plain = decrypt_with_meta(cipher, meta, shift1, shift2)
    dec_path.write_text(plain, encoding="utf-8")
    print(f"[OK] Decrypted  → {dec_path.name}")

    # 3) Verify original vs decrypted
    same, idx = verify_files(raw_path, dec_path)
    if same:
        print("[SUCCESS] Decryption verified: decrypted_text.txt matches raw_text.txt")
    else:
        print("[WARNING] Files differ! First difference at index:", idx)


# Entry point
if __name__ == "__main__":
    main()
