# HIT137 – Group Assignment 2 (20%)

This repository contains solutions for **three programming tasks** in Assignment 2.  
Each solution is implemented in Python and demonstrates different programming skills:  
**file handling, data analysis, recursion, and graphics programming.**

---

## Question 1 – Text Encryption and Decryption

### Objective
Create a program that encrypts and decrypts text from a file using a simple custom shifting method, then verifies the result.

### Features
- Reads text from `raw_text.txt`.
- Prompts the user for two integers: `shift1` and `shift2`.
- Encryption rules:
  - **Lowercase letters (a–m):** shift forward by `shift1 * shift2`.
  - **Lowercase letters (n–z):** shift backward by `shift1 + shift2`.
  - **Uppercase letters (A–M):** shift backward by `shift1`.
  - **Uppercase letters (N–Z):** shift forward by `shift2²`.
  - **Other characters:** unchanged.
- Writes result to `encrypted_text.txt`.
- Decrypts back to `decrypted_text.txt`.
- Compares decrypted text with the original file.

### Run
```bash
python question_1.py
Output
encrypted_text.txt
decrypted_text.txt
Question 2 – Seasonal Temperature Analysis
Objective
Analyze Australian seasonal temperature data from multiple CSV files stored in a temperatures/ folder.
Features
Processes all .csv files inside temperatures/.
Each file contains rows for STATION_NAME and columns January … December.
Performs:
Seasonal averages across all years/stations.
Largest temperature range for a station (Max – Min).
Most stable and most variable stations based on standard deviation.
Ignores missing values (NaN).
Seasons
Summer: December – February
Autumn: March – May
Winter: June – August
Spring: September – November
Run
python question_2.py
Output
average_temp.txt
largest_temp_range_station.txt
temperature_stability_stations.txt
Question 3 – Recursive Polygon Fractal
Objective
Generate a recursive fractal pattern from a regular polygon using Turtle graphics.
Features
Asks user for:
Number of polygon sides (≥ 3)
Side length (pixels)
Recursion depth
Rule:
Divide edge into 3 segments.
Replace the middle segment with two sides of an equilateral triangle pointing inward.
Repeat recursively for each new edge.
Depth 0 → regular polygon.
Depth 1+ → indentations per edge.
Higher depths → intricate fractal patterns.
Run
python question_3.py
Output
A Turtle graphics window showing the fractal.
Example screenshot: q3_output.png.
Requirements
Python 3.8+
Libraries:
pandas (for Question 2)
Standard libraries: turtle, math, glob, os, typing
Install pandas if needed:
pip install pandas
