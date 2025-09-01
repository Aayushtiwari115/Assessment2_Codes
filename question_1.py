# question_1_Solution12345
# ---------------------------------------------------------------------
# Lossless Text Encryption with Per-Character Metadata
# ---------------------------------------------------------------------
# This program implements a reversible character-shift cipher driven by two
# user-provided integer parameters (shift1, shift2). Each character is
# transformed according to its alphabetical partition (lowercase a–m,
# lowercase n–z, uppercase A–M, uppercase N–Z), or left unchanged if
# non-alphabetic. For each transformed character, a metadata symbol
# (0–4) is emitted to enable exact decryption.
#
# Pipeline:
#   1) Read 'raw_text.txt'
#   2) Encrypt to 'encrypted_text.txt' and emit metadata 'encrypted_text.meta'
#   3) Decrypt using ciphertext + metadata → 'decrypted_text.txt'
#   4) Verify decrypted equals original (byte-for-byte)
#
# Design goals:
#   - Full reversibility via metadata (lossless round-trip).
#   - Explicit, partition-based rules to demonstrate conditional ciphers.
#   - Separation of concerns (I/O, transform, verification).
#
# Dependencies: Python 3.8+, standard library only.
# ---------------------------------------------------------------------

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Set, Tuple

# ------------------------- Global Constants ----------------------------------

# Define alphabets and partitions for classification
ALPHA_LOWER: str = "abcdefghijklmnopqrstuvwxyz"
ALPHA_UPPER: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Partition lowercase alphabet into two halves
LOWER_FIRST: Set[str] = set(ALPHA_LOWER[:13])   # a–m
LOWER_SECOND: Set[str] = set(ALPHA_LOWER[13:])  # n–z

# Partition uppercase alphabet into two halves
UPPER_FIRST: Set[str] = set(ALPHA_UPPER[:13])   # A–M
UPPER_SECOND: Set[str] = set(ALPHA_UPPER[13:])  # N–Z


# ----------------------------- Core Helpers ----------------------------------

def _shift_char(ch: str, k: int, alphabet: str) -> str:
    """
    Cyclically shift a single character within the given alphabet.

    If 'ch' is present in 'alphabet', its index is advanced by 'k' positions
    (modulo the alphabet length). Characters not present in 'alphabet' are
    returned unchanged.

    Args:
        ch: A single character to transform.
        k:  The integer shift magnitude (positive or negative).
        alphabet: The alphabet string within which the shift occurs.

    Returns:
        The shifted character if 'ch' ∈ alphabet; otherwise the original 'ch'.
    """
    if ch not in alphabet:
        return ch
    idx = alphabet.index(ch)
    return alphabet[(idx + k) % 26]


def encrypt_with_meta(text: str, shift1: int, shift2: int) -> Tuple[str, str]:
    """
    Encrypt 'text' according to the assignment’s partitioned rules and emit metadata.

    Partition-based rules (metadata in quotes):
        '0' = non-letter (unchanged)
        '1' = lowercase a–m  → shifted by +(shift1 * shift2)
        '2' = lowercase n–z  → shifted by -(shift1 + shift2)
        '3' = uppercase A–M  → shifted by -shift1
        '4' = uppercase N–Z  → shifted by +(shift2 ** 2)

    The returned metadata string records, per character, which rule was applied.
    This enables exact inversion during decryption irrespective of shift values.

    Args:
        text:   The plaintext to encrypt.
        shift1: First integer parameter.
        shift2: Second integer parameter.

    Returns:
        A tuple (cipher_text, metadata_string).
    """
    k1 = shift1 * shift2
    k2 = shift1 + shift2
    kU2 = shift2 ** 2

    out_chars: List[str] = []
    meta_chars: List[str] = []

    for ch in text:
        if ch.islower():
            if ch in LOWER_FIRST:  # lowercase a–m
                out_chars.append(_shift_char(ch, k1, ALPHA_LOWER))
                meta_chars.append('1')
            elif ch in LOWER_SECOND:  # lowercase n–z
                out_chars.append(_shift_char(ch, -k2, ALPHA_LOWER))
                meta_chars.append('2')
            else:
                out_chars.append(ch)  # non-standard lowercase (defensive)
                meta_chars.append('0')
        elif ch.isupper():
            if ch in UPPER_FIRST:  # uppercase A–M
                out_chars.append(_shift_char(ch, -shift1, ALPHA_UPPER))
                meta_chars.append('3')
            elif ch in UPPER_SECOND:  # uppercase N–Z
                out_chars.append(_shift_char(ch, kU2, ALPHA_UPPER))
                meta_chars.append('4')
            else:
                out_chars.append(ch)  # non-standard uppercase (defensive)
                meta_chars.append('0')
        else:
            # Non-alphabetic characters (digits, punctuation, whitespace)
            out_chars.append(ch)
            meta_chars.append('0')

    return "".join(out_chars), "".join(meta_chars)


def decrypt_with_meta(cipher: str, meta: str, shift1: int, shift2: int) -> str:
    """
    Decrypt 'cipher' using per-character 'meta' to apply exact inverse operations.

    The function requires metadata length to equal the ciphertext length. Each
    metadata symbol ('0'–'4') indicates the inverse shift to apply for the
    corresponding character position.

    Args:
        cipher: The encrypted text (ciphertext).
        meta:   The metadata string produced during encryption.
        shift1: First integer parameter used during encryption.
        shift2: Second integer parameter used during encryption.

    Returns:
        The decrypted plaintext string.

    Raises:
        ValueError: If lengths of 'cipher' and 'meta' differ.
    """
    if len(cipher) != len(meta):
        raise ValueError("Metadata length does not match ciphertext length.")

    k1 = shift1 * shift2
    k2 = shift1 + shift2
    kU2 = shift2 ** 2

    out_chars: List[str] = []
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
            # Unexpected metadata symbol – conservative fallback
            out_chars.append(ch)

    return "".join(out_chars)


def verify_files(a: Path, b: Path) -> Tuple[bool, int | None]:
    """
    Compare two text files byte-by-byte for equality.

    Args:
        a: Path to the first file.
        b: Path to the second file.

    Returns:
        (True, None) if files are identical; otherwise
        (False, index_of_first_difference).

    Notes:
        Files are read as UTF-8 text; this is acceptable for the assignment’s scope.
    """
    A = a.read_text(encoding="utf-8")
    B = b.read_text(encoding="utf-8")
    if A == B:
        return True, None
    for i, (ca, cb) in enumerate(zip(A, B)):
        if ca != cb:
            return False, i
    # Divergence occurs at the end if all paired chars matched but lengths differ.
    return False, min(len(A), len(B))


def _prompt_int(msg: str) -> int:
    """
    Prompt the user until a valid integer is entered.

    Args:
        msg: The message displayed to the user.

    Returns:
        A validated integer provided by the user.
    """
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Please enter an integer.")


# ----------------------------- Main Program ----------------------------------

def main() -> None:
    """
    Orchestrate the end-to-end workflow:
        - Validate source availability
        - Collect shift parameters
        - Encrypt with metadata and persist outputs
        - Decrypt using metadata and persist output
        - Verify original vs decrypted, reporting byte-level parity
    """
    print("=== HIT137 Q1: Encrypt → Decrypt → Verify (lossless with metadata) ===")

    # Define file paths relative to current script
    base = Path(__file__).parent
    raw_path = base / "raw_text.txt"         # original input text
    enc_path = base / "encrypted_text.txt"   # encrypted text output
    meta_path = base / "encrypted_text.meta" # metadata output
    dec_path = base / "decrypted_text.txt"   # decrypted text output

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
