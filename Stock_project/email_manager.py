from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.base import MIMEBase
from email import encoders
from os.path import basename

import smtplib

email_config = {}
with open('email_config', 'r') as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.strip().split('=')
        email_config[key] = value
SMTP_SERVER = email_config['smtp_server']
SMTP_PORT = email_config['smtp_port']
SMTP_USER = email_config['smtp_user']
SMTP_PASSWORD = email_config['smtp_password']
        
def send_email(from_user:str, to_users:list, subject:str, contents:str, attachments:list=[], cc_targets=[]) ->bool:
    '''
    * 필수항목
    from_user: 보내는 사람의 메일주소
    to_users: 받는 사람의 메일주소(list)
    subject: 메일제목
    contents: 메일내용

    *선택항목
    attachments: 첨부파일 경로(list)
    cc_targets: 참조자 메일주소(list)
    '''

    try:
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp.login(SMTP_USER, SMTP_PASSWORD)

        if attachments:
            msg = MIMEMultipart('alternative')
        else:
            msg = MIMEMultipart('mixed')

        for attachment in attachments:
            email_file = MIMEBase('application', 'octet-stream')
            with open(attachment, 'rb') as f:
                file_data = f.read()
            email_file.set_payload(file_data)
            encoders.encode_base64(email_file)
            file_name = basename(attachment)
            email_file.add_header('Content_Disposition', 'attachment', filename = file_name)
            msg.attach(email_file)

        msg['From'] = from_user
        msg['To'] = ','.join(set(to_users))
        if cc_targets:
            msg['CC'] = ','.join(cc_targets)
        msg['Subject'] = subject

        text = MIMEText(contents)
        msg.attach(text)

        smtp.sendmail(from_user, set(to_users+cc_targets), msg.as_string())
        
        return True

    except Exception as e:
        print(e)

    finally:
        smtp.close()

    return False