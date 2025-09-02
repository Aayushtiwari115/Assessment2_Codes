
# HIT137 – Group Assignment 2 (20%)

This repository contains solutions for three programming tasks (Question 1, Question 2, Question 3) implemented in Python. Each task is implemented as a standalone script and demonstrates different programming skills: file handling & custom encryption, data analysis with CSV files, and recursive graphics using Turtle.

## Table of Contents

- Project overview
- Repository layout
- Requirements
- How to run
  - Question 1 — Text Encryption / Decryption
  - Question 2 — Seasonal Temperature Analysis
  - Question 3 — Recursive Polygon Fractal

- Outputs
- Notes
- Contributing
- Contact

## Project overview

- Question 1: Read a text file, apply a custom shifting encryption (with metadata), decrypt using the metadata, and verify the result is identical to the original content.
- Question 2: Load multiple CSV files of station temperature data, compute seasonal averages, find the station with the largest temperature range, and identify the most stable and most variable stations.
- Question 3: Draw a recursive polygon-based fractal using Python's turtle graphics. The program asks for polygon parameters (sides, side length, recursion depth).

## Repository layout (key files)

- question_1.py         — Implements encrypt / decrypt / verify workflow.
- question_2.py         — Loads temperature CSVs and runs analysis.
- question_3.py         — Turtle graphics fractal generator.
- raw_text.txt          — Example input used by question_1.py.
- encrypted_text.txt    — Example encrypted output (generated).
- encrypted_text.meta   — Metadata used for decryption (generated).
- decrypted_text.txt    — Example decrypted output (generated).
- README.md             — Original high-level README for the assignment.
- read.md               — This file (project-specific README).
- temperatures/         — (expected) folder containing CSV files for Question 2 (if present).
- q3_output.png         — (example) screenshot of Question 3 output (if present).

Adjust the list above if you add or move files.

## Requirements

- Python 3.8+ (3.8, 3.9, 3.10, etc.)
- pandas (used by Question 2)
- Standard library modules used: turtle, math, glob, os, typing, pathlib

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install pandas
```

## How to run

General: run each question script independently from the repository root (or the folder containing the scripts). Example:

```bash
python question_1.py
python question_2.py
python question_3.py
```

Windows note: use `python` or the explicit path to your Python executable (for virtualenvs: `venv\Scripts\activate` then `python`).

### Question 1 — Text Encryption and Decryption

Objective: Encrypt text in `raw_text.txt` using a custom shifting scheme, save encrypted text and metadata, decrypt using the metadata, then verify the decrypted output matches the original.

Files:
- Input: raw_text.txt (must exist in the same folder as question_1.py)
- Outputs (created by the script):
  - encrypted_text.txt
  - encrypted_text.meta
  - decrypted_text.txt

Run:
```bash
python question_1.py
```

Behavior & user prompts:
- The script prompts for two integers: `shift1` and `shift2`.
- Encryption rules (implemented in the script):
  - Lowercase a–m: shift forward by shift1 * shift2
  - Lowercase n–z: shift backward by shift1 + shift2
  - Uppercase A–M: shift backward by shift1
  - Uppercase N–Z: shift forward by shift2²
  - Other characters remain unchanged
- After encrypting and decrypting, the script compares the original and decrypted files and prints a success/warning message.

Example:
- Ensure `raw_text.txt` contains the text to encrypt, then run `python question_1.py` and follow the prompts.

### Question 2 — Seasonal Temperature Analysis

Objective: Read multiple CSV files from a folder (expected folder name: `temperatures/`), compute seasonal averages, identify the station with the largest temperature range, and find the most/least stable stations.

Files:
- Input: CSV files in `temperatures/` (each CSV should contain a station name and columns for months January…December)
- Outputs (created by the script):
  - average_temp.txt
  - largest_temp_range_station.txt
  - temperature_stability_stations.txt

Run:
```bash
python question_2.py
```

Notes about input CSVs:
- The script expects consistent columns (month columns or a format the script can parse); missing values (NaN) are ignored in calculations.
- Seasons used by the script:
  - Summer: December, January, February
  - Autumn: March, April, May
  - Winter: June, July, August
  - Spring: September, October, November

### Question 3 — Recursive Polygon Fractal (Turtle)

Objective: Generate a recursive fractal pattern using a regular polygon and Turtle graphics.

Run:
```bash
python question_3.py
```

Behavior & prompts:
- The script asks the user for:
  - Number of polygon sides (integer ≥ 3)
  - Side length (pixels)
  - Recursion depth (non-negative integer)
- The program draws the fractal in a Turtle window (interactive). You may optionally save a screenshot with your system tools; an example output file may be present (q3_output.png).

## Outputs (summary)

- encrypted_text.txt, encrypted_text.meta, decrypted_text.txt (Question 1)
  
  <img width="1130" height="101" alt="Screenshot 2025-09-02 at 2 40 41 pm" src="https://github.com/user-attachments/assets/aa5e00ea-f0fb-4d42-aa45-9c475a9494d7" />
  
- average_temp.txt, largest_temp_range_station.txt, temperature_stability_stations.txt (Question 2)
  <img width="1130" height="31" alt="Screenshot 2025-09-02 at 2 41 31 pm" src="https://github.com/user-attachments/assets/92fcf5c2-bf98-4138-b395-f01fe5003027" />
<img width="1141" height="150" alt="Screenshot 2025-09-02 at 2 42 31 pm" src="https://github.com/user-attachments/assets/60995221-cf3e-4508-ad67-0cafc8dc24e7" />
<img width="1141" height="150" alt="Screenshot 2025-09-02 at 2 42 52 pm" src="https://github.com/user-attachments/assets/6bdc0b10-1dc5-4463-8c24-1893456c0ea2" />
<img width="1141" height="150" alt="Screenshot 2025-09-02 at 2 43 05 pm" src="https://github.com/user-attachments/assets/9dfa9789-2c61-4def-a9fc-47ef53424beb" />

- A live Turtle window and optional saved screenshot (Question 3)
<img width="1141" height="102" alt="Screenshot 2025-09-02 at 2 41 49 pm" src="https://github.com/user-attachments/assets/a1ffd992-cadf-4ce3-a0f3-9ff7d6bd2257" />
`
<img width="395" height="349" alt="Screenshot 2025-09-02 at 2 29 34 pm" src="https://github.com/user-attachments/assets/643290dc-6c62-431e-8ace-91ba2a5a5abf" />


## Notes and troubleshooting

- Question 1 will raise an error if `raw_text.txt` is not present. Create that file in the same directory before running.
- Question 2 requires pandas. If you encounter import errors, install pandas with `pip install pandas`.
- Question 3 opens an interactive Turtle window — this is not suitable for headless servers without an X display.
- If CSV formats vary, inspect `question_2.py` to adapt the input parsing or normalize your CSVs to match the expected format.

## Contributing

- If you improve code or documentation, please open a pull request with a clear description of changes.
- Add unit tests for computational functions where appropriate and update this README to reflect changes in usage.


## Contact

Repository owner: @Aayushtiwari115

