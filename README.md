AI-Enhanced Parallel Process Scheduler

An AI-powered process scheduling simulator that combines OpenMP parallel execution with a Random Forest model for CPU burst-time prediction.

1. Objectives
Implement FCFS and SJF scheduling.
Implement parallel execution using OpenMP.
Predict CPU burst time using Machine Learning.
Combine AI predictions with OpenMP scheduling.
Compare execution time, speedup, efficiency, and thread utilization.
Provide an interactive web dashboard for visualization.

3. Technologies Used
C++ – Scheduling algorithms
OpenMP – Parallel execution
Python – AI model
Scikit-learn – Random Forest Regressor
Flask – AI prediction API
HTML, CSS, JavaScript – Web dashboard
Matplotlib – Performance graphs
CSV – Dataset and results
MSYS2 UCRT64 + GCC – C++ compilation

4. Project Structure
AI-Parallel-Process-Scheduler/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── fcfs.cpp
│   ├── sjf.cpp
│   ├── parallel_scheduler.cpp
│   ├── ai_scheduler.cpp
│   └── app.py
│
├── ai_model/
│   ├── train_model.py
│   ├── predict_burst.py
│   ├── generate_predictions.py
│   ├── generate_graphs.py
│   └── model.pkl
│
├── dataset/
├── results/
└── README.md
5. Setup
Install GCC/OpenMP

Install MSYS2 UCRT64 and GCC:

pacman -S mingw-w64-ucrt-x86_64-gcc

Verify:

g++ --version
Setup Python

Create and activate the virtual environment:

python -m pip install virtualenv
python -m virtualenv .venv
.venv\Scripts\Activate.ps1

Install required packages:

python -m pip install pandas numpy scikit-learn joblib matplotlib flask flask-cors

5. Train AI Model
cd ai_model
python train_model.py

This creates:

model.pkl

Generate predictions:

python generate_predictions.py

6. Compile OpenMP Programs

From the backend folder:

g++ fcfs.cpp -o fcfs.exe -fopenmp
g++ sjf.cpp -o sjf.exe -fopenmp
g++ parallel_scheduler.cpp -o parallel_scheduler.exe -fopenmp
g++ ai_scheduler.cpp -o ai_scheduler.exe -fopenmp

Run OpenMP scheduler:

./parallel_scheduler.exe 1
./parallel_scheduler.exe 2
./parallel_scheduler.exe 4
./parallel_scheduler.exe 8
./parallel_scheduler.exe 12

Run AI + OpenMP:

./ai_scheduler.exe 4
7. Generate Graphs
cd ai_model
python generate_graphs.py

Graphs are saved in:

results/

8. Start Flask API

From backend:

source ../.venv/Scripts/activate
python app.py

The API runs at:

http://127.0.0.1:5000

9. Run Dashboard

Open:

frontend/index.html

using VS Code Live Server/Live Preview.

Keep the Flask API running while using the AI predictor and process simulator.

10. Main Features
FCFS scheduling
SJF scheduling
OpenMP parallel SJF
AI + OpenMP scheduling
Random Forest burst-time prediction
Multiple thread-count testing
Speedup and efficiency calculation
Thread utilization analysis
Performance graphs
Interactive process simulator
AI-based scheduling order
Parallel execution timeline
11. Conclusion

The project demonstrates the integration of Artificial Intelligence and Parallel Computing. The AI model predicts process burst time, while OpenMP enables parallel execution across multiple worker threads. The dashboard presents scheduling results and performance metrics in an interactive form.
