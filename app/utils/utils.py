""" Send Mail """

import logging
import logging.config

import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template
from typing import Dict

from app.config.settings import Settings

setting = Settings()

logging.config.dictConfig(setting.LOGGING_CONFIG)
logger = logging.getLogger("smtp")

FRONTEND_URL = setting.frontend_url
EMAIL_HOST = setting.email_host
EMAIL_PORT = setting.email_port
EMAIL_USERNAME = setting.email_username
EMAIL_PASSWORD = setting.email_password

class Utils:
    """class with severals utiliites"""

    def __init__(self, template_dir: str):
        self.template_dir = Path(template_dir)


    def get_template(self, template_name: str = "mail.html") -> Template:
        """Lee una plantilla HTML desde el directorio de templates"""
        template_path = self.template_dir / "groups" / template_name

        if not template_path.exists():
            raise FileNotFoundError(f"Template no encontrado: {template_name}")

        return Template(template_path.read_text(encoding='utf-8'))

    def send_email(
            self,
            email: str,
            template_name: str,
            template_data: Dict[str, str]
        ) -> None:
        """
        Send mail to user
        """

        # Configurar el mensaje
        message = MIMEMultipart()
        message["From"] = EMAIL_USERNAME
        message["To"] = email
        message["Subject"] = "Eklegein - nuevo grupo"

        # Obtener y rellenar la plantilla
        template = self.get_template(template_name)
        html_content = template.safe_substitute(template_data)

        # print(html_content)
        # Adjuntar el contenido HTML
        message.attach(MIMEText(html_content, 'html'))

        # input("MAIL")

        try:
            # Conectar al servidor SMTP
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
                server.send_message(message)

        except Exception as e:
            logger.error("Send mail error: %s", e)
