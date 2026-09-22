# Ferrox-Py-Auth

## 1. Overview (What does this do?)
The `ferrox-py-auth` module is a specialized extension for the Ferrox ecosystem that provides a comprehensive Identity & Access Management (IAM) suite. It delivers pre-built functionalities for managing user registrations, Single Sign-On (SSO), Role-Based Access Control (RBAC), and compliance with European data privacy laws (GDPR).

## 2. Philosophy (Why does it exist?)
Authentication and authorization are complex and highly sensitive domains. Re-implementing secure login flows, password hashing, SSO integration, and GDPR-compliant data deletion mechanisms for every new project is not only inefficient but heavily prone to critical security vulnerabilities. This module exists to provide a battle-tested, standardized "plug-and-play" identity solution that adheres to strict zero-trust principles.

## 3. Target Audience (Who is it for?)
This module is intended for backend engineers and security architects building Enterprise SaaS, financial platforms, or any consumer-facing application where data privacy (like GDPR compliance) and secure access controls are legal or operational requirements.

## 4. Architecture (How does it work?)
`ferrox-py-auth` plugs directly into the **7-Layer Onion Request Pipeline** of the core `ferrox-py` framework, specifically occupying Layers 3 (Threat Engine) and 4 (Auth Guards). It registers a set of domain Services (`AuthService`, `GdprService`) into the central IoC Container and exposes abstract Data Models (`User`, `UserIdentity`) that can be persisted via MongoDB or SQLAlchemy adapters provided by the `ferrox-py` Data Component.

## 5. Installation / Setup
This package requires the core `ferrox-py` framework to function. Install it via pip:

```bash
pip install ferrox-py-auth
```
Ensure you have configured a persistent database layer (either SQL or NoSQL) in your core application to store the user identities.

## 6. Quickstart (Usage)
```python
from ferrox_py.core.app import FerroxApp
from ferrox_py.core.container import Container
from ferrox_py_auth import AuthModule

# Initialize the IoC container
container = Container()

# The AuthModule automatically registers the AuthService, GdprService, 
# and Auth Guards into the container and application lifecycle.
container.register_module(AuthModule)

app = FerroxApp(container)
app.start()
```

## 7. Ecosystem Integration
This module relies heavily on the **Security** component of the core `ferrox-py` framework for generating and parsing PASETO/JWT tokens. It also serves as a foundational dependency for `ferrox-py-commerce`, as a validated User context is required before initiating billing or subscription processes.
