from MTP_lib import *

def heuristic_algorithm(file_path):
    '''
    1. Write your heuristic algorithm here.
    2. We would call this function in grading_program.py to evaluate your algorithm.
    3. Please do not change the function name and the file name.
    4. Do not import any extra library. We will import libraries from MTP_lib.py.
    5. The parameter is the file path of a data file, whose format is specified in the document.
    6. You need to return your schedule in two lists "machine" and "completion_time".
        (a) machine[j][0] is the machine ID (an integer) of the machine to process the first stage of job j + 1, and
            machine[j][1] is the machine ID (an integer) of the machine to process the second stage of job j + 1.
            Note. If job j + 1 has only one stage, you may store any integer in machine[j][1].
        (b) completion_time[j][0] is the completion time (an integer or a floating-point number) of the first stage of job j + 1, and
            completion_time[j][1] is the completion time (an integer or a floating-point number) of the second stage of job j + 1.
            Note. If job j + 1 has only one stage, you may store any integer or floating-point number in completion_time[j][1].
        Note 1. If you have n jobs, both the two lists are n by 2 (n rows, 2 columns).
        Note 2. In the list "machine", you should record the IDs of machines
                (i.e., to let machine 1 process the first stage of job 1,
                you should have machine[0][0] == 1 rather than machine[0][0] == 0).
    7. The only PY file that you need and are allowed to submit is this algorithm_module.py.
    '''

    # read data and store the information into your self-defined variables
    fp = open(file_path, 'r')
    # for a_row in fp:
    #    print(a_row) # a_row is a list
    # ...

    # start your algorithm here
    tardiness = 0
    machine = []
    completion_time = []

    class Job:
        def __init__(self, id, s1, s2, m1, m2, due):
            self.id = id
            self.s1 = s1
            self.s2 = s2
            self.m1 = m1
            self.m2 = m2
            self.due = due
            self.common_elem = set()
        def copy(self):
            return copy.deepcopy(self)
        lefttime = 0
        s1_finishtime = 0

    def compare(job1, myJob): 
        target = myJob.due - myJob.lefttime
        if job1.due-job1.lefttime - target <= 0:
            return True
        return False 

    def insert_job(jobs, myJob):  # 二分搜插入
        if len(jobs) == 0:
            jobs.append(myJob)
        else:
            left = 0
            right = len(jobs)-1
            result = -1
            while left <= right:
                mid = (left + right) // 2
                if compare(jobs[mid], myJob): # compare(job < Target)
                    result = mid
                    left = mid + 1
                else:
                    right = mid - 1
            if result < (len(jobs)-1):
                jobs.insert(result+1, myJob)
            else:
                jobs.append(myJob)
                
    def plan(job, current_machine_time, machine_time):
        plan_job = job.copy()
        current_machine_time += plan_job.s1
        plan_job.s1_finishtime = current_machine_time
        
        choice = job.m2
        machine_list = []
        for index in choice:
            index = int(index)
            machine_list.append(machine_time[index-1])
            
        for mt in machine_list:
            if mt == 0 or mt < plan_job.s1_finishtime + 1.0001:
                return True
        return False
    def theEarlistMachine(job, machine_time, machine_id):
        if machine_time[int(machine_id)-1] == 0:
            return True
        choice = job.m1
        machine_list = []
        for index in choice:
            index = int(index)
            machine_list.append(machine_time[index-1])

        best = min(machine_list)

        if machine_time[int(machine_id)-1] == best:
            return True
        return False
    def find_earliest_machine(job, machine_time): 
        choice = job.m2
        machine_list = []
        for index in choice:
            index = int(index)
            machine_list.append(machine_time[index-1])
        for elem in machine_list:
            if elem == min(machine_list):
                return elem
        
    def pick_job(jobs, machine_id, machine_time, machine, completion_time, tardiness, chooseSequence):
        if (len(jobs) != 0):
            for i in range(0, len(jobs)):
                if jobs[i].s1_finishtime < 0.0001 and machine_id in jobs[i].m1:
                    if (not theEarlistMachine(jobs[i], machine_time, machine_id)):
                        return tardiness   
                    if jobs[i].s2 != 0 and (not plan(jobs[i], machine_time[int(machine_id)-1], machine_time)):
                        mt = find_earliest_machine(jobs[i], machine_time)
                        for j in range(len(jobs)):
                            if j == i: continue
                            if jobs[j].s2 == 0 and machine_time[int(machine_id)-1]+jobs[j].s1 <= mt-jobs[i].s1:
                                jobs[j].lefttime -= jobs[j].s1  
                                machine_time[int(machine_id)-1] += jobs[j].s1
                                jobs[j].s1_finishtime = machine_time[int(machine_id)-1]
                                # for output
                                machine[jobs[j].id-1][0] = int(machine_id)
                                completion_time[jobs[j].id-1][0] = machine_time[int(machine_id)-1]
                                
                                tardiness += max(0, machine_time[int(machine_id)-1]-jobs[j].due)
                                jobs.pop(j)
                                return tardiness
                        machine_time[int(machine_id)-1] = mt
                        continue          
                    jobs[i].lefttime -= jobs[i].s1  
                    machine_time[int(machine_id)-1] += jobs[i].s1
                    jobs[i].s1_finishtime = machine_time[int(machine_id)-1]
                    # for output
                    machine[jobs[i].id-1][0] = int(machine_id)
                    completion_time[jobs[i].id-1][0] = machine_time[int(machine_id)-1]
                    
                    if jobs[i].lefttime < 0.0001 or jobs[i].s2 == 0:
                        tardiness += max(0, machine_time[int(machine_id)-1]-jobs[i].due)
                        jobs.pop(i)
                        return tardiness
                if machine_time[int(machine_id)-1] - jobs[i].s1_finishtime < 1.0001 and jobs[i].lefttime-jobs[i].s2 < 0.0001 and machine_id in jobs[i].m2:
                    if machine_time[int(machine_id)-1] >= jobs[i].s1_finishtime:
                        machine_time[int(machine_id)-1] += jobs[i].s2
                        # for output
                        machine[jobs[i].id-1][1] = int(machine_id)
                        completion_time[jobs[i].id-1][1] = machine_time[int(machine_id)-1]
                        
                        tardiness += max(0, machine_time[int(machine_id)-1]-jobs[i].due)
                        jobs.pop(i)
                        return tardiness
                elif jobs[i].s1_finishtime > 0.0001 and jobs[i].s2 != 0:
                    for id in chooseSequence:
                        if id not in jobs[i].m2:
                            continue
                        id = int(id)
                        for j in range(len(jobs)):
                            if j == i: continue
                            if machine_id not in (jobs[j].m1 & jobs[j].m2): continue
                            if jobs[j].s2 != 0 and machine_time[id-1]+jobs[j].s1+jobs[j].s2 <= jobs[i].s1_finishtime:
                                jobs[j].lefttime -= jobs[j].s1 
                                machine_time[id-1] += jobs[j].s1  
                                jobs[j].s1_finishtime = machine_time[id-1]    
                                
                                # for output
                                machine[jobs[j].id-1][0] = int(id)
                                completion_time[jobs[j].id-1][0] = machine_time[id-1]
                                
                                jobs[j].lefttime -= jobs[j].s2  
                                machine_time[id-1] += jobs[j].s2  
            
                                machine[jobs[j].id-1][1] = int(id)
                                completion_time[jobs[j].id-1][1] = machine_time[id-1]
                                
                                tardiness += max(0, machine_time[id-1]-jobs[j].due)
                                jobs.pop(j)
                                return tardiness
                        
                        for j in range(len(jobs)):
                            if j == i: continue
                            if jobs[j].s2 == 0 and machine_time[id-1]+jobs[j].s1 <= jobs[i].s1_finishtime:
                                jobs[j].lefttime -= jobs[j].s1  
                                machine_time[id-1] += jobs[j].s1
                                jobs[j].s1_finishtime = machine_time[id-1]
                                # for output
                                machine[jobs[j].id-1][0] = int(id)
                                completion_time[jobs[j].id-1][0] = machine_time[id-1]
                                
                                tardiness += max(0, machine_time[id-1]-jobs[j].due)
                                jobs.pop(j)
                                return tardiness
                    
                        machine_time[id-1] += jobs[i].s2
                        # for output
                        machine[jobs[i].id-1][1] = int(id)
                        completion_time[jobs[i].id-1][1] = machine_time[id-1]
                        
                        tardiness += max(0, machine_time[id-1]-jobs[i].due)
                        jobs.pop(i)
                        return tardiness
            return tardiness
        else:
            return tardiness
        
    df = pd.read_csv(file_path)
    num_of_rows = len(df)
    jobs = list()
    check_jobs = list()
    machines_time = list()
    machine_used_times = dict()
    for i in range(num_of_rows):
        myJob = Job(df.iloc[i]['Job ID'],  # int
                    df.iloc[i]['Stage-1 Processing Time'],  # float
                    df.iloc[i]['Stage-2 Processing Time'],  # float
                    set(str(df.iloc[i]['Stage-1 Machines']).split(',')),  # string
                    set(str(df.iloc[i]['Stage-2 Machines']).split(',')),  # string
                    int(df.iloc[i]['Due Time']))  # float
        myJob.lefttime = myJob.s1+myJob.s2
        for m in myJob.m1:
            machine_used_times.setdefault(m, 0)
            machine_used_times[m] += 1
        for m in myJob.m2:
            machine_used_times.setdefault(m, 0)
            machine_used_times[m] += 1
        check_jobs.append(myJob)
        insert_job(jobs, myJob)
    if 'nan' in machine_used_times.keys():
        del machine_used_times['nan']
    for job in jobs:
        print(job.s1, job.s2, job.m1, job.m2, job.due, job.lefttime)
    print(machine_used_times)
    for i in range(len(machine_used_times)):
        machines_time.append(0)
    def custom_key(job_id):
        return (machine_used_times[job_id], job_id)
    chooseSequence = sorted(machine_used_times, key=custom_key, reverse = True)
    r = sorted(machine_used_times, key=custom_key, reverse = False)
    print(chooseSequence)
    print([jobs[i].id for i in range(len(jobs))])
    # initialize output
    for _ in range(len(jobs)):
        machine.append([0, 0])
        completion_time.append([0.0, 0.0])
        
    while len(jobs) != 0:
        for machineid in chooseSequence:
            tardiness= pick_job(jobs, machineid, machines_time, machine, completion_time, tardiness, r)

            
    print(machine)
    print(completion_time)
    print(machines_time)

    def check_waiting_time (completion_time, jobs):
        for i in range(len(jobs)):
            if not(completion_time[i][1] - jobs[i].s2 - completion_time[i][0] < 1.01):
                return False
        return True
    print(check_waiting_time(completion_time, check_jobs))

    print(machine)
    for i in range(len(check_jobs)):
        print(completion_time[i][0]-check_jobs[i].s1, completion_time[i][0], completion_time[i][1]-check_jobs[i].s2, completion_time[i][1])   
    makespan = max(machines_time)   

    def check_feasible(jobs, id, machine, completion_time):
        format = []
        for i in range(len(machine)):
            if machine[i][0] == id:
                format.append([completion_time[i][0]-jobs[i].s1, completion_time[i][0]])
            if machine[i][1] == id:
                format.append([completion_time[i][1]-jobs[i].s2, completion_time[i][1]])
        format = sorted(format)
        print('->', format)
        return format

    for i in range(len(machine_used_times)): 
        print(f'machine{i+1}') 
        format = check_feasible(check_jobs, i+1, machine, completion_time)   
        for j in range(0, len(format)-1):
            if format[j+1][0] - format[j][1] < -0.1:
                print('ERROR machine -------------------------------------------------')
                
    print("total makespan =", makespan)
    print("total tardiness =", tardiness)
    # ...

    return machine, completion_time
