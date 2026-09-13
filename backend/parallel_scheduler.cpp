#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <omp.h>

using namespace std;

struct Process {
    string processId;
    int arrivalTime;
    double burstTime;
};


void executeProcess(const Process& p)
{
    volatile long long result = 0;

    long long iterations =
        static_cast<long long>(p.burstTime * 1000000);

    for (long long i = 0; i < iterations; i++) {
        result += (i % 100);
    }
}


int main(int argc, char* argv[])
{
    int numThreads = 4;

    if (argc > 1) {
        numThreads = atoi(argv[1]);
    }

    if (numThreads < 1) {
        numThreads = 1;
    }

    omp_set_num_threads(numThreads);


    // ==========================================
    // Read test workload
    // ==========================================

    ifstream file("../dataset/test_workload.csv");

    if (!file.is_open()) {
        cerr << "Error: Could not open test_workload.csv\n";
        return 1;
    }

    vector<Process> processes;

    string line;

    getline(file, line);

    while (getline(file, line)) {

        stringstream ss(line);
        string value;

        Process p;

        getline(ss, p.processId, ',');

        getline(ss, value, ',');
        p.arrivalTime = stoi(value);

        getline(ss, value, ',');
        getline(ss, value, ',');
        getline(ss, value, ',');
        getline(ss, value, ',');
        getline(ss, value, ',');

        getline(ss, value, ',');
        p.burstTime = stod(value);

        processes.push_back(p);
    }

    file.close();


    // ==========================================
    // SJF ordering
    // ==========================================

    sort(
        processes.begin(),
        processes.end(),
        [](const Process& a, const Process& b) {

            if (a.burstTime == b.burstTime) {
                return a.arrivalTime < b.arrivalTime;
            }

            return a.burstTime < b.burstTime;
        }
    );


    // ==========================================
    // Thread statistics
    // ==========================================

    int nextProcess = 0;

    vector<double> threadBusyTime(
        numThreads,
        0.0
    );


    // ==========================================
    // Parallel execution
    // ==========================================

    double startTime = omp_get_wtime();


    #pragma omp parallel shared(nextProcess, processes, threadBusyTime)
    {
        int threadId = omp_get_thread_num();

        while (true) {

            int processIndex = -1;

            #pragma omp critical
            {
                if (nextProcess < (int)processes.size()) {
                    processIndex = nextProcess;
                    nextProcess++;
                }
            }

            if (processIndex == -1) {
                break;
            }


            double processStart =
                omp_get_wtime();

            executeProcess(
                processes[processIndex]
            );

            double processEnd =
                omp_get_wtime();


            threadBusyTime[threadId] +=
                processEnd - processStart;
        }
    }


    double endTime = omp_get_wtime();

    double executionTime =
        endTime - startTime;


    // ==========================================
    // Calculate utilization
    // ==========================================

    double totalBusyTime = 0.0;

    for (int i = 0; i < numThreads; i++) {
        totalBusyTime += threadBusyTime[i];
    }


    double utilization =
        (totalBusyTime /
        (executionTime * numThreads))
        * 100.0;


    // ==========================================
    // Results
    // ==========================================

    cout << "\n==========================================\n";
    cout << " OPENMP PARALLEL SJF\n";
    cout << "==========================================\n";

    cout << "Processes          : "
         << processes.size()
         << endl;

    cout << "Threads            : "
         << numThreads
         << endl;

    cout << "Execution Time     : "
         << executionTime
         << " seconds"
         << endl;

    cout << "Total Busy Time    : "
         << totalBusyTime
         << " seconds"
         << endl;

    cout << "Thread Utilization : "
         << utilization
         << "%"
         << endl;

    cout << "\nOpenMP SJF execution completed!\n";


    return 0;
}