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
    print(str(task))
    Cmax[0] += task[0]
    for i in range(1,m):
      if(Cmax[i-1] > Cmax[i]):
        Cmax[i] = Cmax[i-1]
      Cmax[i] += task[i]
  return Cmax[m-1]

