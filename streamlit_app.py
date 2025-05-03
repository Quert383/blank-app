import streamlit as st
from scipy.optimize import newton

def oblicz_rrso(wyplaty, splaty):
    def funkcja(X):
        lewa = sum(ck / (1 + X)**tk for ck, tk in wyplaty)
        prawa = sum(dl / (1 + X)**sl for dl, sl in splaty)
        return lewa - prawa

    X0 = 0.05  # początkowe przybliżenie (5%)
    try:
        wynik = newton(funkcja, X0)
        return round(wynik * 100, 1)  # przeliczenie na procenty
    except RuntimeError:
        return None

def main():
    st.title("Obliczanie Rzeczywistej Rocznej Stopy Oprocentowania (RRSO)")

    st.header("Dane o wypłatach")
    m = st.number_input("Podaj liczbę wypłat:", min_value=1, step=1)

    wyplaty = []
    for i in range(int(m)):
        st.subheader(f"Wypłata nr {i+1}")
        ck = st.number_input(f"Kwota wypłaty nr {i+1}:", key=f"ck_{i}")
        tk = st.number_input(f"Czas wypłaty nr {i+1} (w latach, np. 0 dla wypłaty dzisiaj):", key=f"tk_{i}", format="%.6f")
        wyplaty.append((ck, tk))

    st.header("Dane o ratach")

    rata_stala = st.number_input("Podaj wysokość stałej raty (zł):", min_value=0.0, step=0.01, format="%.2f")
    liczba_rat_stalych = st.number_input("Podaj liczbę stałych rat:", min_value=0, step=1)
    rata_ostatnia = st.number_input("Podaj wysokość ostatniej raty (wyrównawczej):", min_value=0.0, step=0.01, format="%.2f")

    splaty = []
    # Dodajemy stałe raty co miesiąc
    for i in range(int(liczba_rat_stalych)):
        czas = (i + 1) / 12  # pierwszy miesiąc = 1/12 roku, potem 2/12 itd.
        splaty.append((rata_stala, czas))

    # Dodajemy ostatnią ratę
    czas_ostatniej_raty = (liczba_rat_stalych + 1) / 12  # kolejny miesiąc po stałych ratach
    splaty.append((rata_ostatnia, czas_ostatniej_raty))

    if st.button("Oblicz RRSO"):
        rrso = oblicz_rrso(wyplaty, splaty)
        if rrso is not None:
            st.success(f"Rzeczywista Roczna Stopa Oprocentowania (RRSO) wynosi: {rrso}%")
        else:
            st.error("Nie udało się obliczyć RRSO. Sprawdź wprowadzone dane.")

if __name__ == "__main__":
    main()
