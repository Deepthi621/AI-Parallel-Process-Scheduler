#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <string>
#include <cmath>
#include <cstdlib>
#include <omp.h>

using namespace std;


struct Process {
    string processId;
    int arrivalTime;

    double actualBurst;
    double predictedBurst;

    int threadId;
    double executionTime;
};


void executeProcess(const Process& p)
{
    volatile long long result = 0;

    long long iterations =
        static_cast<long long>(p.actualBurst * 1000000);

    for (long long i = 0; i < iterations; i++) {
        result += (i % 100);
    }
}


int main(int argc, char* argv[])
{
    // ==========================================
    // Number of OpenMP threads
    // ==========================================

    int numThreads = 4;

    if (argc > 1) {
        numThreads = atoi(argv[1]);
    }

    if (numThreads < 1) {
        numThreads = 1;
    }

    omp_set_num_threads(numThreads);


    // ==========================================
    // Read AI predictions
    // ==========================================

    ifstream file("../dataset/predictions.csv");

    if (!file.is_open()) {
        cerr << "Error: Could not open predictions.csv\n";
        return 1;
    }


    vector<Process> processes;

    string line;

    // Skip header
    getline(file, line);


    while (getline(file, line)) {

        stringstream ss(line);

        string value;

        Process p;

        // process_id
        getline(ss, p.processId, ',');

        // arrival_time
        getline(ss, value, ',');
        p.arrivalTime = stoi(value);

        // cpu_usage
        getline(ss, value, ',');

        // memory_usage
        getline(ss, value, ',');

        // io_operations
        getline(ss, value, ',');

        // process_type
        getline(ss, value, ',');

        // priority
        getline(ss, value, ',');

        // actual burst time
        getline(ss, value, ',');
        p.actualBurst = stod(value);

        // predicted burst time
        getline(ss, value, ',');
        p.predictedBurst = stod(value);

        p.threadId = -1;
        p.executionTime = 0.0;

        processes.push_back(p);
    }

    file.close();


    // ==========================================
    // Sort using AI predicted burst time
    // ==========================================

    sort(
        processes.begin(),
        processes.end(),
        [](const Process& a, const Process& b) {
            return a.predictedBurst < b.predictedBurst;
        }
    );


    cout << "\n==========================================\n";
    cout << " AI + OPENMP PARALLEL SCHEDULER\n";
    cout << "==========================================\n";

    cout << "Processes : "
         << processes.size() << endl;

    cout << "Threads   : "
         << numThreads << endl;


    cout << "\nScheduling order based on AI prediction:\n";

    for (const auto& p : processes) {

        cout << p.processId
             << "  Predicted: "
             << p.predictedBurst
             << "  Actual: "
             << p.actualBurst
             << endl;
    }


    // ==========================================
    // Thread statistics
    // ==========================================

    vector<double> threadBusyTime(
        numThreads,
        0.0
    );

    int nextProcess = 0;


    // ==========================================
    // Start parallel execution
    // ==========================================

    double startTime = omp_get_wtime();


    #pragma omp parallel shared(nextProcess, processes, threadBusyTime)
    {
        int threadId =
            omp_get_thread_num();


        while (true) {

            int processIndex;


            // Safely select next process
            #pragma omp critical
            {
                if (nextProcess < (int)processes.size()) {

                    processIndex = nextProcess;

                    nextProcess++;
                }
                else {

                    processIndex = -1;
                }
            }


            // No processes remaining
            if (processIndex == -1) {
                break;
            }


            double processStart =
                omp_get_wtime();


            // Execute actual workload
            executeProcess(
                processes[processIndex]
            );


            double processEnd =
                omp_get_wtime();


            double processTime =
                processEnd - processStart;


            processes[processIndex].threadId =
                threadId;

            processes[processIndex].executionTime =
                processTime;


            threadBusyTime[threadId] +=
                processTime;


            cout << "Thread "
                 << threadId
                 << " executed "
                 << processes[processIndex].processId
                 << endl;
        }
    }


    double endTime =
        omp_get_wtime();


    // ==========================================
    // Performance calculations
    // ==========================================

    double totalTime =
        endTime - startTime;


    double totalBusyTime = 0.0;


    for (int i = 0; i < numThreads; i++) {

        totalBusyTime +=
            threadBusyTime[i];
    }


    double utilization =
        (totalBusyTime /
        (totalTime * numThreads))
        * 100.0;


    // ==========================================
    // Prediction error
    // ==========================================

    double totalPredictionError = 0.0;


    for (const auto& p : processes) {

        totalPredictionError +=
            abs(
                p.actualBurst -
                p.predictedBurst
            );
    }


    double meanPredictionError =
        totalPredictionError /
        processes.size();


    // ==========================================
    // Final results
    // ==========================================

    cout << "\n==========================================\n";
    cout << " FINAL RESULTS\n";
    cout << "==========================================\n";

    cout << "Number of Processes : "
         << processes.size()
         << endl;

    cout << "Threads             : "
         << numThreads
         << endl;

    cout << "Parallel Time       : "
         << totalTime
         << " seconds"
         << endl;

    cout << "Total Busy Time     : "
         << totalBusyTime
         << " seconds"
         << endl;

    cout << "Thread Utilization  : "
         << utilization
         << "%"
         << endl;

    cout << "Mean Prediction Error : "
         << meanPredictionError
         << endl;


    cout << "\nAI + OpenMP scheduling completed!\n";


    return 0;
}