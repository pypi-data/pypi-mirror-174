from dataclasses import asdict, dataclass
from email.mime.base import MIMEBase
from typing import Any, Dict, Optional, Sequence

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@dataclass
class EmailContext:
    """
    Template context for the `Email` object
    """

    title: str = ""
    subtitle: str = ""
    body: str = ""
    preview: str = ""
    branding: str = ""


class Email(EmailMessage):
    """
    Base email object
    """

    content_subtype = "html"
    template_name = "libemail/generic.html"

    def __init__(
        self,
        subject: str = "",
        context: EmailContext = None,
        template_name: Optional[str] = None,
        from_email: Optional[str] = None,
        to: Optional[Sequence[str]] = None,
        bcc: Optional[Sequence[str]] = None,
        connection: Optional[Any] = None,
        attachments: Optional[Sequence[MIMEBase]] = None,
        headers: Optional[Dict[str, str]] = None,
        cc: Optional[Sequence[str]] = None,
        reply_to: Optional[Sequence[str]] = None,
    ) -> None:

        template_name = template_name if template_name else self.template_name
        body = render_to_string(template_name, asdict(context))

        from_email = from_email if from_email else self.__get_from_email__()
        to = to if isinstance(to, list) else [to]
        super().__init__(subject, body, from_email, to, bcc, connection, attachments, headers, cc, reply_to)

    def __get_from_email__() -> str:
        if hasattr(settings, "DEFAULT_FROM_EMAIL"):
            return settings.DEFAULT_FROM_EMAIL
        elif hasattr(settings, "EMAIL_HOST_USER"):
            return settings.EMAIL_HOST_USER
