# Projekt ZTT - Symulacja systemu transmisji TCM

Symulacja systemu transmisji TCM (Trellis Coded Modulation) z wykorzystaniem algorytmu Viterbiego. Celem projektu jest zdekodowanie wiadomości zakodowanej koderem splotowym poprzez obliczenie dystansu zmodulowanych słów kodowych od punktów konstelacji 8-PSK.

## Funkcje i ustawienia

- **Moc transmisji**: Możliwość zmiany mocy transmisji w symulacji.
- **Moc szumu**: Możliwość dostosowania SNR w symulacji.
- **Kodowanie Gray'a**: Wybór opcji kodowania Gray'a dla słów kodowych.
- **Długość ramki**: Możliwość zmiany długości ramki transmisji.
- **Limit błędów**: Ustawienie maksymalnej liczby błędów, które mogą być wykryte w trakcie dekodowania.
- **Liczba iteracji**: Możliwość określenia liczby iteracji dekodowania.

## Pliki projektu

- **channel.py**: Zawiera funkcję dodającą szum do sygnału.
- **coder.py**: Zawiera funkcję realizującą kodowanie splotowe.
- **decoder.py**: Zawiera implementację algorytmu Viterbiego.
- **demodulation.py**: Zawiera funkcję obliczającą odległość punktów obserwowanych od punktów - konstelacji 8-PSK.
- **framegen.py**: Generuje losowe ramki do symulacji.
- **gray.py**: Zawiera funkcje do przekształcania na kod Graya i spowrotem.
- **modulation.py**: Zawiera funkcje modulujące słowa kodowe na punkty na konstelacji 8-PSK.
- **setup.py**: Zawiera wszystkie dostępne ustawienia i konfiguracje.
- **gui.py**: Główny plik, który łączy, uruchamia i wyświetla całą symulację.

## Uruchamianie symulacji

Aby uruchomić symulację, wykonaj następujące kroki:

1. Sklonuj repozytorium na komputer.
2. Zainstaluj wymagane zależności, uruchamiając w terminalu lub wierszu poleceń **'pip install numpy matplotlib pysimplegui'** .
3. Skonfiguruj preferowane ustawienia w pliku **'setup.py'**.
4. Uruchom symulację, wykonując **'python main.py'**.

## Wyniki i wykresy

Po zakończeniu symulacji wyniki zostaną wyświetlone na ekranie. Opcjonalnie można zdecydować, czy wyświetlić punkty z ostatniej ramki na wykresie oraz czy wyświetlić dane debugowania w terminalu.

Autorzy: Maciej Niedźwiecki, Piotr Skrzypczak, Marcin Wachowski
