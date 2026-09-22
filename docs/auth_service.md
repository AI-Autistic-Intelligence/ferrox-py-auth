# AuthService (Autenticazione & SSO)

Il modulo esporta l'`AuthService`, un servizio singleton registrato nell'IoC container di Ferrox.

## Registrazione Standard
Permette di registrare un utente e avviare il processo di "Double Opt-In" (Mail di conferma) tipico delle applicazioni sicure. L'utente non può accedere finché la mail non è confermata.

## Integrazione Single Sign-On (SSO)
Supporta il login o la registrazione via OIDC/OAuth2. L'identità (Es. un ID di Google) viene salvata in un sub-documento `identities` associato allo user.
Se l'accesso avviene via SSO, lo stato "email confermata" viene ereditato dal provider, scavalcando la necessità di inviare la mail di opt-in.

```python
from ferrox_py_auth.services.auth_service import AuthService

# Registrazione via SSO (Bypass Email Validation)
user = await auth_service.register_via_sso(
    email="test@gmail.com",
    provider="google",
    provider_id="1010101010101"
)
```
