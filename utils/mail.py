import smtplib
from email.mime.text import MIMEText
from .algorythms import recursive_keyval

import os

def style_mail(title, track_obj):
    table_rows = ''
    for item in recursive_keyval(track_obj).items():
        table_rows += """
        <tr>
            <td style='border: 1px solid black;'>{key}</td>
            <td style='border: 1px solid black;'>{val}</td>
        </tr>
        """.format(key=item[0], val=item[1])

    content = """
    <table style='width: 100%;' />
    <h1>{title}</h1>
    <table>
        <tr >
            <th style='border: 1px solid black;'><h3>Clave</h3></th>
            <th style='border: 1px solid black;'><h3>Valor</h3></th>
        </tr>
        <tr>
        {table}
        </tr>
    </table>
    """.format(title=title, table=table_rows)

    return content

def send_mail(from_email,
              to_email,
              subject,
              content,
              receiver_name='',
              cc_email='',
              cc_name=''):
    message = MIMEText(content, 'html')

    message['From'] = from_email
    message['To'] = '{} <{}>'.format(receiver_name, to_email)
    message['Cc'] = '{} <{}>'.format(cc_name, cc_email)
    message['Subject'] = subject

    msg_full = message.as_string()

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(os.getenv('EMAIL_USER', ''), os.getenv('EMAIL_PASSWORD', ''))
    server.sendmail(from_email,
                    [to_email, cc_email],
                    msg_full)
    server.quit()
