# HIT137 — Group Assignment 2 (20%)

This repository contains completed solutions for all three questions in *Assignment 2*.

---

## 📦 Contents

ASSESSMENT2_CODES/
│
├── temperatures/ # Folder for Q2 CSV input files
│
├── question_1.py # Q1: Encryption/Decryption program
├── question_2.py # Q2: Temperature analysis program
├── question_3.py # Q3: Recursive polygon fractal (Turtle)
│
├── raw_text.txt # Input for Q1
├── encrypted_text.txt # Output (encrypted text)
├── decrypted_text.txt # Output (decrypted text)
│
├── average_temp.txt # Q2 output: seasonal averages
├── largest_temp_range_station.txt # Q2 output: station(s) with largest range
├── temperature_stability_stations.txt # Q2 output: most stable/variable stations
│
├── q3_output.png # Screenshot/sample output for Q3
├── github_link.txt # Public GitHub repo link (edit this)
└── README.md # Documentation (this file)
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

