# GdprService

Ogni framework SaaS moderno in Europa e California deve aderire alle stringenti normative sulla privacy. Il `GdprService` astrae i comandi complessi per conformarsi.

## 1. Diritto all'Oblio (Cancellazione)
Invece di lasciare ai developer il compito di eseguire cascate di cancellazioni pericolose, `delete_user_data` maschera o elimina in modo sicuro il PII (Personally Identifiable Information).

```python
from ferrox_py_auth.services.gdpr_service import GdprService

# Soft delete o hard delete
await gdpr_service.delete_user_data(user_id="user_123")
```

## 2. Portabilità dei Dati
Fornisce un dump completo e leggibile in JSON (o CSV) dello stato utente e delle preferenze collegate, pronto per essere inviato via mail o scaricato dall'utente come pacchetto `.zip`.

```python
dump = await gdpr_service.export_user_data(user_id="user_123")
# { "email": "...", "identities": [...], "created_at": "..." }
```
