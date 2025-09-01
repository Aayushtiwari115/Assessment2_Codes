
from pathlib import Path
from typing import Tuple

ALPHA_LOWER = "abcdefghijklmnopqrstuvwxyz"
ALPHA_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER_FIRST = set(ALPHA_LOWER[:13])   # a–m
LOWER_SECOND = set(ALPHA_LOWER[13:])  # n–z
UPPER_FIRST = set(ALPHA_UPPER[:13])   # A–M
UPPER_SECOND = set(ALPHA_UPPER[13:])  # N–Z


# ----------------------------- core helpers ----------------------------------

def _shift_char(ch: str, k: int, alphabet: str) -> str:
    """
    Cyclic shift of a single character 'ch' by k within 'alphabet' (size 26).
    Non-members are returned unchanged.
    """
    if ch not in alphabet:
        return ch
    idx = alphabet.index(ch)
    return alphabet[(idx + k) % 26]


def encrypt_with_meta(text: str, shift1: int, shift2: int) -> Tuple[str, str]:
    """
    Apply the assignment's encryption rules to 'text' and return:
      (cipher_text, metadata_string)
    Metadata encodes which rule was applied, char-by-char:

        '0' = non-letter (unchanged)
        '1' = lowercase a–m  : + (shift1 * shift2)
        '2' = lowercase n–z  : - (shift1 + shift2)
        '3' = uppercase A–M  : - shift1
        '4' = uppercase N–Z  : + (shift2 ** 2)
    """
    k1 = shift1 * shift2
    k2 = shift1 + shift2
    kU2 = shift2 ** 2

    out_chars = []
    meta_chars = []

    for ch in text:
        if ch.islower():
            if ch in LOWER_FIRST:
                out_chars.append(_shift_char(ch, k1, ALPHA_LOWER))
                meta_chars.append('1')
            elif ch in LOWER_SECOND:
                out_chars.append(_shift_char(ch, -k2, ALPHA_LOWER))
                meta_chars.append('2')
            else:
                out_chars.append(ch)
                meta_chars.append('0')
        elif ch.isupper():
            if ch in UPPER_FIRST:
                out_chars.append(_shift_char(ch, -shift1, ALPHA_UPPER))
                meta_chars.append('3')
            elif ch in UPPER_SECOND:
                out_chars.append(_shift_char(ch, kU2, ALPHA_UPPER))
                meta_chars.append('4')
            else:
                out_chars.append(ch)
                meta_chars.append('0')
        else:
            out_chars.append(ch)
            meta_chars.append('0')

    return "".join(out_chars), "".join(meta_chars)


def decrypt_with_meta(cipher: str, meta: str, shift1: int, shift2: int) -> str:
    """
    Invert the encryption using the metadata to decide which inverse to apply.
    """
    if len(cipher) != len(meta):
        raise ValueError("Metadata length does not match ciphertext length.")

    k1 = shift1 * shift2
    k2 = shift1 + shift2
    kU2 = shift2 ** 2

    out_chars = []
    for ch, m in zip(cipher, meta):
        if m == '0':       # unchanged
            out_chars.append(ch)
        elif m == '1':     # a–m used +k1 → inverse -k1
            out_chars.append(_shift_char(ch, -k1, ALPHA_LOWER))
        elif m == '2':     # n–z used -k2 → inverse +k2
            out_chars.append(_shift_char(ch, +k2, ALPHA_LOWER))
        elif m == '3':     # A–M used -shift1 → inverse +shift1
            out_chars.append(_shift_char(ch, +shift1, ALPHA_UPPER))
        elif m == '4':     # N–Z used +shift2^2 → inverse -shift2^2
            out_chars.append(_shift_char(ch, -kU2, ALPHA_UPPER))
        else:
            # Unexpected code – fail safe: leave as-is
            out_chars.append(ch)

    return "".join(out_chars)


def verify_files(a: Path, b: Path):
    """
    Byte-wise equality check. Returns (is_equal: bool, first_diff_index or None).
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
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Please enter an integer.")


# main 

def main() -> None:
    print("=== HIT137 Q1: Encrypt → Decrypt → Verify (lossless with metadata) ===")
    base = Path(__file__).parent
    raw_path = base / "raw_text.txt"
    enc_path = base / "encrypted_text.txt"
    meta_path = base / "encrypted_text.meta"
    dec_path = base / "decrypted_text.txt"

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {raw_path.resolve()}.\n"
            "Please create 'raw_text.txt' in the same folder."
        )

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


if __name__ == "__main__":
    main()