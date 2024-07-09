import threading
import time
from queue import Queue

resource1 = 0
resource2 = 0
resource3 = 0
lock = threading.Lock()

ready_queue1 = Queue()
ready_queue2 = Queue()
ready_queue3 = Queue()
ready1 = []
ready2 = []
ready3 = []
waiting_index = []
waiting = Queue()
utilization1 = 0
ready1_state = True
utilization2 = 0
ready2_state = True
utilization3 = 0
ready3_state = True
p1_process_count = 0
p2_process_count = 0
p3_process_count = 0

tasks = []

print("Enter the number of resources(r1, r2, r3): ")
resource1, resource2, resource3= map(int, input().split())
print("Enter tasks (press Enter to finish):")
while True:
    line = input()
    if line.strip() == "":
        break
    tasks.append(line.split())
for i in tasks:
    i.append(0)
    for j in range(1, len(i)):
        i[j] = int(i[j])

tasks.sort(key=lambda x: (x[1], x[6]))
for i in tasks:
    if i[6] == 1:
        p1_process_count += 1
    elif(i[6] == 2):
        p2_process_count += 1
    elif(i[6] == 3):
        p3_process_count += 1
if p1_process_count:
    max_utilization1 = p1_process_count * (2 ** (1 / p1_process_count) - 1)
if p2_process_count:
    max_utilization2 = p2_process_count * (2 ** (1 / p2_process_count) - 1)
if p3_process_count:
    max_utilization3 = p3_process_count * (2 ** (1 / p3_process_count) - 1)
min1 = 10000
min2 = 10000
min3 = 10000
ready1_index = 0
ready2_index = 0
ready3_index = 0
waiting_index = 0
for i in tasks:
    preferred_processor = int(i[6])
    if preferred_processor == 1:
        if min1 > i[1] :
            min1 = i[1]
        if (ready1_state):
            if (utilization1 + (i[2] / i[1]) < max_utilization1):
                utilization1 += (i[2] / i[1])
                ready_queue1.put(i)
                ready1_index += 1
                ready1.append(i)
            else:
                ready1_state = False
                waiting_index += 1
                waiting.put(i)
        else:
            waiting_index += 1
            waiting.put(i)

    elif (preferred_processor == 2):
        if min2 > i[1]:
            min2 = i[1]
        if (ready2_state):
            if (utilization2 + (i[2] / i[1]) < max_utilization2):
                utilization2 += (i[2] / i[1])
                ready_queue2.put(i)
                ready2_index += 1
                ready2.append(i)
            else:
                ready2_state = False
                waiting_index += 1
                waiting.put(i)
        else:
            waiting_index += 1
            waiting.put(i)

    elif(preferred_processor == 3):
        if min3 > i[1] :
            min3 = i[1]
        if (ready3_state):
            if (utilization3 + (i[2] / i[1]) < max_utilization3):
                utilization3 += (i[2] / i[1])
                ready_queue3.put(i)
                ready3_index += 1
                ready3.append(i)
            else:
                ready3_state = False
                waiting_index += 1
                waiting.put(i)
        else:
            waiting_index += 1
            waiting.put(i)





def run_task(ready , resource1 , resource2 , resource3 , p):
    tim = 0
    i = 1
    while not (ready.empty() and waiting.empty()):
        while not ready.empty():
            x = ready.get()
            if x[3] <= resource1 and x[4] <= resource2 and x[5] <= resource3:
                with lock:
                    resource1 -= x[3]
                    resource2 -= x[4]
                    resource3 -= x[5]
            else:
                waiting.put(x)
                continue
            if x[8] == 0:
                tim += x[2]
                if (p * i) >= tim:
                    print("the running task is: ", x[0])
                    if x[6] == 1:
                        print("the ready queue of p1 is: ", ready1)
                    elif x[6] == 2:
                        print("the ready queue of p2 is: ", ready2)
                    else:
                        print("the ready queue of p3 is: ", ready3)
                    time.sleep(x[2])
                    x[7] -= 1
                    if x[7] > 0:
                        waiting.put(x)
                else:
                    tim -= x[2]
                    q = ((p * i) - (tim))
                    x[8] = x[2] - q
                    tim += q
                    print("the running task is: ", x[0])
                    if x[6] == 1:
                        print("the ready queue of p1 is: ", ready1)
                    elif x[6] == 2:
                        print("the ready queue of p2 is: ", ready2)
                    else:
                        print("the ready queue of p3 is: ", ready3)
                    time.sleep(q)
                    i += 1
                    if x[7] > 0:
                        waiting.put(x)
            else:
                tim += x[8]
                if p * i >= tim:
                    time.sleep(x[8])
                    x[7] -= 1
                    x[8] = 0
                else:
                    tim -= x[8]
                    q = (p * i) - tim
                    x[8] = x[8] - q
                    tim += q
                    time.sleep(q)
                    i += 1
                    if x[7] > 0:
                        waiting.put(x)
            with lock:
                resource1 += x[3]
                resource2 += x[4]
                resource3 += x[5]

            continue
        if not waiting.empty():
            y = waiting.get()
            ready.put(y)
            if y[6] == 1:
                ready1.append(y)
            if y[6] == 2:
                ready2.append(y)
            if y[6] == 3:
                ready3.append(y)
            continue

threads = []
start = time.time()
if ready1:
    threads.append(threading.Thread(target=run_task, args=(ready_queue1 , resource1 , resource2 , resource3 , min1)))
if ready2:
    threads.append(threading.Thread(target=run_task, args=(ready_queue2 , resource1 , resource2 , resource3 , min2)))
if ready3:
    threads.append(threading.Thread(target=run_task, args=(ready_queue3 , resource1 , resource2 , resource3 , min3)))
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end = time.time()
print("the execution time is ", end-start)
