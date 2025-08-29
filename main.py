import requests
import random
import time
from datetime import datetime
import pytz

# Costanti per la configurazione manuale
INIZIO_PAUSA_PRANZO = "12:30"       # Formato HH:MM
FINE_PAUSA_PRANZO = "13:36"         # Formato HH:MM
CHIUSURA_GIORNATA = "17:50"         # Formato HH:MM

# Credenziali (Inserisci direttamente le tue credenziali qui)
USERNAME = "xxxxx"
PASSWORD = "xxxxx"
ASSET_ID = 2622
AREAS = ['15', '16', '17', '18', '19', '10b', '3a', '4', '5']

# Fuso orario Italiano
ITALY_TZ = pytz.timezone('Europe/Rome')

# Funzione per generare una frase casuale
def genera_frase(numero):
    numero_corretto = (numero - 1) % 15 + 1
    area_weights = [0.13, 0.13, 0.13, 0.13, 0.13, 0.18, 0.05, 0.05, 0.05]  # Pesi per le nuove aree
    area = random.choices(AREAS, weights=area_weights, k=1)[0]
    return f"Scarica {numero_corretto} su area {area}"

# Funzione per effettuare il login e ottenere il token di sessione
def login(session):
    url_login = "https://my.kiwitron.tech/api_v1/login"
    headers_login = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    data_login = {
        "username": USERNAME,
        "password": PASSWORD
    }

    try:
        response = session.post(url_login, headers=headers_login, json=data_login)
        if response.status_code == 200:
            print("Login avvenuto con successo!")
            risposta = response.json()
            session_token = risposta.get("session")
            if session_token:
                # Aggiungi il token di sessione agli headers per le richieste successive
                session.headers.update({"Session": session_token})
                return True
            else:
                print("Token di sessione non trovato nella risposta del login.")
                return False
        else:
            print(f"Errore durante il login. Codice di stato: {response.status_code}")
            print(f"Messaggio di errore: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Eccezione durante il login: {e}")
        return False

# Funzione per inviare un messaggio con gestione degli errori
def invia_messaggio(session, frase, max_retry=3):
    url_hmi = "https://my.kiwitron.tech/api_v2/hmi"
    headers_hmi = {
        "Accept": "*/*",
        "Content-Type": "application/json",
    }
    data_hmi = {
        "assetId": ASSET_ID,
        "message": frase,
        "deliveryType": 1
    }

    tentativi = 0
    while tentativi < max_retry:
        try:
            response = session.post(url_hmi, headers=headers_hmi, json=data_hmi)
            if response.status_code == 200:
                print(f"Messaggio inviato con successo: {frase}")
                return True
            elif response.status_code == 401:
                print("Errore 401 Unauthorized. Tentativo di ri-autenticazione...")
                if login(session):
                    tentativi += 1
                else:
                    print("Re-autenticazione fallita.")
                    break
            else:
                print(f"Errore durante l'invio del messaggio. Codice di stato: {response.status_code}")
                print(f"Messaggio di errore: {response.text}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Eccezione durante l'invio del messaggio: {e}")
            break
    print("Massimo numero di tentativi raggiunto. Passando al prossimo messaggio.")
    return False

# Funzione per verificare l'intervallo di pausa
def è_pausa_corrente():
    ora_corrente = datetime.now(ITALY_TZ).time()
    inizio_pausa = datetime.strptime(INIZIO_PAUSA_PRANZO, "%H:%M").time()
    fine_pausa = datetime.strptime(FINE_PAUSA_PRANZO, "%H:%M").time()
    return inizio_pausa <= ora_corrente < fine_pausa

# Funzione per verificare se è ora di terminare il programma
def è_ora_di_terminare():
    ora_corrente = datetime.now(ITALY_TZ).time()
    termine = datetime.strptime(CHIUSURA_GIORNATA, "%H:%M").time()
    return ora_corrente >= termine

# Funzione principale
def main():
    # Crea una sessione persistente
    session = requests.Session()

    # Effettua il login
    if not login(session):
        print("Impossibile effettuare il login. Terminazione dello script.")
        return

    # Inizializza la lista di frasi
    frasi_totali = [genera_frase(numero) for numero in range(1, 16)]

    # Genera la lista di frasi per il cassone
    posizioni_cassone = random.sample(range(15), 10)
    for i, posizione in enumerate(posizioni_cassone):
        area_weights_cassone = [0.06, 0.06, 0.06, 0.06, 0.06]
        area_cassone = random.choices(['13', '15', '17', '19', '31'], weights=area_weights_cassone, k=1)[0]
        frase_cassone = f"Carica un cassone per mat area {area_cassone}"
        frasi_totali.insert(posizione + i, frase_cassone)

    # Inizializza un indice per iterare attraverso la lista di frasi
    indice_frase = 0

    while True:
        # Controlla se è l'ora di terminare il programma
        if è_ora_di_terminare():
            print("Ora di terminazione raggiunta. Chiusura del programma.")
            break

        # Controlla se è l'intervallo di pausa
        if è_pausa_corrente():
            print(f"Intervallo di pausa attivo ({INIZIO_PAUSA_PRANZO} - {FINE_PAUSA_PRANZO}). Attesa fino alla fine della pausa.")
            # Calcola il tempo rimanente fino alla fine della pausa
            ora_corrente = datetime.now(ITALY_TZ)
            fine_pausa = ora_corrente.replace(hour=int(FINE_PAUSA_PRANZO.split(":")[0]),
                                             minute=int(FINE_PAUSA_PRANZO.split(":")[1]),
                                             second=0, microsecond=0)
            tempo_rimanente = (fine_pausa - ora_corrente).total_seconds()
            if tempo_rimanente > 0:
                time.sleep(tempo_rimanente)
            continue

        # Invia la frase corrente
        invia_messaggio(session, frasi_totali[indice_frase])

        # Incrementa l'indice per passare alla prossima frase
        indice_frase = (indice_frase + 1) % len(frasi_totali)

        # Attendi un intervallo casuale tra 29 e 55 minuti prima del prossimo invio
        tempo_attesa = random.randint(29, 55)  # Intervallo iniziale
        print(f"Attesa di {tempo_attesa} minuti prima del prossimo invio...")

        # Ciclo per aggiornare il tempo di attesa ogni minuto fino al prossimo invio
        for _ in range(tempo_attesa):
            # Verifica se è l'ora di terminare durante l'attesa
            if è_ora_di_terminare():
                print("Ora di terminazione raggiunta durante l'attesa. Chiusura del programma.")
                return
            # Verifica se entra nell'intervallo di pausa durante l'attesa
            ora_corrente = datetime.now(ITALY_TZ).time()
            if datetime.strptime(INIZIO_PAUSA_PRANZO, "%H:%M").time() <= ora_corrente < datetime.strptime(FINE_PAUSA_PRANZO, "%H:%M").time():
                print(f"Intervallo di pausa attivo durante l'attesa ({INIZIO_PAUSA_PRANZO} - {FINE_PAUSA_PRANZO}). Attesa fino alla fine della pausa.")
                break
            print(f"Prossimo messaggio in arrivo tra {tempo_attesa} minuti...")
            time.sleep(60)  # Attendi un minuto
            tempo_attesa -= 1

if __name__ == "__main__":
    main()
