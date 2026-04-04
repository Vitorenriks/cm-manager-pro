# 🏗️ CM Manager Pro - Construction Management MicroSaaS

> 🚀 **Acesse o Projeto:** [https://cm-manager-pro.onrender.com](https://cm-manager-pro.onrender.com)

## 🔑 Acesso para Testes (Modo Demonstração)

Para facilitar a exploração das funcionalidades do sistema, utilize as credenciais abaixo:

| Usuário | Senha |
| :--- | :--- |
| `admin` | `1234` |

> **Nota:** O sistema está operando em modo de demonstração para preservação da integridade dos dados.

---

## 📸 Screenshots

### Login Page
![Login Screen](screenshots/login.png)

### Main Dashboard
![Dashboard Screen](screenshots/dashboard.png)

---

## 🇧🇷 Sobre o Projeto
O **CM Manager Pro** é uma plataforma de gestão de obras projetada para trazer eficiência e controle para pequenas e médias construtoras. O sistema centraliza o gerenciamento de projetos, permitindo o acompanhamento em tempo real de status, custos e cronogramas através de uma interface intuitiva e segura.

## ✨ Principais Funcionalidades / Key Features

* **Dashboard Interativo:** Visão geral de todos os projetos ativos com indicadores visuais de status.
* **Gestão Completa (CRUD):** Fluxo total de criação, leitura, edição e exclusão de obras com persistência de dados.
* **Foco em UX (User Experience):** Interface densa e otimizada com escala visual reduzida para evitar rolagens desnecessárias, priorizando a produtividade.
* **Mobile Optimized (Android/iOS):** Template e UX aprimorados especificamente para dispositivos móveis, garantindo agilidade no uso em campo.
* **Sistema Multiusuário:** Autenticação robusta onde cada gestor possui seu próprio ambiente isolado e seguro.

### 🛠️ Diferenciais Técnicos:
- **Banco de Dados de Produção:** Migração concluída de SQLite para **PostgreSQL** (via Render), garantindo maior escalabilidade, concorrência e segurança dos dados.
- **Arquitetura Segura:** Autenticação via `Flask-Login` com proteção de rotas e gestão de sessões.
- **Criptografia Avançada:** Armazenamento de credenciais utilizando hashes `PBKDF2-SHA256`.
- **Interface Pro:** UX focada em produtividade, desenvolvida com Bootstrap 5 e CSS personalizado para um design Clean/SaaS.

---

## 🇺🇸 About the Project
**CM Manager Pro** is a construction management MicroSaaS built to streamline workflows for small to medium-sized construction firms.

### 🛠️ Technical Highlights:
- **Production Database:** Powered by **PostgreSQL** for high availability and data consistency.
- **Mobile-First UX:** Enhanced templates optimized for **Android/iOS** devices, perfect for on-site management.
- **Secure Auth:** Industry-standard password hashing and session management.

---

## 🚀 Tech Stack
- **Backend:** Python 3.x / Flask
- **Database:** **PostgreSQL** (Production) / SQLAlchemy (ORM)
- **Frontend:** HTML5, CSS3 (Modern UI), Bootstrap 5, Jinja2
- **Security:** Werkzeug Security / Flask-Login
- **Deployment:** Gunicorn / Render

---

## Instalação e Execução / Setup

1. **Clone & Folder:**
   ```bash
   git clone https://github.com/Vitorenriks/cm-manager-pro.git
   cd cm-manager-pro
   ```

2. **Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch:**
   ```bash
   python setup_db.py
   flask run
   ```

---

## 👤 Author

**Vitor Henriques** - *Aspiring Software Engineer*

> "Building software that builds the world."

linkedin : https://linkedin.com/in/vitor-henriques-86a37b2a4
