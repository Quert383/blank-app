import streamlit as st
from scipy.optimize import newton

def oblicz_rrso(wyplaty, splaty):
    def funkcja(X):
        lewa = sum(ck / (1 + X)**tk for ck, tk in wyplaty)
        prawa = sum(dl / (1 + X)**sl for dl, sl in splaty)
        return lewa - prawa

    X0 = 0.05  # początkowe przybliżenie 5%
    try:
        wynik = newton(funkcja, X0)
        return round(wynik * 100, 1)  # RRSO w procentach
    except RuntimeError:
        return None

def main():
    st.title("Obliczanie Rzeczywistej Rocznej Stopy Oprocentowania (RRSO)")

    st.header("🔵 Dane o wypłatach kredytu")
    m = st.number_input("Podaj liczbę wypłat:", min_value=1, step=1)

    wyplaty = []
    for i in range(int(m)):
        st.subheader(f"Wypłata nr {i+1}")
        ck = st.number_input(f"Kwota wypłaty nr {i+1} (zł):", key=f"ck_{i}", format="%.2f")
        tk = st.number_input(f"Czas wypłaty nr {i+1} (w latach, np. 0 = dziś):", key=f"tk_{i}", format="%.6f")
        wyplaty.append((ck, tk))

    st.header("🟡 Koszty dodatkowe (prowizje, opłaty, ubezpieczenie)")

    prowizja = st.number_input("Prowizja (jednorazowo, zł):", min_value=0.0, step=0.01, format="%.2f")
    oplata_przygotowawcza = st.number_input("Opłata przygotowawcza (jednorazowo, zł):", min_value=0.0, step=0.01, format="%.2f")
    koszt_miesieczny = st.number_input("Koszt cykliczny (np. ubezpieczenie miesięczne, zł):", min_value=0.0, step=0.01, format="%.2f")

    st.header("🟢 Dane o spłatach kredytu (ratach)")

    rata_stala = st.number_input("Wysokość stałej raty (zł):", min_value=0.0, step=0.01, format="%.2f")
    liczba_rat_stalych = st.number_input("Liczba stałych rat:", min_value=0, step=1)
    rata_ostatnia = st.number_input("Wysokość ostatniej raty (wyrównawczej, zł):", min_value=0.0, step=0.01, format="%.2f")

    splaty = []

    # Dodaj prowizję i opłatę przygotowawczą jako natychmiastowe spłaty (czas = 0)
    if prowizja > 0:
        splaty.append((prowizja, 0))
    if oplata_przygotowawcza > 0:
        splaty.append((oplata_przygotowawcza, 0))

    # Dodajemy stałe raty + koszty miesięczne
    for i in range(int(liczba_rat_stalych)):
        czas = (i + 1) / 12
        kwota_raty = rata_stala + koszt_miesieczny
        splaty.append((kwota_raty, czas))

    # Dodajemy ostatnią ratę + koszt miesięczny
    czas_ostatniej_raty = (liczba_rat_stalych + 1) / 12
    splaty.append((rata_ostatnia + koszt_miesieczny, czas_ostatniej_raty))

    if st.button("Oblicz RRSO"):
        rrso = oblicz_rrso(wyplaty, splaty)
        if rrso is not None:
            st.success(f"🎯 Rzeczywista Roczna Stopa Oprocentowania (RRSO) wynosi: {rrso}%")
        else:
            st.error("❌ Nie udało się obliczyć RRSO. Sprawdź poprawność danych!")

if __name__ == "__main__":
    main()
