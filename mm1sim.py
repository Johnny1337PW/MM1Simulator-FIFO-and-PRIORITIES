import simpy
import numpy as np
import matplotlib.pyplot as plt
import itertools

def gen_inter_arrival_time():
    return np.random.exponential(1)

def gen_service_time():
    #return np.random.exponential(0.99)
    return (0.99)

def simulation_run(env,servers):
    i=0
    while True:
        i+=1
        yield env.timeout(gen_inter_arrival_time())
        env.process(packet(env,i,servers))

wait_time = []
number_of_packets_departure=[]
def packet (env,packet, servers):
    with servers.request() as request:
        time_arrival=env.now
        print (env.now, '{} pakiet przychodzi'.format(packet))
        yield request
        print (env.now, '{} pakiet jest obslugiwany'.format(packet))
        yield env.timeout(gen_service_time())
        print (env.now, '{} pakiet opuszcza serwer'.format(packet))
        time_depart = env.now
        wait_time.append(time_depart-time_arrival)
        number_of_packets_departure.append(0)

obs_times = []
q_length = []

def results(env,servers):
    while True:
        obs_times.append(env.now)
        q_length.append(len(servers.queue))
        yield env.timeout(0.5)

np.random.seed(2)

env=simpy.Environment()

servers = simpy.Resource(env, capacity=1)

env.process(simulation_run(env,servers))
env.process(results(env,servers))

env.run(until=120)

sum_wait_time = sum(wait_time)

avg_q_length=sum(q_length)/len(q_length)
avg_g_time=sum(wait_time)/len(number_of_packets_departure)
part_sum_wait_time = list(itertools.accumulate(wait_time))
print ("############################################################################################")
print (f"Zostalo obsluzonych w sumie {len(number_of_packets_departure)} pakietow")
print(f"Calkowity czas oczekiwania dla wszystkich pakietow wyniosl {sum(wait_time)}")
print(f"Sredni czas oczekiwania na obsluge dla jednego pakietu wyniosl {avg_g_time}")
print(f"Srednie zapelnienie kolejki wynioslo {avg_q_length}")
print ("############################################################################################")

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




