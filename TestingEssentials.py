from RandomGenerator import RandomGenerator 
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import pandas as pd
import copy

##########################################################
#
#           Część odpowiedzialna za podstawowe operacje na zbiorze zadań i permutacji
#
##########################################################



def GenerateJ(_n,_M,_seed):   
  """Generates job processing times matrix and permutation vector.

  Args:
      _n (int): Number of jobs.
      _M (int): Number of machines.
      _seed (int): Seed for random number generation.

  Returns:
      tuple: Tuple containing job processing times matrix (J) and permutation vector (pi).
          J (list): List of lists representing job processing times matrix, where J[i][j] is the processing time
                    of job i on machine j.
          pi (list): Permutation vector representing the order of jobs.
  """
  rng = RandomGenerator(_seed)
  n = _n
  M  = _M
  J = []
  pi = []
  for i in range(n):
      p_ij = [rng.next_int(1, 9) for _ in range(M)]
      pi.append(i);
      J.append(copy.deepcopy(p_ij))
  return J, pi



def getMakData(ograniczenie):
  """Gets data from Dr. Makuchowski's dataset and returns a list of cases.

  Returns:
      list: List of cases, where each case contains a list of tasks.
          Each task is represented by a list of processing times on machines.
          Processing times are consecutive time units describing the time of performing a task on one machine.
  """
  dataToReturn = []
  zbieranie_wymiarow = False
  zbierz_rozw_neh = False
  zbierz_perm_neh = False
  J = []
  cmax = 0
  n_wczytywanie = 0 # zmienna pomocnicza do wczytywania danych
  m = 0 # ilość maszyn zapis per zestaw danych
  n = 0 # ilość zadań  zapis per zestaw danych

  for line in open('data.txt', 'rt'):
    line_data = line.rstrip()

    if(n_wczytywanie > 0):
      n_wczytywanie = n_wczytywanie -1
      H = []
      for strNum in line_data.split(' '):
        H.append(int(strNum))
      J.append(H)
      #if(n_wczytywanie == 0):
      #  dataToReturn.append(J)
        #print(str(J))

    if(zbieranie_wymiarow):
      zbieranie_wymiarow = False
      wym = line_data.split(' ')
      n = int(wym[0])
      n_wczytywanie = n
      m = int(wym[1])
      J = []

    if(len(line_data) > 4):
      if( line_data[0] + line_data[1] + line_data[2] + line_data[3] == 'data' ):
        zbieranie_wymiarow = True
        if(int(line_data[-4]+line_data[-3]+line_data[-2]) == ograniczenie):
          print("OGRANICZONO, wczytanod do(ale bez) data."+line_data[-4]+line_data[-3]+line_data[-2])
          print(ograniczenie)
          break

    if zbierz_perm_neh:
      H = []
      for strNum in line_data.split(' '):
        H.append(int(strNum))
      dataToReturn.append([J,cmax,H])
      zbierz_perm_neh = False
    
    if zbierz_rozw_neh:
      cmax = int(line_data)
      zbierz_rozw_neh = False
      zbierz_perm_neh = True

    if(len(line_data) >= 4):
      if (line_data[0] + line_data[1] + line_data[2] == 'neh'):
        zbierz_rozw_neh = True

  return dataToReturn



def EvaluateC(_J, _pi): 
  """Calculates C for the task sequence in the given _J, extendable to multiple machines.

  Args:
      _J (list): List of tasks.
          Each task is represented by a list of processing times on machines.
      _pi (list): Permutation representing the order of tasks.

  Returns:
      list: List representing the schedule of completion times (C).
          Each element C[i][j] represents the completion time of task i on machine j.
  """
  J_matrix = [_J[_pi[i]] for i in range(len(_pi))]
  n = len(J_matrix)
  m = len(J_matrix[0])
  C = [[0] * m for _ in range(n)]

  C[0][0] = J_matrix[0][0]  # Czas zakończenia 1. zadania na 1. maszynie
  for i in range(1,m):
      C[0][i] = J_matrix[0][i]+C[0][i-1] # Obliczamy czasy zakończenia 1. zadania na reszcie maszyn

  # Czasy zakończenia pozostałych zadań
  for j in range(1, n): 
      for i in range(m):
          C[j][i] = max(C[j-1][i], C[j][i-1]) + J_matrix[j][i] # zadanie moze zacząć się dopiero jak jego część na poprzedniej maszynie zostanie zrealizowana oraz aktualna maszyna sie zwolni. 
                                                          # Aby uzyskać czas ukończenia musimy dodać jeszcze czas trwania
  return C



def C_MaxFromC(C):
  """Calculates Cmax for the task sequence based on the given completion schedule.

  Args:
      C (list): Completion schedule.
          Each element C[i][j] represents the completion time of task i on machine j.

  Returns:
      int: Completion time of the last task.
  """
  Cmax = C[-1][-1]
  return Cmax



def C_Max(data, permutation):
  """Calculates Cmax for the task sequence based on the given data and permutation.

  Args:
      data (list): List of tasks.
          Each task is represented by a list of processing times on machines.
      permutation (list): Permutation representing the order of tasks.

  Returns:
      int: Completion time of the last task.
  """
  m = len(data[0])
  Cmax = []
  for _ in range(0,m):
    Cmax.append(0)
  
  for task_id in permutation:
    task = data[task_id]
    Cmax[0] += task[0]
    for i in range(1,m):
      if(Cmax[i-1] > Cmax[i]):
        Cmax[i] = Cmax[i-1]
      Cmax[i] += task[i]
  return Cmax[m-1]



def start_t(_J, _pi, _C):
  """Calculates start times for tasks based on the given data, permutation, and completion schedule.

  Args:
      _J (list): List of tasks.
          Each task is represented by a list of processing times on machines.
      _pi (list): Permutation representing the order of tasks.
      _C (list): Completion schedule.
          Each element _C[i][j] represents the completion time of task i on machine j.

  Returns:
      list: List of lists representing start times for tasks.
          Each element represents the start time of the corresponding task on each machine.
  """
  J_matrix = [_J[_pi[i]] for i in range(len(_pi))]
  return [[_C[i][j] - J_matrix[i][j] for j in range(len(_C[i]))] for i in range(len(_C))]