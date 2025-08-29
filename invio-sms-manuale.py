import requests
import tkinter as tk
from tkinter import messagebox

# Credenziali (Inserisci direttamente le tue credenziali qui)
USERNAME = "xxxxx"
PASSWORD = "xxxxxx"
ASSET_ID = 2622

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
            risposta = response.json()
            session_token = risposta.get("session")
            if session_token:
                session.headers.update({"Session": session_token})
                return True
            else:
                messagebox.showerror("Errore", "Token di sessione non trovato.")
                return False
        else:
            messagebox.showerror("Errore", f"Errore durante il login: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Eccezione", f"Eccezione durante il login: {e}")
        return False

# Funzione per inviare un messaggio
def invia_messaggio(session, frase):
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

    try:
        response = session.post(url_hmi, headers=headers_hmi, json=data_hmi)
        if response.status_code == 200:
            messagebox.showinfo("Successo", f"Messaggio inviato con successo: {frase}")
            return True
        else:
            messagebox.showerror("Errore", f"Errore durante l'invio del messaggio: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Eccezione", f"Eccezione durante l'invio del messaggio: {e}")
        return False

# Funzione per gestire l'invio del messaggio dalla GUI
def invia_da_gui():
    frase = entry.get()
    if frase:
        if not login(session):
            messagebox.showerror("Errore", "Impossibile effettuare il login.")
            return
        invia_messaggio(session, frase)
    else:
        messagebox.showwarning("Attenzione", "Inserisci un messaggio prima di inviare.")

# Configurazione della GUI
root = tk.Tk()
root.title("Invia Messaggio")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Inserisci il tuo messaggio:")
label.pack(pady=5)

entry = tk.Entry(frame, width=50)
entry.pack(pady=5)

button_invia = tk.Button(frame, text="Invia", command=invia_da_gui)
button_invia.pack(pady=5)

# Crea una sessione persistente
session = requests.Session()

root.mainloop()
