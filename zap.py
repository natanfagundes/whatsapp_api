import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pywhatkit
import time

SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("people", "v1", credentials=creds)
        contacts = []
        next_page_token = None
        while True:
            results = service.people().connections().list(
                resourceName="people/me",
                pageSize=1000,  # Máximo recomendado por chamada (até 2000)
                personFields="names,phoneNumbers",
                pageToken=next_page_token
            ).execute()
            
            connections = results.get("connections", [])
            for person in connections:
                name = person.get("names", [{}])[0].get("displayName", "Sem nome")
                phones = person.get("phoneNumbers", [])
                phone_list = [phone.get("value", "").strip() for phone in phones if phone.get("value")]
                if phone_list:
                    contacts.append({"name": name, "phones": phone_list})
            
            next_page_token = results.get("nextPageToken")
            if not next_page_token:
                break

        # Exibir contatos
        for contact in contacts:
            print(f"Nome: {contact['name']}, Telefones: {contact['phones']}")

        # Enviar mensagens (opcional)
        message = "Olá! Esta é uma mensagem de teste enviada automaticamente."
        for contact in contacts:
            for phone in contact["phones"]:
                formatted_phone = phone if phone.startswith('+') else f"+55{phone.replace(' ', '').replace('-', '')}"
                try:
                    pywhatkit.sendwhatmsg_instantly(formatted_phone, message)
                    print(f"Mensagem enviada para {contact['name']} ({formatted_phone})")
                    time.sleep(10)  # Pausa para evitar bloqueio
                except Exception as e:
                    print(f"Erro ao enviar para {formatted_phone}: {e}")

    except HttpError as err:
        print(f"Erro na API: {err}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
