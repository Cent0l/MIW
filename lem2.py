import pandas as pd
from collections import Counter


# Dane wejściowe
dane = pd.read_csv('file.txt', sep=" ", header=None)
n = dane.shape[1]
dane.columns=[f'a{i+1}' for i in range(n-1)]+['d']

atrybuty = dane.columns[:-1]  # bez kolumny decyzyjnej

reguly = []

# Dla każdej unikalnej wartości decyzji (np. 1, 2)
for decyzja in sorted(dane['d'].unique()):

    # Zbiór indeksów obiektów, które jeszcze nie są pokryte regułą
    pozostale = set(dane.index[dane['d'] == decyzja])

    while pozostale:

        # Liczymy częstość występowania par (atrybut, wartość) wśród pozostałych
        czestosci = {}
        for atr in atrybuty:
            wystapienia = Counter(dane.loc[list(pozostale), atr])
            for wartosc, ile in wystapienia.items():
                czestosci[(atr, wartosc)] = ile

        # Szukamy najlepszego (najczęstszego) deskryptora
        najlepszy = None
        najwiecej = -1
        for (a, v), ilosc in czestosci.items():
            if ilosc > najwiecej:
                najlepszy = (a, v)
                najwiecej = ilosc

        # Tworzymy regułę z jednym deskryptorem
        regula = [najlepszy]

        # Rozszerzamy regułę aż będzie niesprzeczna
        while True:
            dopasowane = set(dane.index)
            for atr, val in regula:
                dopasowane = dopasowane & set(dane.index[dane[atr] == val])

            # Sprawdzamy, czy wszystkie obiekty mają tę samą decyzję
            zgodna = True
            for i in dopasowane:
                if dane.loc[i, 'd'] != decyzja:
                    zgodna = False
                    break
            if zgodna:
                break  # reguła jest dobra

            # Szukamy obiektu do rozszerzenia reguły
            kandydaci = dopasowane & pozostale
            if not kandydaci:
                break

            wybrany = min(kandydaci)
            wiersz = dane.loc[wybrany]

            mozliwe = []
            for atr in atrybuty:
                nowy = (atr, wiersz[atr])
                if nowy not in regula:
                    nowa_regula = regula + [nowy]
                    nowe_dopasowane = set(dane.index)
                    for a_, v_ in nowa_regula:
                        nowe_dopasowane = nowe_dopasowane & set(dane.index[dane[a_] == v_])
                    pokrycie = len(nowe_dopasowane & set(dane.index[dane['d'] == decyzja]))
                    mozliwe.append((nowy, pokrycie))

            if not mozliwe:
                break

            # Wybieramy najlepszy z możliwych (największe pokrycie, potem kolejność atrybutów)
            mozliwe.sort(key=lambda x: (-x[1], list(atrybuty).index(x[0][0])))
            regula.append(mozliwe[0][0])

        # Zaznaczamy które obiekty są pokryte tą regułą
        pokryte = set(dane.index)
        for a, v in regula:
            pokryte = pokryte & set(dane.index[dane[a] == v])
        pokryte = pokryte & pozostale

        reguly.append((regula, decyzja, len(pokryte)))
        pozostale -= pokryte

# Wypisujemy wszystkie reguły
for i, (regula, decyzja, ile) in enumerate(reguly):
    lewa = " ∧ ".join(f"({a} = {v})" for a, v in regula)
    prawa = f"(d = {decyzja})"
    sup = f"[{ile}]" if ile > 1 else ""
    print(f"reg: {i+1} {lewa} => {prawa}{sup}")
