// ==========================================
// CSV Loader
// ==========================================

async function loadCSV(filePath) {

    const response = await fetch(filePath);

    const text = await response.text();

    const lines = text.trim().split("\n");

    const headers = lines[0].split(",");

    const data = [];

    for (let i = 1; i < lines.length; i++) {

        const values = lines[i].split(",");

        const row = {};

        headers.forEach((header, index) => {

            row[header.trim()] =
                values[index]?.trim() || "";

        });

        data.push(row);
    }

    return data;
}


// ==========================================
// Load Performance Data
// ==========================================

async function loadPerformanceData() {

    const results =
        await loadCSV(
            "../results/performance_results.csv"
        );


    // ======================================
    // AI + OpenMP Results
    // ======================================

    const aiResults =
        results.filter(
            row =>
                row.scheduler === "AI + OpenMP"
        );


    // ======================================
    // Find Best Speedup
    // ======================================

    let bestSpeedup = 0;


    // ======================================
    // Find Best Execution Time
    // ======================================

    let bestExecutionTime = Infinity;

    let bestTimeScheduler = "";

    let bestTimeThreads = "";


    aiResults.forEach(row => {

        const speedup =
            parseFloat(row.speedup);

        const time =
            parseFloat(row.execution_time);


        if (speedup > bestSpeedup) {

            bestSpeedup = speedup;

        }


        if (time < bestExecutionTime) {

            bestExecutionTime = time;

            bestTimeScheduler =
                row.scheduler;

            bestTimeThreads =
                row.threads;

        }

    });


    // ======================================
    // Update Dashboard Cards
    // ======================================

    document.getElementById(
        "best-speedup"
    ).textContent =
        bestSpeedup.toFixed(2) + "×";


    document.getElementById(
        "best-time"
    ).textContent =
        bestExecutionTime.toFixed(3) + " s";


    document.getElementById(
        "best-time-label"
    ).textContent =
        bestTimeScheduler +
        " · " +
        bestTimeThreads +
        " threads";


    // ======================================
    // Scheduler Comparison Table
    // ======================================

    const tableBody =
        document.getElementById(
            "comparison-body"
        );


    const threadSelect =
        document.getElementById(
            "thread-select"
        );


    function updateComparisonTable() {

        const selectedThreads =
            threadSelect.value;


        tableBody.innerHTML = "";


        const filteredResults =
            results.filter(row => {

                return (
                    row.threads === selectedThreads
                    &&
                    (
                        row.scheduler === "OpenMP SJF"
                        ||
                        row.scheduler === "AI + OpenMP"
                    )
                );

            });


        filteredResults.forEach(row => {

            const tr =
                document.createElement(
                    "tr"
                );


            tr.innerHTML = `

                <td>
                    ${row.scheduler}
                </td>

                <td>
                    ${row.threads}
                </td>

                <td>
                    ${row.execution_time} s
                </td>

                <td>
                    ${row.speedup}×
                </td>

                <td>
                    ${row.efficiency}%
                </td>

                <td>
                    ${row.utilization || "N/A"}%
                </td>

            `;


            tableBody.appendChild(tr);

        });

    }


    // ======================================
    // Update Table When Threads Change
    // ======================================

    threadSelect.addEventListener(
        "change",
        updateComparisonTable
    );


    // ======================================
    // Initial Table
    // ======================================

    updateComparisonTable();

}



// ==========================================
// Load AI Metrics
// ==========================================

async function loadAIMetrics() {

    const metrics =
        await loadCSV(
            "../results/ai_metrics.csv"
        );


    metrics.forEach(row => {

        const metric =
            row.metric;

        const value =
            row.value;


        // Training processes

        if (
            metric ===
            "training_processes"
        ) {

            document.getElementById(
                "training-processes"
            ).textContent = value;

        }


        // Validation R2

        if (
            metric ===
            "validation_r2"
        ) {

            document.getElementById(
                "validation-r2"
            ).textContent = value;

        }


        // Validation MAE

        if (
            metric ===
            "validation_mae"
        ) {

            document.getElementById(
                "validation-mae"
            ).textContent = value;

        }


        // Test processes

        if (
            metric ===
            "unseen_test_processes"
        ) {

            document.getElementById(
                "test-processes"
            ).textContent = value;

        }


        // Test prediction error

        if (
            metric ===
            "unseen_test_mean_error"
        ) {

            document.getElementById(
                "test-error"
            ).textContent = value;


            document.getElementById(
                "ai-error"
            ).textContent = value;

        }

    });

}



// ==========================================
// Start Dashboard
// ==========================================

async function initializeDashboard() {

    try {

        await loadPerformanceData();

        await loadAIMetrics();


        console.log(
            "Dashboard data loaded successfully."
        );

    }

    catch (error) {

        console.error(
            "Error loading dashboard data:",
            error
        );

    }

}


initializeDashboard();





// ==========================================
// Process Scheduling Simulator
// ==========================================

const processes = [];


const addProcessButton =
    document.getElementById(
        "add-process-button"
    );


const processTableBody =
    document.getElementById(
        "process-table-body"
    );


const schedulingOrder =
    document.getElementById(
        "scheduling-order"
    );


const fcfsOrder =
    document.getElementById(
        "fcfs-order"
    );


const sjfOrder =
    document.getElementById(
        "sjf-order"
    );


const aiOpenMPOrder =
    document.getElementById(
        "ai-openmp-order"
    );


const executionTimeline =
    document.getElementById(
        "execution-timeline"
    );



// ==========================================
// Generate Parallel Execution Timeline
// ==========================================

function generateExecutionTimeline(
    sortedProcesses
) {

    executionTimeline.innerHTML = "";


    if (
        sortedProcesses.length === 0
    ) {

        executionTimeline.innerHTML = `

            <div class="timeline-empty">

                Add processes to display
                the parallel execution timeline.

            </div>

        `;

        return;

    }


    // Use up to 4 worker threads
    // for the frontend visualization.

    const numberOfThreads =
        Math.min(
            4,
            sortedProcesses.length
        );


    // ======================================
    // Create Thread Rows
    // ======================================

    for (
        let thread = 0;
        thread < numberOfThreads;
        thread++
    ) {

        const row =
            document.createElement(
                "div"
            );


        row.className =
            "timeline-row";


        const label =
            document.createElement(
                "div"
            );


        label.className =
            "timeline-label";


        label.textContent =
            "Thread " +
            thread;


        const track =
            document.createElement(
                "div"
            );


        track.className =
            "timeline-track";


        // ==================================
        // Assign Processes to Threads
        // ==================================

        sortedProcesses.forEach(
            (process, index) => {

                if (
                    index %
                    numberOfThreads
                    ===
                    thread
                ) {

                    const processBlock =
                        document.createElement(
                            "div"
                        );


                    processBlock.className =
                        "timeline-process";


                    processBlock.textContent =
                        process.processId;


                    // ==================================
                    // Set Block Width Based on Burst Time
                    // ==================================

                    const burst =
                        parseFloat(
                            process.predictedBurst
                        );


                    const blockWidth =
                        Math.max(
                            90,
                            burst * 12
                        );


                    processBlock.style.width =
                        blockWidth + "px";


                    processBlock.title =
                        "Process: " +
                        process.processId +
                        "\nPredicted Burst: " +
                        burst +
                        " time units";


                    track.appendChild(
                        processBlock
                    );

                }

            }
        );


        row.appendChild(
            label
        );


        row.appendChild(
            track
        );


        executionTimeline.appendChild(
            row
        );

    }

}



// ==========================================
// Add Process
// ==========================================

addProcessButton.addEventListener(
    "click",
    async function () {


        // ==================================
        // Read Process Information
        // ==================================

        const processId =
            document.getElementById(
                "process-id-input"
            ).value.trim();


        const cpu =
            document.getElementById(
                "sim-cpu-input"
            ).value;


        const memory =
            document.getElementById(
                "sim-memory-input"
            ).value;


        const io =
            document.getElementById(
                "sim-io-input"
            ).value;


        const processType =
            document.getElementById(
                "sim-type-input"
            ).value;


        const priority =
            document.getElementById(
                "sim-priority-input"
            ).value;


        // ==================================
        // Validate Process ID
        // ==================================

        if (!processId) {

            alert(
                "Please enter a Process ID."
            );

            return;

        }


        try {


            // ==================================
            // Ask AI for Burst Prediction
            // ==================================

            const response =
                await fetch(
                    "http://127.0.0.1:5000/predict",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            cpu_usage:
                                cpu,

                            memory_usage:
                                memory,

                            io_operations:
                                io,

                            process_type:
                                processType

                        })

                    }
                );


            const data =
                await response.json();


            // ==================================
            // Check Prediction Error
            // ==================================

            if (data.error) {

                alert(
                    data.error
                );

                return;

            }


            // ==================================
            // Get Predicted Burst Time
            // ==================================

            const predictedBurst =
                data.predicted_burst_time;


            // ==================================
            // Store Process
            // ==================================

            processes.push({

                processId:
                    processId,

                cpu:
                    cpu,

                memory:
                    memory,

                io:
                    io,

                processType:
                    processType,

                priority:
                    priority,

                predictedBurst:
                    predictedBurst

            });


            // ==================================
            // Clear Existing Table
            // ==================================

            processTableBody.innerHTML =
                "";


            // ==================================
            // Sort Processes by AI Prediction
            // ==================================

            const sortedProcesses =
                [...processes].sort(
                    (a, b) =>
                        a.predictedBurst -
                        b.predictedBurst
                );


            // ==================================
            // Display Processes
            // ==================================

            sortedProcesses.forEach(
                process => {

                    const row =
                        document.createElement(
                            "tr"
                        );


                    row.innerHTML = `

                        <td>
                            ${process.processId}
                        </td>

                        <td>
                            ${process.cpu}
                        </td>

                        <td>
                            ${process.memory}
                        </td>

                        <td>
                            ${process.io}
                        </td>

                        <td>
                            Type ${process.processType}
                        </td>

                        <td>
                            ${process.priority}
                        </td>

                        <td>

                            <strong>
                                ${process.predictedBurst}
                            </strong>

                        </td>

                    `;


                    processTableBody.appendChild(
                        row
                    );

                }
            );


            // ==================================
            // Generate Scheduling Orders
            // ==================================


            // ==================================
            // FCFS Order
            // ==================================

            const fcfsOrderText =
                processes
                    .map(
                        (process, index) =>
                            `${index + 1}. ${process.processId}`
                    )
                    .join("<br>");


            fcfsOrder.innerHTML =
                fcfsOrderText;



            // ==================================
            // SJF Order
            // ==================================

            const sjfOrderText =
                sortedProcesses
                    .map(
                        (process, index) =>
                            `${index + 1}. ${process.processId}
                            (${process.predictedBurst})`
                    )
                    .join("<br>");


            sjfOrder.innerHTML =
                sjfOrderText;



            // ==================================
            // AI + OpenMP Order
            // ==================================

            const aiOrderText =
                sortedProcesses
                    .map(
                        (process, index) =>
                            `${index + 1}. ${process.processId}
                            (${process.predictedBurst})`
                    )
                    .join("<br>");


            aiOpenMPOrder.innerHTML =
                aiOrderText;



            // ==================================
            // Main AI Scheduling Order
            // ==================================

            schedulingOrder.innerHTML = `

                <strong>
                    AI-Based Scheduling Order
                </strong>

                <br><br>

                ${aiOrderText}

            `;


            // ==================================
            // Automatically Create Next ID
            // ==================================

            document.getElementById(
                "process-id-input"
            ).value =
                "P" +
                (101 + processes.length);


            // ==================================
            // Generate Parallel Timeline
            // ==================================

            generateExecutionTimeline(
                sortedProcesses
            );


        }

        catch (error) {

            alert(
                "Unable to connect to AI API. " +
                "Make sure Flask is running."
            );


            console.error(error);

        }

    }
);