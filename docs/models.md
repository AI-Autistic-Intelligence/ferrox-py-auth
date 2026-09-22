# Models (Pydantic / Mongo)

Il modulo esporta i modelli base dell'utente validati staticamente tramite Pydantic. 
Questi modelli sono pensati per essere salvati (serializzati/deserializzati) nativamente su MongoDB o convertiti per SQLAlchemy.

## UserIdentity
Il sotto-documento che descrive un'identità esterna.
- `provider`: "google", "apple", "facebook", "local"
- `provider_id`: Identificatore alfanumerico fornito dall'IdP.
- `last_login`: Timestamp.

## User
Il modello aggregato principale.
- Contiene l'email principale.
- Gestisce i flag booleani come `is_email_verified` e `is_active`.
- `identities`: Lista di oggetti `UserIdentity` (Array in Mongo).
- `roles`: Lista di stringhe che definiscono i permessi per il modulo RBAC.
