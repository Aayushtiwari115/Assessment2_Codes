# HIT137 — Group Assignment 2 (20%)

This repository contains completed solutions for all three questions in *Assignment 2*.

> **Important:** Keep your GitHub repository **public** and add all group members before you begin.  
> Include your repo URL in `github_link.txt`, zip the programming files and outputs, and upload the zip to Learnline per instructions.

---

## 📦 Contents

- `question_1_Solution.py` — Text encryption/decryption with verification.
- `question_2_Solution.py` — Seasonal temperature analysis over multiple CSVs.
- `question_3_Solution.py` — Recursive polygon fractal using Turtle graphics.
- `temperatures/` — Put all CSVs for Q2 here (one file per year).
- `raw_text.txt` — Input for Q1 (replace with the provided file from assignment zip).
- `github_link.txt` — **Edit this** to contain your public GitHub repository URL.
- Outputs created at runtime:
  - `encrypted_text.txt`, `decrypted_text.txt` (Q1)
  - `average_temp.txt`, `largest_temp_range_station.txt`, `temperature_stability_stations.txt` (Q2)

---

## ✅ Question 1 — Encryption / Decryption / Verification

### Run
```bash
python question_1_Solution.py
```
You will be prompted for two integers: `shift1` and `shift2`.  
The script reads `raw_text.txt`, writes `encrypted_text.txt`, decrypts to `decrypted_text.txt`, and prints whether the decrypted text matches the original.

### Rules Recap
- **Lowercase (a–z):**
  - a–m → forward by `shift1 * shift2`
  - n–z → backward by `shift1 + shift2`
- **Uppercase (A–Z):**
  - A–M → backward by `shift1`
  - N–Z → forward by `shift2 ** 2`
- Non-letters unchanged.

---

## 🌡️ Question 2 — Seasonal Temperature Analysis

Process **all** `*.csv` files inside `temperatures/` (each one year, each row = station with columns `STATION_NAME`, `January` … `December`).

### Outputs
- `average_temp.txt` — mean temperature per season across **all stations and years**.
- `largest_temp_range_station.txt` — station(s) with max (max−min) range.
- `temperature_stability_stations.txt` — most stable / most variable station(s) by std dev.

### Run
```bash
python question_2_Solution.py
```

> Seasons: Summer(Dec–Feb), Autumn(Mar–May), Winter(Jun–Aug), Spring(Sep–Nov).  
> Missing values are ignored automatically.

---

## 🧩 Question 3 — Recursive Polygon Fractal

Prompts for polygon sides, side length, and recursion depth, then draws the Koch-like indentation pattern on each edge.

### Run
```bash
python question_3_Solution.py
```
A Turtle window opens; close it to exit. Depth > 6 can be slow.

---

## 🔧 Environment & Setup

- Python 3.8+
- Dependencies:
  - `pandas` (Q2)
  - Standard library: `turtle`, `math`, `glob`, `os`, `typing`

Install pandas if needed:
```bash
pip install pandas
```

---

## 🔗 GitHub & Submission

1. Create a **public** GitHub repository.
2. Add all group members with Write access.
3. Commit/push all files from this folder.
4. Put your repo URL in `github_link.txt` (one line).
5. Zip the folder contents (including outputs) and upload to Learnline.

Good luck! ✨
