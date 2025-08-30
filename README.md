# 📲 Google Contacts + WhatsApp Automation

Este projeto integra a API do **Google People (Contacts)** com o **WhatsApp**, permitindo:
- Ler os contatos salvos na conta Google.
- Extrair nomes e números de telefone.
- Enviar mensagens automáticas pelo WhatsApp usando a biblioteca **pywhatkit**.

---

## 🚀 Funcionalidades
- Autenticação via OAuth2 com a API do Google.
- Coleta de até 2000 contatos por requisição.
- Normalização automática dos números (adiciona `+55` se não tiver DDI).
- Envio de mensagens automáticas pelo WhatsApp.

---

## 📦 Pré-requisitos
- **Python 3.8+**
- Conta Google (com contatos salvos).
- Navegador Google Chrome instalado (necessário para o pywhatkit).
- WhatsApp Web configurado no navegador.

---

## ⚙️ Instalação
Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
pip install -r requirements.txt
