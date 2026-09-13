#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <algorithm>
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


int main()
{
    ifstream file("../dataset/test_workload.csv");

    if (!file.is_open()) {
        cerr << "Error: Could not open test_workload.csv\n";
        return 1;
    }

    vector<Process> processes;

    string line;

    getline(file, line); // Skip header

    while (getline(file, line)) {

        stringstream ss(line);
        string value;

        Process p;

        // process_id
        getline(ss, p.processId, ',');

        // arrival_time
        getline(ss, value, ',');
        p.arrivalTime = stoi(value);

        // Skip CPU usage
        getline(ss, value, ',');

        // Skip memory usage
        getline(ss, value, ',');

        // Skip I/O operations
        getline(ss, value, ',');

        // Skip process type
        getline(ss, value, ',');

        // Skip priority
        getline(ss, value, ',');

        // burst time
        getline(ss, value, ',');
        p.burstTime = stod(value);

        processes.push_back(p);
    }

    file.close();


    // FCFS = sort by arrival time
    sort(
        processes.begin(),
        processes.end(),
        [](const Process& a, const Process& b) {
            return a.arrivalTime < b.arrivalTime;
        }
    );


    double startTime = omp_get_wtime();


    // Sequential execution
    for (const auto& p : processes) {
        executeProcess(p);
    }


    double endTime = omp_get_wtime();

    double executionTime = endTime - startTime;


    cout << "\n==========================================\n";
    cout << " SEQUENTIAL FCFS\n";
    cout << "==========================================\n";

    cout << "Processes       : "
         << processes.size() << endl;

    cout << "Execution Time  : "
         << executionTime
         << " seconds" << endl;

    cout << "\nFCFS execution completed!\n";


    return 0;
}