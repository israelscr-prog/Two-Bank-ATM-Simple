# ROADMAP — TWO Bank ATM Simple

> 🌐 [Read in English](./ROADMAP.EN.md)

Funcionalidades planificadas ordenadas por prioridad.

---

## ✅ Completado

- [x] Estructura de capas (Domain, Application, Infrastructure, Presentation)
- [x] Entidades del dominio (Account, Card, Transaction)
- [x] Excepciones del dominio
- [x] Repositorios en memoria
- [x] Use cases: balance, withdraw, deposit, change_pin, mini_statement
- [x] CLI completo
- [x] GUI con CustomTkinter

---

## 🔜 Próximo

- [ ] Tests con pytest (test_entities, test_repositories, test_session)
- [ ] Transferencias entre cuentas
- [ ] Bloqueo de tarjeta tras 3 intentos fallidos

---

## 💡 Futuro

- [ ] Persistencia con SQLite
- [ ] Admin panel (crear cuentas, bloquear tarjetas)
- [ ] Historial visual de transacciones en la GUI
- [ ] Soporte multi-moneda