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
        tk = st.number_input(f"Czas wypłaty nr {i+1} (w latach):", key=f"tk_{i}", format="%.6f")
        wyplaty.append((ck, tk))

    st.header("Dane o spłatach/opłatach")
    m_prim = st.number_input("Podaj liczbę spłat/opłat:", min_value=1, step=1)

    splaty = []
    for i in range(int(m_prim)):
        st.subheader(f"Spłata/Opłata nr {i+1}")
        dl = st.number_input(f"Kwota spłaty/opłaty nr {i+1}:", key=f"dl_{i}")
        sl = st.number_input(f"Czas spłaty/opłaty nr {i+1} (w latach):", key=f"sl_{i}", format="%.6f")
        splaty.append((dl, sl))

    if st.button("Oblicz RRSO"):
        rrso = oblicz_rrso(wyplaty, splaty)
        if rrso is not None:
            st.success(f"Rzeczywista Roczna Stopa Oprocentowania (RRSO) wynosi: {rrso}%")
        else:
            st.error("Nie udało się obliczyć RRSO. Sprawdź wprowadzone dane.")

if __name__ == "__main__":
    main()
