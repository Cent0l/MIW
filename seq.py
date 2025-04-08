import numpy as np
import itertools

# Wczytanie danych z pliku
plik = "macierz.txt"
dane = np.loadtxt(plik, dtype=int)

liczba_kolumn = dane.shape[1]
atrybuty = list(range(liczba_kolumn - 1))  # ostatnia kolumna to decyzja

reguly = []
pokryte_indeksy = []

# Dla każdej liczby atrybutów (od 1 do wszystkich)
for ile_atr in range(1, len(atrybuty) + 1):

    # Generujemy kombinacje atrybutów np. (0, 1), (0, 2), itp.
    kombinacje = list(itertools.combinations(atrybuty, ile_atr))

    for i in range(len(dane)):
        if i in pokryte_indeksy:
            continue

        obiekt = dane[i]

        for kombinacja in kombinacje:
            if i in pokryte_indeksy:
                break

            sprzeczna = False

            # Sprawdzamy, czy kombinacja tworzy regułę sprzeczną z innym obiektem
            for j in range(len(dane)):
                if i == j:
                    continue

                inny = dane[j]
                zgodne = True
                for a in kombinacja:
                    if obiekt[a] != inny[a]:
                        zgodne = False
                        break

                if zgodne and obiekt[-1] != inny[-1]:
                    sprzeczna = True
                    break

            if sprzeczna:
                continue

            # Obiekty pokryte przez regułę
            pokryte = []
            for k in range(len(dane)):
                zgodny = True
                for a in kombinacja:
                    if dane[k][a] != obiekt[a]:
                        zgodny = False
                        break
                if zgodny:
                    pokryte.append(k)

            # Dodajemy do listy pokrytych
            for x in pokryte:
                if x not in pokryte_indeksy:
                    pokryte_indeksy.append(x)

            # Tworzymy regułę jako tekst
            lewa = ""
            for a in kombinacja:
                lewa += f"(a{a+1}={obiekt[a]}) ∧ "
            lewa = lewa[:-3]  # usuwamy ostatnie " ∧ "

            prawa = f"(d={obiekt[-1]})"

            pokrycie = f"[{len(pokryte)}]" if len(pokryte) > 1 else ""

            tekst_reguly = f"o{i+1} {lewa} => {prawa}{pokrycie}"

            if tekst_reguly not in reguly:
                reguly.append(tekst_reguly)

# Wypisanie wszystkich reguł
for r in reguly:
    print(r)
