from Task import Task, genetic

zbieranie_wymiarow = False
J = []
n_wczytywanie = 0 # zmienna pomocnicza do wczytywania danych
m = 0 # ilość maszyn zapis per zestaw danych
n = 0 # ilość zadań  zapis per zestaw danych

for line in open('data.txt', 'rt'):
  line_data = line.rstrip()

  if(n_wczytywanie > 0):
    n_wczytywanie = n_wczytywanie -1
    J.append(Task(line_data.split(' '),n - 1 - n_wczytywanie))
    if(n_wczytywanie == 0):
      genetic(J,m)


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
      if(line_data[-2] == '1'):
        break