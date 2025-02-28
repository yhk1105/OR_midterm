# Operations Research Midterm Project

This repository contains our midterm project for the Operations Research course (Spring 2024). The project addresses a complex scheduling problem for the IEDO company, focusing on optimizing job scheduling in a two-stage food processing environment. The main objectives are to minimize total tardiness and, under that constraint, to minimize the makespan.

## Team Information

- **Team Name:** Team O
- **Members:**
  - Hong-Kai Yang (B11611047)
  - Yi-Ting Chen (B11705051)
  - Chi-Wei Ho (B11702044)
  - Yu-Ting Chou (B11702080)

## Project Overview

The project is divided into several parts:

1. **Mathematical Formulation:**  
   We developed two integer programming models for the scheduling problem:
   - **Stage 1:** Minimize total tardiness.
   - **Stage 2:** Minimize the makespan while keeping the total tardiness at the minimum level obtained in Stage 1.

2. **Optimal Scheduling Using Gurobi:**  
   For instance 5 (provided as a CSV file), we formulated and solved the scheduling problem using Gurobi Optimizer. The output is a complete, business-ready schedule with job splits and machine assignments along with the corresponding objective values.

3. **Heuristic Algorithm Development:**  
   Recognizing that large-scale instances may be too time-consuming for exact methods, we designed and implemented a heuristic algorithm in Python 3.9. This algorithm is tested on multiple instances (five provided and ten hidden) and its performance is benchmarked against optimal or relaxed solutions.

4. **Algorithm Analysis and Experimentation:**  
   We documented our heuristic approach in detail, including flowcharts, pseudocode, and a Big-O analysis of its time complexity. Extensive experiments on randomly generated instances are conducted to demonstrate its efficiency and robustness.

For a complete description—including mathematical formulations, detailed algorithm explanations, experimental settings, and performance comparisons—please refer to the attached PDF report.
