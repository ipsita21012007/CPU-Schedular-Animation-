# CPU-Schedular-Animation-
📋 Project Overview
A Python-based animated visualization that demonstrates three fundamental CPU scheduling algorithms: FCFS (First-Come-First-Serve). This educational tool provides real-time visual insights into how operating systems manage process execution.

🎯 Features
Real-time Animation: Watch algorithms in action with smooth transitions.

Visual Metrics: Track CPU utilization, ready queue status, and process states.

Interactive Display: Three-panel visualization showing Gantt charts, process states, and performance metrics.

Educational Focus: Perfect for understanding operating system concepts.

🛠 Technologies Used
Python 3.13.7

Matplotlib for animation and visualization

NumPy for numerical operations

VS Code as the primary development environment
🚀 Installation & Setup
Prerequisites
Python 3.13.7 or higher

VS Code (recommended) or any Python IDE

Step-by-Step Setup
Clone or Download the Project

bash
# Create project directory
mkdir cpu-scheduling-animation
cd cpu-scheduling-animation
Set Up Virtual Environment (Recommended)

bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
Install Dependencies

bash
pip install matplotlib numpy
Create Project Files

Copy the provided Python files into your project directory

Ensure you have:

main.py

process.py

scheduling_algorithms.py

🎮 How to Run
Method 1: Using VS Code
Open the project folder in VS Code

Open the integrated terminal (`Ctrl + ``)

Run the animation:

bash
python main.py
Method 2: Using Command Line
Navigate to project directory

Activate virtual environment (if using)

Execute:

bash
python main.py
📊 What You'll See
The animation displays three synchronized panels:

1. Gantt Chart (Top)
Visual timeline of process execution

Color-coded process blocks

Real-time progression through time units

2. Process States (Middle)
Current state of each process:

🔴 Waiting: Process has arrived but not executing

🟢 Running: Currently executing on CPU

🟠 Ready: In ready queue, waiting for CPU

🔵 Completed: Finished execution

⚫ Not Arrived: Yet to arrive in system

3. Performance Metrics (Bottom)
CPU Utilization: Percentage of time CPU is busy

Ready Queue: Number of processes waiting

Current Algorithm: Active scheduling method

⚙️ Scheduling Algorithms Explained
FCFS (First-Come-First-Serve)
Processes executed in arrival order

Simple but can lead to convoy effect

Non-preemptive

🎨 Customization
Modifying Process Parameters
Edit the process list in main.py:

python
self.processes = [
    Process(1, 0, 5),   # PID, Arrival Time, Burst Time
    Process(2, 1, 3),
    Process(3, 2, 8),
    Process(4, 3, 6),
    Process(5, 4, 2)
]
Adjusting Animation Speed
Modify the interval parameter in main.py:

python
anim = animation.FuncAnimation(
    ..., interval=200, ...  # Lower = faster, Higher = slower
)
Changing Time Quantum (Round Robin)
Modify in scheduling_algorithms.py:

python
def round_robin(self, processes, time_quantum=2):  # Change this value
🐛 Troubleshooting
Common Issues & Solutions
Import Errors:

bash
# Ensure all files are in same directory
ls -la  # Should show main.py, process.py, scheduling_algorithms.py
Module Not Found:

bash
# Reinstall dependencies
pip install --upgrade matplotlib numpy
Animation Window Doesn't Open:

bash
# Try different matplotlib backend
python -c "import matplotlib; matplotlib.use('TkAgg'); import main"
Virtual Environment Issues:

bash
# Reactivate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
📈 Educational Value
This visualization helps understand:

Scheduling Criteria: Waiting time, turnaround time, throughput

Algorithm Trade-offs: FCFS vs SJF vs Round Robin

Preemptive vs Non-preemptive scheduling

CPU Utilization concepts

Process State transitions

🤝 Contributing
Feel free to:

Add more scheduling algorithms

Improve visualization aesthetics

Add interactive controls

Extend with performance statistics

📝 License
This project is open source and available for educational purposes.

👨‍💻 Author : IPSITA ROY 
Created for operating systems education and visualization.

🕒 Runtime Information
Duration: Approximately 2 minutes total

Algorithm Rotation: Changes every ~40 seconds

Frame Rate: 200ms per frame for smooth animation
