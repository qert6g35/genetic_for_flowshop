#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <cmath>

using namespace std;

struct zadanie
{
  int id;
  bool czy_dodane;
  int *p; // czas trwania
};

string data_name(int ktore)
{
  string ret = "data.000:";
  ret[7] += ktore % 10;
  ret[6] += (ktore / 10) % 10;
  ret[5] += (ktore / 100) % 10;
  return ret;
}

int C_max(zadanie zadania[500], int *Kol_id, int ile_zad, int m)
{
  int *C_maszyny = (int *)malloc(sizeof(int) * m);
  for (int masz = 0; masz < m; masz++)
  {
    C_maszyny[masz] = 0;
  }
  for (int zad = 0; zad < ile_zad; zad++)
  {
    C_maszyny[0] += zadania[Kol_id[zad]].p[0];
    for (int masz = 1; masz < m; masz++)
    {
      if (C_maszyny[masz - 1] > C_maszyny[masz])
      {
        C_maszyny[masz] = C_maszyny[masz - 1];
      }
      C_maszyny[masz] += zadania[Kol_id[zad]].p[masz];
    }
  }
  return C_maszyny[m - 1];
}

int C_max2(zadanie zadania[500], int *Kol_id, int ile_zad, int m)
{ // na ostatnim miejscu row ma być dodawane zadanie, a zwrócone zostanie najleprzed id;
  int **C_maszyny = (int **)malloc(sizeof(int *) * m);
  int **C_maszynyRev = (int **)malloc(sizeof(int *) * m);

  for (int masz = 0; masz < m; masz++)
  {
    C_maszyny[masz] = (int *)malloc(sizeof(int) * ile_zad);
    C_maszynyRev[masz] = (int *)malloc(sizeof(int) * ile_zad);
    for (int zad = 0; zad < ile_zad; zad++)
    {
      C_maszyny[masz][zad] = 0;
      C_maszynyRev[masz][zad] = 0;
    }
  }

  for (int zad = 0; zad < ile_zad; zad++)
  { //                         Wyliczanie Tabel Pomocniczych
    // masz = 0
    C_maszyny[0][zad] += zadania[Kol_id[zad]].p[0];
    C_maszynyRev[m - 1][ile_zad - 1 - zad] += zadania[Kol_id[ile_zad - 1 - zad]].p[m - 1];
    if (zad != 0)
    {
      C_maszynyRev[m - 1][ile_zad - 1 - zad] += C_maszynyRev[m - 1][ile_zad - zad];
      C_maszyny[0][zad] += C_maszyny[0][zad - 1];
    } //                                                          Etap maszyny pierwszej/ ostatniej
    for (int masz = 1; masz < m; masz++)
    {
      if (zad != 0)
      {
        if (C_maszyny[masz - 1][zad] > C_maszyny[masz][zad - 1])
        { // koniec szasu na maszynach regular
          C_maszyny[masz][zad] = C_maszyny[masz - 1][zad];
        }
        else
        {
          C_maszyny[masz][zad] = C_maszyny[masz][zad - 1];
        }

        if (C_maszynyRev[m - 1 - (masz) + 1][ile_zad - 1 - zad] > C_maszynyRev[m - 1 - (masz)][ile_zad - zad])
        { // koniec czasu maszyny masz na zadaniu zad
          C_maszynyRev[m - 1 - (masz)][ile_zad - 1 - zad] = C_maszynyRev[m - 1 - (masz) + 1][ile_zad - 1 - zad];
        }
        else
        {
          C_maszynyRev[m - 1 - (masz)][ile_zad - 1 - zad] = C_maszynyRev[m - 1 - (masz)][ile_zad - zad];
        }
      }
      else
      {
        C_maszyny[masz][zad] = C_maszyny[masz - 1][zad];
        C_maszynyRev[m - 1 - (masz)][ile_zad - 1 - zad] = C_maszynyRev[m - 1 - (masz) + 1][ile_zad - 1 - zad];
      }
      C_maszyny[masz][zad] += zadania[Kol_id[zad]].p[masz];
      C_maszynyRev[m - 1 - masz][ile_zad - 1 - zad] += zadania[Kol_id[ile_zad - 1 - zad]].p[m - 1 - masz];
    }
  }

  //		for(int zad = 0; zad < ile_zad;zad++){
  //		for(int masz = 0; masz < m; masz++){
  //			cout<<"["<<C_maszyny[masz][zad]<<","<<C_maszynyRev[masz][zad]<<"]  ";
  //		}
  //		cout<<"zmiana ZAD"<<endl;
  //	}

  int BestPoz = -1;
  int BestC = 9999999999;
  int *pom_c = (int *)malloc(sizeof(int) * m);
  int czast_trwania_pom;
  for (int miejsce = 0; miejsce < ile_zad + 1; miejsce++)
  {
    for (int masz = 0; masz < m; masz++)
    {
      pom_c[masz] = zadania[Kol_id[ile_zad]].p[masz];
      if (miejsce > 0)
      {
        pom_c[masz] += C_maszyny[masz][miejsce - 1];
      }
      if (miejsce < (ile_zad))
      {
        pom_c[masz] += C_maszynyRev[masz][miejsce];
      }
      // dodaj do poma czasy z zadania
    }

    czast_trwania_pom = pom_c[0];
    for (int masz = 0; masz < m; masz++)
    {
      if (czast_trwania_pom <= pom_c[masz])
      {
        czast_trwania_pom = pom_c[masz];
      }
    }
    if (czast_trwania_pom < BestC)
    {
      BestPoz = miejsce;
      BestC = czast_trwania_pom;
    }
  }

  return BestPoz;
}

void swap(int a, int b, int *id_rozwionzania)
{
  int pom = id_rozwionzania[a];
  id_rozwionzania[a] = id_rozwionzania[b];
  id_rozwionzania[b] = pom;
}

int ktore_dodajemy(zadanie zadania[500], int n, int m)
{
  int waga = 0;
  int pom;
  int wybrane_zad;
  for (int i = 0; i < n; i++)
  {
    if (zadania[i].czy_dodane == false)
    {
      pom = zadania[i].p[0];
      for (int j = 1; j < m; j++)
      {
        pom += zadania[i].p[j];
      }
      if (waga <= pom)
      {
        waga = pom;
        wybrane_zad = i;
      }
    }
  }
  zadania[wybrane_zad].czy_dodane = true;
  return wybrane_zad;
}

void Szeregoj(zadanie zadania[500], int *id_rozwionzania, int n, int m)
{
  int sprawdzane_zad;
  int poz_naj;
  int Cmax_naj; // C_max najleprzego
  int Cmax_pom;

  for (int ktore_dodaje = 0; ktore_dodaje < n; ktore_dodaje++)
  {
    id_rozwionzania[ktore_dodaje] = ktore_dodajemy(zadania, n, m);
    // Cmax_naj = C_max(zadania,id_rozwionzania,ktore_dodaje + 1,m);
    // cout<<Cmax_naj;
    poz_naj = 0;
    if (ktore_dodaje > 0)
    {
      poz_naj = C_max2(zadania, id_rozwionzania, ktore_dodaje, m);
      // cout<<"dodajemy id:"<<1 + id_rozwionzania[ktore_dodaje]<<" na miejsce"<<poz_naj<<endl;
    }
    // cout<<ktore_dodaje<<"<poz "<<id_rozwionzania[ktore_dodaje]<<"wpisano_id na zerowym >>";
    // cout<<endl<<id_rozwionzania[0]+1<<"   naj poz :"<<poz_naj;
    for (int pom = ktore_dodaje; pom > poz_naj; pom--)
    {
      swap(pom, pom - 1, id_rozwionzania);
    }
    // cout<<"  rozw[naj_poz]"<<id_rozwionzania[poz_naj]+1<<endl;
  }
}

int main()
{

  cout << "start" << endl;
  ifstream PLIK("data.txt"); // szeregowy
  string w = "";             // skiper
  zadanie zadania[500];      // kowalsi
  int n;                     // ilosc procesów
  int m;                     // ilosc maszyn
  int *id_rozwionzania;

  for (int dataloop = 0; dataloop <= 120; dataloop++)
  {
    while (w != data_name(dataloop))
    {
      PLIK >> w;
    }

    PLIK >> n >> m;
    id_rozwionzania = (int *)malloc(sizeof(int) * n);
    // cout<<"data."<<dataloop<<" n = "<<n<<" m = "<<m<<endl;
    // cout<<"\n Przed sortowaniem \n";
    for (int i = 0; i < n; i++)
    {
      zadania[i].id = i;
      zadania[i].czy_dodane = false;
      zadania[i].p = (int *)malloc(sizeof(int) * m);
      for (int j = 0; j < m; j++)
      {
        PLIK >> zadania[i].p[j];
        // cout<<zadania[i].p[j];
      }
      // cout<<endl;
    }
    // cout<<"Szereguje:"<<endl;
    Szeregoj(zadania, id_rozwionzania, n, m);
    //    	id_rozwionzania[0] = 0;
    //		id_rozwionzania[1] = 3;
    //		id_rozwionzania[2] = 2;
    //		id_rozwionzania[3] = 1;
    //		cout<<"ostatnie dodaje na miejsce:"<<C_max2(zadania,id_rozwionzania, 3, m)<<" dodaje:"<<id_rozwionzania[3];

    // for(int i = 0; i < n;i++){
    //	cout<<" "<<id_rozwionzania[i] + 1;
    // }
    // cout<<endl<<"Rozw:"<<C_max(zadania,id_rozwionzania,n,m)<<endl;
    free(id_rozwionzania);
  } // ________________________PĘTLA DLA KAŻDEGO ZESAWU DANYCH___________________________
  cout << "koniec" << endl;
}
