import simpy
import numpy as np
import matplotlib.pyplot as plt
import itertools

def gen_inter_arrival_time():
    return np.random.exponential(0.5)

def gen_inter_arrival_time_of_priority():
    return np.random.exponential(0.5)

def gen_service_time():
    #return np.random.exponential(0.95)
    return 0.5

i=0

def simulation_run1(env,servers,i):

    while True:
        i+=1
        env.process(packet1(env,i,servers,priority=1))
        yield env.timeout(gen_inter_arrival_time_of_priority())

def simulation_run2(env,servers,i):

    while True:
        i+=1
        env.process(packet2(env,i,servers,priority=2))
        yield env.timeout(gen_inter_arrival_time())
        

wait_time = []
wait_time_of_priority =[]
wait_time_of_normal=[]
number_of_packets_departure=[]
number_of_priority_packets_departure=[]
number_of_normal_packets_departure=[]

def packet1 (env,packet, servers, priority):
    with servers.request(priority=priority) as request:
        time_arrival=env.now
        print (env.now, '{} przychodzi pakiet z priorytetem'.format(packet))
        yield request
        print (env.now, '{} pakiet z priorytetem jest obslugiwany'.format(packet))
        yield env.timeout(gen_service_time())
        print (env.now, '{} pakiet z priorytetem opuszcza serwer'.format(packet))
        time_depart = env.now
        wait_time.append(time_depart-time_arrival)
        wait_time_of_priority.append(time_depart-time_arrival)
        number_of_packets_departure.append(0)
        number_of_priority_packets_departure.append(0)

def packet2 (env,packet, servers, priority):
    with servers.request(priority=priority) as request:
        time_arrival_of_normal=env.now
        print (env.now, '{} przychodzi zwykly pakiet'.format(packet))
        yield request
        print (env.now, '{} zwykly pakiet jest obslugiwany'.format(packet))
        yield env.timeout(gen_service_time())
        print (env.now, '{} !!!! zwykly pakiet opuszcza serwer !!!!'.format(packet))
        time_depart = env.now
        wait_time.append(time_depart-time_arrival_of_normal)
        wait_time_of_normal.append(time_depart-time_arrival_of_normal)
        number_of_packets_departure.append(0)
        number_of_normal_packets_departure.append(0)

obs_times = []
q_length = []

def results(env,servers):
    while True:
        obs_times.append(env.now)
        q_length.append(len(servers.queue))
        yield env.timeout(0.5)

np.random.seed(1)

env=simpy.Environment()

servers = simpy.PriorityResource(env, capacity=1)
i=0
env.process(simulation_run1(env,servers,i))
env.process(simulation_run2(env,servers,i))
env.process(results(env,servers))

env.run(until=110)

sum_wait_time = sum(wait_time)
avg_q_length=sum(q_length)/len(q_length)
part_sum_wait_time = list(itertools.accumulate(wait_time))
avg_priority_time=sum(wait_time_of_priority)/len(number_of_priority_packets_departure)
avg_normal_time=sum(wait_time_of_normal)/len(number_of_normal_packets_departure)
percent = len(number_of_priority_packets_departure)/len(number_of_packets_departure)*100
print ("###################################################################################################################")
print (f"Zostalo obsluzonych w sumie {len(number_of_packets_departure)} pakietow w tym {len(number_of_priority_packets_departure)} pakietow priorytetowych co stanowi {percent}% calosci")
print(f"Calkowity czas oczekiwania dla wszystkich pakietow wyniosl {sum(wait_time)}")
print(f"Calkowity czas oczekiwania dla pakietow priorytetowych wyniosl {sum(wait_time_of_priority)}")
if number_of_normal_packets_departure==[]:
    number_of_normal_packets_departure=[1]
print(f"Calkowity czas oczekiwania dla pakietow zwyklych wyniosl {sum(wait_time_of_normal)}")
print(f"Sredni czas oczekiwania na obsluge dla jednego pakietu wyniosl {sum(wait_time)/len(number_of_packets_departure)}")
print(f"Sredni czas oczekiwania na obsluge dla jednego pakietu priorytetowego wyniosl {avg_priority_time} a dla zwyklego {avg_normal_time} ")
print(f"Srednie zapelnienie kolejki wynioslo {avg_q_length}")
print ("###################################################################################################################")

len_array = [i+1 for i in range(len(number_of_packets_departure))]

plot1=plt.figure(1)
plt.hist(wait_time)
plt.xlabel('Czas oczekiwania (min)')
plt.ylabel('Liczba pakietow')

plot1=plt.figure(2)
plt.plot(len_array,part_sum_wait_time)
plt.xlabel('N-ty pakiet')
plt.ylabel('Sumaryczny czas oczekiwania')

plot1=plt.figure(3)
plt.plot(len_array,wait_time)
plt.xlabel('N-ty pakiet')
plt.ylabel('Czas oczekiwania')

plot2=plt.figure(4)
plt.step(obs_times, q_length, where='post')
plt.xlabel('Czas (min)')
plt.ylabel('Zapelnienie kolejki')
plt.show()




