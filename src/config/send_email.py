import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import socks

load_dotenv()

#Função responsável em pegar o ultimo log processado
def get_latest_log_file(log_dir):
    files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))]
    if not files:
        return None
    latest_file = max(files, key=os.path.getctime)
    return latest_file

#Essa função está configurando o proxy e o smtp para envio de emails
def enviar_email(subject, body, emails, attachment_path):
    proxy_host = os.getenv('PROXY_IP')
    proxy_port = int(os.getenv('PROXY_PORT'))
    proxy_user = os.getenv('PROXY_USERNAME')
    proxy_password = os.getenv('PROXY_PASSWORD')
    
    socks.set_default_proxy(socks.HTTP, proxy_host, proxy_port, True, proxy_user, proxy_password)
    socks.wrapmodule(smtplib)
    #Importando váriaveis de ambiente
    smtp_server = os.getenv('smtp_server')
    email_from = os.getenv('email_from')
    pswd = os.getenv('senha')
    port = int(os.getenv('porta'))

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = ', '.join(emails)
    msg.set_content(body)

    #Verifica o ultimo arquivo de log e caso ele exista, envie ele
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Iniciar TLS
            server.login(email_from, pswd)
            server.send_message(msg)
            print("Email enviado com sucesso!")
    except smtplib.SMTPServerDisconnected as e:
        print("Conexão encerrada inesperadamente:", e)
    except smtplib.SMTPAuthenticationError as e:
        print("Erro de autenticação SMTP:", e)
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
