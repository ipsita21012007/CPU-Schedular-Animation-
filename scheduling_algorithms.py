import heapq
from process import Process

class Scheduler:
    def __init__(self):
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
    
    def fcfs(self, processes):
        """First Come First Serve Scheduling"""
        processes.sort(key=lambda x: x.arrival_time)
        self.current_time = 0
        
        for process in processes:
            if self.current_time < process.arrival_time:
                self.current_time = process.arrival_time
            
            process.start_time = self.current_time
            self.current_time += process.burst_time
            process.completion_time = self.current_time
            process.waiting_time = process.start_time - process.arrival_time
            
            self.gantt_chart.append((process.pid, process.start_time, process.completion_time))
            self.completed_processes.append(process)
    
    def sjf(self, processes):
        """Shortest Job First Scheduling"""
        processes.sort(key=lambda x: x.arrival_time)
        self.current_time = 0
        ready_queue = []
        process_index = 0
        
        while process_index < len(processes) or ready_queue:
            # Add arriving processes to ready queue
            while (process_index < len(processes) and 
                   processes[process_index].arrival_time <= self.current_time):
                heapq.heappush(ready_queue, (processes[process_index].burst_time, process_index))
                process_index += 1
            
            if ready_queue:
                burst_time, idx = heapq.heappop(ready_queue)
                process = processes[idx]
                
                process.start_time = self.current_time
                self.current_time += process.burst_time
                process.completion_time = self.current_time
                process.waiting_time = process.start_time - process.arrival_time
                
                self.gantt_chart.append((process.pid, process.start_time, process.completion_time))
                self.completed_processes.append(process)
            else:
                self.current_time += 1
    
    def round_robin(self, processes, time_quantum=2):
        """Round Robin Scheduling"""
        processes.sort(key=lambda x: x.arrival_time)
        self.current_time = 0
        ready_queue = []
        process_index = 0
        
        # Create copies to preserve original burst times
        process_copies = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes]
        
        while process_index < len(process_copies) or ready_queue:
            # Add arriving processes to ready queue
            while (process_index < len(process_copies) and 
                   process_copies[process_index].arrival_time <= self.current_time):
                ready_queue.append(process_copies[process_index])
                process_index += 1
            
            if ready_queue:
                process = ready_queue.pop(0)
                
                if process.start_time is None:
                    process.start_time = self.current_time
                
                execution_time = min(time_quantum, process.remaining_time)
                start_execution = self.current_time
                self.current_time += execution_time
                process.remaining_time -= execution_time
                
                self.gantt_chart.append((process.pid, start_execution, self.current_time))
                
                # Add arriving processes during execution
                while (process_index < len(process_copies) and 
                       process_copies[process_index].arrival_time <= self.current_time):
                    ready_queue.append(process_copies[process_index])
                    process_index += 1
                
                if process.remaining_time > 0:
                    ready_queue.append(process)
                else:
                    process.completion_time = self.current_time
                    process.waiting_time = process.completion_time - process.arrival_time - process.burst_time
                    self.completed_processes.append(process)
            else:
                self.current_time += 1