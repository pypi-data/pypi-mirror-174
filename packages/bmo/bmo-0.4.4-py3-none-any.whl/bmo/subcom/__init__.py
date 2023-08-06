__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"


import logging

from datetime import datetime
from pathlib import Path

from envelopes import Envelope

import bmo.common
import bmo.helpers.notion

import typer

app = typer.Typer()


@app.command()
def send_email(
    to: str = typer.Option(...),
    config: str = typer.Option(..., callback=bmo.common.conf_callback, is_eager=True),
    smtp_server: str = typer.Option(...),
    smtp_port: int = typer.Option(...),
    smtp_username: str = typer.Option(...),
    smtp_password: str = typer.Option(...),
    subject: str = typer.Option(...),
    body: str = typer.Option(...),
):
    """Send email to a given user"""
    bmo.common.send_email_smtp(
        f"smtps://{smtp_username}:{smtp_password}@{smtp_server}:{smtp_port}",
        to=to,
        subject=subject,
        html=body,
    )


@app.command()
def weekly_email(
    to: str = typer.Option(...),
    config: str = typer.Option(..., callback=bmo.common.conf_callback, is_eager=True),
    notion_token: str = typer.Option(...),
    smtp_server: str = typer.Option(...),
    smtp_port: int = typer.Option(...),
    smtp_username: str = typer.Option(...),
    smtp_password: str = typer.Option(...),
    force: bool = typer.Option(False, "--force"),
):
    """This week in SubCom delivered to your INBOX."""
    if not notion_token:
        logging.error("Empty token. Add `--help` to usage.")
        return

    if datetime.today().weekday() != 0 and not force:
        logging.warning("Totay is not Monday. Use `--force` to override.")
        return

    notion = bmo.helpers.notion.Notion(notion_token)

    html = """<p>Greetings, puny Humans! I am <a
    href='https://github.com/SubconsciousCompute/bmo'>Subconscious BMO</a>.  I
    automate stuff. I found the following content that occurred at SubCom last
    week. Missing something? Let <a
    href='webmaster@subcom.tech'>webmaster@subcom.tech</a> know!</p>"""

    html += notion.weekly_update()
    html += "<p>-- <br /> 🎔 Subconscious BMO</p>"

    logging.info(html)

    # create an email and send it. Don't send duplicates.
    emaildir = Path.home() / ".cache" / "bmo"
    h = bmo.common.hash256(html.encode())
    hfile = emaildir / h
    if hfile.is_file() and not force:
        logging.warn("Email already sent.")
        return

    sender_email = smtp_username
    assert sender_email
    weekno = datetime.today().isocalendar()[1]
    subject = f"SubCom Weekly #{weekno}"

    send_email(
        to,
        config,
        smtp_server,
        smtp_port,
        smtp_username,
        smtp_password,
        subject=subject,
        body=html,
    )
    # write the hash to disk.
    hfile.parent.mkdir(parents=True, exist_ok=True)
    hfile.write_text(h)


if __name__ == "__main__":
    app()
