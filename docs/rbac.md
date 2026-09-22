# RBAC (Role-Based Access Control)

Il Controllo degli Accessi è implementato tramite il decoratore `@require_roles`.

## Architettura e Pipeline
Quando un endpoint HTTP o gRPC viene chiamato, il token (JWT o PASETO) è stato validato al Livello 3 della Onion Request Pipeline. Il payload del token contiene i "claims" dell'utente, inclusa la lista di `roles`.

Il decoratore di livello 4 intercetta la chiamata *prima* di eseguire il controller.

```python
from ferrox_py_auth.security.rbac import require_roles

class AdminController:
    
    @require_roles("superadmin", "editor")
    async def delete_article(self, request, article_id):
        # L'esecuzione arriva qui solo se il token ha il ruolo corrispondente
        pass
```

### Configurazione
Il decoratore controlla nativamente lo scope di esecuzione. L'implementazione base solleva un `ForbiddenError` (HTTP 403) se il ruolo non è presente nei claims del context locale associato al token.
