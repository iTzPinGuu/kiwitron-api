🚀 Sistema di Invio Messaggi Automatici 💬✨
===========================================

Il codice che hai condiviso è un programma smart ✨ che invia automaticamente messaggi predefiniti a intervalli casuali 🚦, pensando a tutte le pause e gli orari di chiusura 🕒. È come avere un assistente digitale 🧑‍💻 che lavora senza mai stancarsi!

* * * * *

🎯 Obiettivo
------------

Automatizzare l'invio di messaggi durante l'orario di lavoro 📋, rispettando pause pranzo 🍽️ e orari di chiusura ⛔.

* * * * *

🔑 Componenti Chiave
--------------------

1\. Configurazione e Orari di Lavoro 🕰️
----------------------------------------

-   Pause pranzo: dalle 12:30 alle 13:36
-   Chiusura: alle 17:50
-   Fuso orario: Italia 🇮🇹 (pytz).

2\. Autenticazione con API 🔑
-----------------------------

-   Login tramite API `https://my.kiwitron.tech/api_v1/login`
-   Ottieni un token di sessione 🛡️ per le richieste successive
-   Gestisci errori come se fosse un gioco 🕹️

3\. Generazione di Messaggi 🎲
------------------------------

-   Scarico: `"Scarica {numero} su area {area}"` -- con numeri 1-15, area scelta con peso 💪
-   Carico Cassoni: `"Carica un cassone per mat area {area}"` -- casualmente inseriti nella sequenza 🚧

4\. Invio dei Messaggi 📤
-------------------------

-   Usa l'endpoint `/api_v2/hmi`
-   Massimo 3 tentativi per non perdere nulla 🚀
-   Ricrea il token se scade 🔄

5\. Gestione del Tempo ⏳
------------------------

-   Controlla se è pausa o orario di terminare 🔍
-   Attende prima di proporre il prossimo messaggio, tra 29 e 55 minuti 🗓️
-   Pausa automatica se è ora di pranzo 🥗

* * * * *

🔄 Come Funziona il Loop Principale
-----------------------------------

-   Login al sistema kiwitron ✅
-   Prepara 15 messaggi di scarico + 10 messaggi di cassone in modo casuale 🎰
-   Inizia il ciclo infinito:
    -   Verifica se è ora di terminare (ultima ora del giorno) ⏰
    -   Controlla se è pausa pranzo: se sì, aspetta fino alla fine 💤
    -   Invia il messaggio attuale ✅
    -   Rotazione dei messaggi per variarne l'ordine🔄
    -   Attende tra 29 e 55 minuti con un sistema di controllo continuo ⌛

* * * * *

🌟 Punti di Forza
-----------------

-   Resilienza: retries automatici e ri-autenticazioni 💪
-   Distribuzione intelligente: aree più motivate (tipo 10b) e inserimenti casuali 🎯
-   Preciso timing: rispetto puntuale di pause e orari di chiusura 🕒
-   Automazione totale: senza intervento manuale, anche durante le pause e le convalide 🚀

* * * * *

🛠️ Integrazione API
--------------------

-   Login: `POST /api_v1/login` 🔐
-   Messaggi: `POST /api_v2/hmi` con i payload `assetId`, `message` e `deliveryType` 📩

* * * * *

📝 Esempio di Output
--------------------

text

`✅ Login avvenuto con successo! 💬 Scarica 1 su area 10b ⏳ Attesa di 42 minuti prima del prossimo invio... 🔄 Prossimo messaggio tra 41 minuti... 🛑 Ora di terminare: chiusura giornata! `

* * * * *

🎉 Il Bello?
------------

Questo sistema mantiene tutto sotto controllo, rispettando tempi e pause, lasciando che il tuo lavoro fluisca senza stress! È come un assistente invisibile, affidabile e sempre presente! 💼🤖
