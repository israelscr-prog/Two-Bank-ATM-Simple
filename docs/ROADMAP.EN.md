# ROADMAP — Two-Bank-ATM-Simple

> 🌐 [Leer en Español](./ROADMAP.md)

Planned features ordered by priority.

---

## ✅ Completed

- [x] Layered architecture (Domain, Application, Infrastructure, Presentation)
- [x] Domain entities (Account, Card, Transaction)
- [x] Domain exceptions
- [x] In-memory repositories
- [x] Use cases: balance, withdraw, deposit, change_pin, mini_statement
- [x] Full CLI
- [x] GUI with CustomTkinter
- [x] SQLite persistence
- [x] GitHub Actions CI pipeline
- [x] Full test suite — 94 tests, 0 failures
- [x] Automatic card lockout after 3 failed attempts

---

## 🔜 Next

- [ ] Transfers between accounts
- [ ] Admin panel (create accounts, block cards)
- [ ] Visual transaction history in the GUI

---

## 💡 Future

- [ ] Multi-currency support
- [ ] Export statement as PDF
- [ ] REST API layer
- [ ] Docker support
