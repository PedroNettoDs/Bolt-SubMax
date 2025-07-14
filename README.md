
# SubMax — Plataforma de Gestão para Personal Trainers

**SubMax** é uma aplicação web desenvolvida em **Python 3.12** e **Django 5.2**, projetada para simplificar o gerenciamento diário de personal trainers, oferecendo cadastro de alunos, registro de avaliações físicas e agenda de eventos.

---

## 🔎 Funcionalidades Principais

- **Gestão de Alunos**
  - Cadastro, edição e exclusão de alunos
  - Dados pessoais, contato, informações médicas e estilo de vida
  - Lista pesquisável e paginada
  - Ficha individual com abas para Dados Pessoais, Avaliações e Treinos

- **Avaliações Físicas**
  - Registro de peso, massa muscular, percentual de gordura e observações
  - Histórico com as últimas 10 avaliações por aluno

- **Agenda de Eventos**
  - Criação e listagem de eventos (título, descrição, data)
  - Visualização em calendário com FullCalendar

---

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python 3.12+
- **Framework:** Django 5.2
- **Banco de Dados:** SQLite3 (desenvolvimento) — recomendado PostgreSQL/MySQL em produção
- **Frontend:**
  - HTML5
  - Bootstrap 5.3
  - Bootstrap Icons
- **Calendário:** FullCalendar
- **Outros:**
  - Django Templates
  - Estrutura modular com múltiplos apps (`Pages` e `submax_app`)

---

## 🛠️ Pré-requisitos

- Python 3.12+
- pip
- Git

---

## ⚙️ Instalação e Setup

1. **Clone o repositório:**

   ```bash
   git clone https://seu-repositorio.git
   cd attano-projeto-submax
   ```

2. **Crie e ative um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure variáveis de ambiente**  
   Renomeie `.env.example` para `.env` e configure conforme necessário:
   ```ini
   SECRET_KEY=suachavesecreta
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Aplique as migrações do banco de dados:**

   ```bash
   python manage.py migrate
   ```

6. **Crie um superusuário:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Colete arquivos estáticos:**

   ```bash
   python manage.py collectstatic
   ```

8. **Inicie o servidor de desenvolvimento:**

   ```bash
   python manage.py runserver
   ```

   Acesse `http://127.0.0.1:8000` no navegador.

---

## 📂 Organização do Projeto

```
/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── LICENSE
├── readme.md
├── Pages/         # App para páginas de login, dashboard e templates estáticos
├── submax/        # Configurações globais do projeto Django
├── submax_app/    # App principal: alunos, avaliações, eventos
├── static/        # Assets globais
├── templates/     # Views globais
└── .git/
```

- **Pages/** — páginas de login, dashboard e templates estáticos
- **submax_app/** — modelos, views e lógica de domínio (Aluno, Avaliação, Evento)
- **submax/** — configurações globais (`settings`, `urls`, `wsgi`, `asgi`)
- **static/** e **templates/** dentro de cada app — assets e views específicas

---

## 📝 Boas Práticas e Recomendações

- Mantenha **SECRET_KEY** e outras chaves fora do repositório usando variáveis de ambiente
- Use **PostgreSQL** ou **MySQL** em produção
- Ative `DEBUG=False` e defina `ALLOWED_HOSTS` para produção
- Utilize linters (flake8, isort) e formatters (black)
- Implemente testes automatizados (cobertura mínima de 80%)

---

## 🧪 Testes

Atualmente não há testes implementados. Para adicionar:

```bash
python manage.py test
```

Recomenda-se criar testes unitários para modelos e views críticas.

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**. Veja o arquivo [`LICENSE`](LICENSE) para detalhes.

---

Desenvolvido com ❤️ para personal trainers que buscam eficiência e praticidade.
