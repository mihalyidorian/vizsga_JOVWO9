from abc import ABC, abstractmethod
from datetime import datetime
class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def get_info(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)

    def get_info(self):
        return f"Egyágyas szoba, Ár: {self.ar}, Szobaszám: {self.szobaszam}"

class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)

    def get_info(self):
        return f"Kétágyas szoba, Ár: {self.ar}, Szobaszám: {self.szobaszam}"

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def szoba_hozzaad(self, szoba):
        self.szobak.append(szoba)

    def get_info(self):
        info = f"Szálloda: {self.nev}\n"
        for szoba in self.szobak:
            info += szoba.get_info() + "\n"
        return info

class Foglalas:
    foglalasok = []

    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum
        Foglalas.foglalasok.append(self)

    @staticmethod
    def foglal(szoba, datum):
        if Foglalas.foglalas_lehetseges(szoba, datum):
            uj_foglalas = Foglalas(szoba, datum)
            print(f"Foglalás rögzítve: Szoba {szoba.szobaszam}, Dátum: {datum}, Ár: {szoba.ar}")
            return szoba.ar
        return None

    @staticmethod
    def lemond(foglalas):
        Foglalas.foglalasok.remove(foglalas)
        print(f"Foglalás lemondva: Szoba {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")

    @staticmethod
    def listaz_foglalasok():
        if not Foglalas.foglalasok:
            print("Nincsenek foglalások.")
            return
        print("Foglalások lista:")
        for f in Foglalas.foglalasok:
            print(f"Szoba {f.szoba.szobaszam}, Dátum: {f.datum}")

    @staticmethod
    def foglalas_lehetseges(szoba, datum):
        if datetime.strptime(datum, "%Y-%m-%d") <= datetime.now():
            print("Csak jövőbeli dátumra lehet foglalni")
            return False

        for f in Foglalas.foglalasok:
            if f.szoba == szoba and f.datum == datum:
                print("Ez a szoba már foglalt ezen a dátumon")
                return False

        return True

szalloda = Szalloda("Corinthia Hotel")
szoba1 = EgyagyasSzoba(10000, 101)
szoba2 = KetagyasSzoba(15000, 102)
szoba3 = EgyagyasSzoba(12000, 103)
szalloda.szoba_hozzaad(szoba1)
szalloda.szoba_hozzaad(szoba2)
szalloda.szoba_hozzaad(szoba3)

Foglalas.foglal(szoba1, "2023-12-05")
Foglalas.foglal(szoba2, "2023-12-08")
Foglalas.foglal(szoba3, "2023-11-29")
Foglalas.foglal(szoba1, "2023-12-20")
Foglalas.foglal(szoba2, "2024-01-05")

Foglalas.foglal(szoba1, "2023-11-30")
Foglalas.listaz_foglalasok()

foglalas_lemond = Foglalas(szoba1, "2023-11-30")
Foglalas.lemond(foglalas_lemond)
Foglalas.listaz_foglalasok()

def szoba_keresese(szam):
    return next((szoba for szoba in szalloda.szobak if szoba.szobaszam == szam), None)

def foglalas_keresese(szobaszam, datum):
    return next((f for f in Foglalas.foglalasok if f.szoba.szobaszam == szobaszam and f.datum == datum), None)

while True:
    print("\nVálasszon egy műveletet:")
    print("1 - Foglalás")
    print("2 - Lemondás")
    print("3 - Foglalások listázása")
    print("4 - Kilépés")

    valasztas = input("Kérem adja meg a választását (1-4) ")

    if valasztas == "1":
        try:
            szobaszam = int(input("Adja meg a szoba számát: "))
            datum = input("Adja meg a dátumot (YYYY-MM-DD formátumban): ")
            kivalasztott_szoba = szoba_keresese(szobaszam)
            if kivalasztott_szoba:
                Foglalas.foglal(kivalasztott_szoba, datum)
            else:
                print("Nincs ilyen szobaszám.")
        except ValueError:
            print("Érvénytelen szobaszám vagy dátum formátum.")

    elif valasztas == "2":
        szobaszam = int(input("Adja meg a szoba számát, amelyikből le szeretné mondani a foglalást: "))
        datum = input("Adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")

        lemondando_foglalas = next((f for f in Foglalas.foglalasok if f.szoba.szobaszam == szobaszam and f.datum == datum), None)
        if lemondando_foglalas:
            Foglalas.lemond(lemondando_foglalas)
        else:
            print("Nincs ilyen foglalás")

    elif valasztas == "3":
        Foglalas.listaz_foglalasok()

    elif valasztas == "4":
        break
    else:
        print("Érvénytelen választás")
