# Ferrox-Py-Auth Overview

Il pacchetto `ferrox-py-auth` si occupa della gestione dell'Identità, del Controllo degli Accessi (IAM) e della conformità privacy (GDPR).

## Architettura IAM
In sistemi distribuiti e SaaS complessi, l'autenticazione non è una singola tabella "Users". Deve supportare l'estensione dinamica tramite Single Sign-On (Google, Apple, Microsoft) e mantenere un'architettura dati disaccoppiata.

Questo modulo si aggancia al livello 3 e 4 della `Onion Request Pipeline` di `ferrox-py` fornendo l'implementazione pratica della validazione e della persistenza degli utenti.

## Funzionalità Integrate
- Gestione di utenti multipli con Single Sign-On (SSO) collegati alla stessa entità.
- Controllo granulare degli accessi (RBAC).
- Strumenti pronti per la conformità GDPR, come il diritto all'oblio (Cancellazione) e la portabilità dei dati.
