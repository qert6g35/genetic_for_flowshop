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

# Zwraca listę J obiektów typu Task na podstawie zadanych parametrów
# Przyjmowane zmienne
# _n        - ilość zadań
# _M        - ilość maszyn
# _seed     - seed dla generatora pseudolosowegos
#
# Zwracane zmienne
# J         - lista zadań
# pi        - permutacja

def GenerateJ(_n,_M,_seed):     
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

#
# funkcja pobierająca dane makuchowskiego i zwracająca 
# listę:[przypadki]
# przypadek:[zadania]
# zadanie:[czasy {4,2,5 ...}]
# czasy to kolejne jednostki czasowe opisujące czas wykonywania się elementu zadania na jednej maszynie
def getMakData():
  dataToReturn = []
  zbieranie_wymiarow = False
  J = []
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
      if(n_wczytywanie == 0):
        dataToReturn.append(J)
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
        if(line_data[-2] == '3'):
          break

  return dataToReturn

# Oblicza C dla kolejności zadań w podanym _J, rozszerzalne na wiele maszyn
# Przyjmowane zmienne
# _J        - lista zadań
# _pi       - permutacja
#
# Zwracane zmienne
# C         - harmonogram czasów zakończenia


def EvaluateC(_J, _pi):           
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

# Oblicza Cmax dla kolejności zadań w podanym _J, na podstawie harmonogramu czasów
# Przyjmowane zmienne
# C         - harmonogram czasów zakończenia
#
# Zwracane zmienne
# Cmax      - czas zakończenia ostatniego zadania

def C_MaxFromC(C):
    Cmax = C[-1][-1]
    return Cmax

#
#   funkcja wyliczająca długość ciągu o podanych danych (data) i podanej permutacji (permutation)
#
def C_Max(data, permutation):
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

# Oblicza C dla kolejności zadań w podanym _J, rozszerzalne na wiele maszyn
# Przyjmowane zmienne
# _J        - lista zadań
# _C        - harmonogram czasów zakończenia
# _pi       - permutacja
#
# Zwracane zmienne
# _         - lista z listami czasów rozpoczęcia obiektów

def start_t(_J, _pi, _C):
    J_matrix = [_J[_pi[i]] for i in range(len(_pi))]
    return [[_C[i][j] - J_matrix[i][j] for j in range(len(_C[i]))] for i in range(len(_C))]