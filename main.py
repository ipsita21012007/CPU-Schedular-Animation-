import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scheduling_algorithms import Scheduler
from process import Process

class CPUAnimation:
    def __init__(self):
        
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(12, 10))
        self.fig.suptitle('CPU Scheduling Algorithms Visualization', fontsize=16, fontweight='bold')
        
        # Sample processes for demonstration
        self.processes = [
            Process(1, 0, 5),
            Process(2, 1, 3),
            Process(3, 2, 8),
            Process(4, 3, 6),
            Process(5, 4, 2)
        ]
        
        self.schedulers = {
            "FCFS": Scheduler(),
            "SJF": Scheduler(),
            "Round Robin": Scheduler()
        }
        
        # Run all scheduling algorithms
        self.schedulers["FCFS"].fcfs(self.processes.copy())
        self.schedulers["SJF"].sjf(self.processes.copy())
        self.schedulers["Round Robin"].round_robin(self.processes.copy())
        
        self.current_algorithm = "FCFS"
        self.current_time = 0
        self.max_time = max(scheduler.current_time for scheduler in self.schedulers.values())
        
        # Colors for different processes
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
    def init_animation(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        # Set up the axes
        self.ax1.set_xlim(0, self.max_time + 2)
        self.ax1.set_ylim(0, 3)
        self.ax1.set_title(f'{self.current_algorithm} - Gantt Chart', fontweight='bold')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('CPU')
        self.ax1.grid(True, alpha=0.3)
        
        self.ax2.set_xlim(0, self.max_time + 2)
        self.ax2.set_ylim(0, len(self.processes) + 1)
        self.ax2.set_title('Process States', fontweight='bold')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Processes')
        self.ax2.grid(True, alpha=0.3)
        
        self.ax3.set_xlim(0, self.max_time + 2)
        self.ax3.set_ylim(0, 10)
        self.ax3.set_title('CPU Utilization & Queue Status', fontweight='bold')
        self.ax3.set_xlabel('Time')
        self.ax3.set_ylabel('Metrics')
        self.ax3.grid(True, alpha=0.3)
        
        return []
    
    def update_animation(self, frame):
        self.current_time = frame
        self.init_animation()
        
        scheduler = self.schedulers[self.current_algorithm]
        
        # Draw Gantt chart
        self.draw_gantt_chart(scheduler)
        
        # Draw process states
        self.draw_process_states(scheduler)
        
        # Draw CPU utilization and queue
        self.draw_metrics(scheduler)
        
        # Switch algorithm every 40 frames (for 2-minute animation)
        if frame > 0 and frame % 40 == 0:
            algorithms = list(self.schedulers.keys())
            current_index = algorithms.index(self.current_algorithm)
            self.current_algorithm = algorithms[(current_index + 1) % len(algorithms)]
        
        return []
    
    def draw_gantt_chart(self, scheduler):
        """Draw the Gantt chart for current time"""
        for pid, start, end in scheduler.gantt_chart:
            if start <= self.current_time:
                duration = min(end, self.current_time) - start
                if duration > 0:
                    color_idx = (pid - 1) % len(self.colors)
                    self.ax1.barh(1, duration, left=start, height=0.6, 
                                 color=self.colors[color_idx], alpha=0.8)
                    self.ax1.text(start + duration/2, 1, f'P{pid}', 
                                ha='center', va='center', fontweight='bold')
        
        # Draw timeline
        for time in range(0, int(self.max_time) + 1, 2):
            self.ax1.axvline(x=time, color='gray', linestyle='--', alpha=0.5)
            self.ax1.text(time, 0.3, str(time), ha='center')
    
    def draw_process_states(self, scheduler):
        """Draw process states at current time"""
        for i, process in enumerate(self.processes):
            y_pos = len(self.processes) - i
            
            # Process label
            self.ax2.text(-0.5, y_pos, f'P{process.pid}', fontweight='bold', 
                         ha='right', va='center')
            
            # Determine process state
            state = "Waiting"
            state_color = 'red'
            
            for pid, start, end in scheduler.gantt_chart:
                if pid == process.pid:
                    if start <= self.current_time < end:
                        state = "Running"
                        state_color = 'green'
                        break
                    elif self.current_time >= end:
                        state = "Completed"
                        state_color = 'blue'
                        break
                    elif process.arrival_time <= self.current_time:
                        state = "Ready"
                        state_color = 'orange'
            
            if self.current_time < process.arrival_time:
                state = "Not Arrived"
                state_color = 'gray'
            
            # Draw state indicator
            self.ax2.scatter(self.current_time, y_pos, color=state_color, s=100, zorder=3)
            self.ax2.text(self.current_time, y_pos + 0.3, state, 
                         ha='center', va='bottom', fontsize=8)
    
    def draw_metrics(self, scheduler):
        """Draw CPU utilization and queue information"""
        # CPU utilization
        busy_time = 0
        for _, start, end in scheduler.gantt_chart:
            if start <= self.current_time:
                busy_time += min(end, self.current_time) - start
        
        utilization = (busy_time / self.current_time * 100) if self.current_time > 0 else 0
        self.ax3.bar(1, utilization, color='skyblue', alpha=0.7)
        self.ax3.text(1, utilization + 0.5, f'{utilization:.1f}%', 
                     ha='center', va='bottom', fontweight='bold')
        self.ax3.text(1, -1, 'CPU Utilization', ha='center', va='top')
        
        # Ready queue
        ready_count = 0
        for process in self.processes:
            arrived = process.arrival_time <= self.current_time
            completed = any(pid == process.pid and self.current_time >= end 
                          for pid, start, end in scheduler.gantt_chart)
            running = any(pid == process.pid and start <= self.current_time < end 
                         for pid, start, end in scheduler.gantt_chart)
            
            if arrived and not completed and not running:
                ready_count += 1
        
        self.ax3.bar(3, ready_count, color='lightgreen', alpha=0.7)
        self.ax3.text(3, ready_count + 0.5, str(ready_count), 
                     ha='center', va='bottom', fontweight='bold')
        self.ax3.text(3, -1, 'Ready Queue', ha='center', va='top')
        
        # Current algorithm info
        self.ax3.text(5, 8, f'Algorithm: {self.current_algorithm}', 
                     fontweight='bold', fontsize=12, bbox=dict(boxstyle="round,pad=0.3", 
                     facecolor='lightyellow', alpha=0.7))
        
        self.ax3.set_xticks([1, 3, 5])
        self.ax3.set_xticklabels(['Utilization', 'Queue', 'Info'])
    
    def run_animation(self):
        """Run the animation"""
        # The line below has an error - it's calling the wrong function
        # anim = animation.run_animation(  # FIXED: lowercase 'f'
        
        # Correct version: use matplotlib's FuncAnimation
        anim = animation.FuncAnimation(
            self.fig, self.update_animation, init_func=self.init_animation,
            frames=int(self.max_time * 1.2), interval=200, blit=False, repeat=True
        )
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    cpu_animation = CPUAnimation()
    cpu_animation.run_animation()
    