import random
import sys

def expon(mean):
    return random.expovariate(1.0 / mean)

# Simulation parameters
SIM_TIME = 160.0  # 160 hours
time_next_event = {'arrive': expon(2), 'inspect': float('inf'), 'repair1': float('inf'), 'repair2': float('inf')}
sim_time = 0.0
prev_sim_time = 0.0

# State variables
server_inspect = 'idle'
servers_repair = [False, False]  # False is empty, True is full

time_inspect = []
time_repair = []

delays_inspect = []
delays_repair = []

num_buses_inspected = 0
num_buses_repaired = 0

total_queue_time_inspect = 0
total_queue_time_repair = 0

busy_time_inspect = 0
busy_time_repair = 0

def timing():
    global sim_time, next_event_type, time_next_event

    next_event_type = min(time_next_event, key=time_next_event.get)
    sim_time = time_next_event[next_event_type]

def arrive():
    global time_next_event, sim_time, time_inspect, server_inspect, num_buses_inspected, busy_time_inspect

    time_next_event['arrive'] = sim_time + expon(2)

    if server_inspect == 'busy':
        time_inspect.append(sim_time)
    else:
        num_buses_inspected += 1
        server_inspect = 'busy'
        temp_time = random.uniform(0.25, 1.05)
        busy_time_inspect += temp_time
        time_next_event['inspect'] = sim_time + temp_time


def inspect():
    global sim_time, time_next_event, servers_repair, time_repair, num_buses_repaired, busy_time_repair, time_inspect, server_inspect, num_buses_inspected, busy_time_inspect

    if random.random() <= 0.3:
        if all(servers_repair): 
            time_repair.append(sim_time)
        else:
            num_buses_repaired += 1
            for i in range(2):
                if not servers_repair[i]:
                    servers_repair[i] = True
                    temp_time = random.uniform(2.1, 4.5)
                    busy_time_repair += temp_time
                    time_next_event[f'repair{i}'] = sim_time + temp_time
                    break
        
            
    if len(time_inspect) > 0:
        num_buses_inspected += 1
        delays_inspect.append(sim_time - time_inspect.pop(0))
        temp_time = random.uniform(0.25, 1.05)
        busy_time_inspect += temp_time
        time_next_event['inspect'] = sim_time + temp_time
    else:
        server_inspect = 'idle'
        time_next_event['inspect'] = float('inf')


def repair(station):
    global time_next_event, servers_repair, busy_time_repair, num_buses_repaired
    
    servers_repair[station] = False
    
    if len(time_repair) > 0:
        num_buses_repaired += 1
        delays_repair.append(sim_time - time_repair.pop(0))
        servers_repair[station] = True
        temp_time = random.uniform(2.1, 4.5)
        busy_time_repair += temp_time
        time_next_event[f'repair{station}'] = sim_time + temp_time
    else:
        time_next_event[f'repair{station}'] = float('inf')

while sim_time < SIM_TIME:
    timing()
    total_queue_time_inspect += len(time_inspect)*(sim_time-prev_sim_time)
    total_queue_time_repair += len(time_repair)*(sim_time-prev_sim_time)
    if next_event_type == 'arrive':
        arrive()
    elif next_event_type == 'inspect':
        inspect()
    elif next_event_type.startswith('repair'):
        repair(int(next_event_type[-1]))
    
    prev_sim_time = sim_time

def print_stats():
    print(f'Average delay in inspection queue: {sum(delays_inspect) / len(delays_inspect):.2f} hours')
    print(f'Average delay in repair queue: {sum(delays_repair) / len(delays_repair):.2f} hours')
    print(f'Average queue size (inspection): {total_queue_time_inspect / SIM_TIME:.2f}')
    print(f'Average queue size (repair): {total_queue_time_repair / SIM_TIME:.2f}')
    print(f'Utilization of inspection station: {busy_time_inspect / SIM_TIME * 100:.2f}%')
    print(f'Utilization of repair stations: {(busy_time_repair / SIM_TIME) / 2 * 100:.2f}%')

print_stats()

