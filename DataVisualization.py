from RandomGenerator import RandomGenerator 
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

##########################################################
#
#           Część odpowiedzialna za wykresy
#
##########################################################

# Generuje losowy kolor dla zadania do wykresu
# Przyjmowane zmienne
# rng       - obiekt RandomGenerator
#
# Zwracane zmienne
# color_hex - kod hex koloru

def generate_random_color(rng):
    r = rng.next_int(0, 255)
    g = rng.next_int(0, 255)
    b = rng.next_int(0, 255)
    color_hex = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    return color_hex    

# zwraca dataframe z taskami do wykresu
# Przyjmowane zmienne
# J             - lista zadań
# pi            - permutacja
# start_times   - harmonogram czasów rozpoczęcia
#
# Zwracane zmienne
# df            - dataframe potrzebny do wygenerowania wykresu

def tasks_df(pi, J, start_times):
    n = len(J)  # liczba zadań
    m = len(J[0])  # liczba mapipszyn
    data = []
    Tasks = [J[pi[i]] for i in range(len(pi))]
    c_dict = {}
    rng = RandomGenerator(1)
    for task in range(n):
        for machine in range(m):
            start_time = start_times[task][machine]
            duration = Tasks[task][machine]
            hlp =  str(pi[task])
            if not hlp in c_dict:
                c_dict[hlp] = generate_random_color(rng)
            color = c_dict[hlp]
            data.append([pi[task], machine+1, start_time, duration, color])

    df = pd.DataFrame(data, columns=['Zadanie', 'Maszyna', 'Czas_Rozpoczęcia', 'Czas_Trwania','Color'])
    return df

# Wyświetla poglądowy wykres ganta dla ulozonych zadań
# Przyjmowane zmienne
# df            - dataframe generowany przez funckje task_df

def plot_schedule(df):
    fig, ax = plt.subplots(1, figsize=(16,6))
    ax.barh(df.Maszyna, df.Czas_Trwania, left=df.Czas_Rozpoczęcia,color=df.Color)
    plt.show()

# Wyświetla wykres ganta dla ulozonych zadań
# Przyjmowane zmienne
# J             - lista zadań
# pi            - permutacja
# start_times   - harmonogram czasów rozpoczęcia
#

def plot_schedule_fancy(pi, J, start_times):
    n = len(J)  # liczba zadań
    m = len(J[0])  # liczba mapipszyn
    Tasks = [J[pi[i]] for i in range(len(pi))]
    data = []
    c_dict = {}
    end_set = set()
    rng = RandomGenerator(1)
    for task in range(n):
        for machine in range(m):
            start_time = start_times[task][machine]
            duration = Tasks[task][machine]
            end_set.add(start_time+duration)
            hlp = str(pi[task])
            if not hlp in c_dict:
                c_dict[hlp] = generate_random_color(rng)
            color = c_dict[hlp]
            data.append([pi[task], machine+1, start_time, duration, color])

    df = pd.DataFrame(data, columns=['Zadanie', 'Maszyna', 'Czas_Rozpoczęcia', 'Czas_Trwania','Color'])
    fig, ax = plt.subplots(1, figsize=(16,6))
    ax.barh(df.Maszyna, df.Czas_Trwania, left=df.Czas_Rozpoczęcia,color=df.Color)
    legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
    plt.legend(handles=legend_elements)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel('czas')
    plt.ylabel('maszyny')
    plt.xticks(list(end_set))
    plt.show()
    
    