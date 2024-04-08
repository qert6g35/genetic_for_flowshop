

class Zadanie:

  def __init__(self,czasy,_id) -> None:
    self.id = _id
    self.czasy = []
    for liczba in czasy.split(' '):
      self.czasy.append(int(liczba))
    #print("id:" + str(self.id) +" czasy:" + str(self.czasy))

def C_max(zadania, permutacja):
  max_czas = 0
  return max_czas

def genetic(Zadania, Maszyny):
  print(str(Zadania))


zbieranie_wymiarow = False
zadania = []
n_wczytywanie = 0 # zmienna pomocnicza do wczytywania danych
m = 0 # ilość maszyn zapis per zestaw danych
n = 0 # ilość zadań  zapis per zestaw danych

for line in open('data.txt', 'rt'):
  line_data = line.rstrip()

  if(n_wczytywanie > 0):
    n_wczytywanie = n_wczytywanie -1
    zadania.append(Zadanie(line_data,n - n_wczytywanie))
    if(n_wczytywanie == 0):
      genetic(zadania,m)


  if(zbieranie_wymiarow):
    zbieranie_wymiarow = False
    wym = line_data.split(' ')
    n = int(wym[0])
    n_wczytywanie = n
    m = int(wym[1])
    zadania = []


  if(len(line_data) > 4):
    if( line_data[0] + line_data[1] + line_data[2] + line_data[3] == 'data' ):
      zbieranie_wymiarow = True
      if(line_data[-2] == '2'):
        break