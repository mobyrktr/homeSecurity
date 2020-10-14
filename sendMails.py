import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email.encoders import encode_base64
from getpass import getpass
from smtplib import SMTP

def get_email(email):
    if '<' in email:
        data = email.split('<')
        email = data[1].split('>')[0].strip()
    return email.strip()

class Email(object):
    def __init__(self, from_, to, subject, message, message_type='html',
                 attachments=None, cc=None, message_encoding='utf-8'):
        self.email = MIMEMultipart()
        self.email['From'] = from_
        self.email['To'] = to
        self.email['Subject'] = subject
        if cc is not None:
            self.email['Cc'] = cc
        text = MIMEText(message, message_type, message_encoding)
        self.email.attach(text)
        if attachments is not None:
            for filename in attachments:
                mimetype, encoding = guess_type(filename)
                mimetype = mimetype.split('/', 1)
                fp = open(filename, 'rb')
                attachment = MIMEBase(mimetype[0], mimetype[1])
                attachment.set_payload(fp.read())
                fp.close()
                encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment',
                                      filename=os.path.basename(filename))
                self.email.attach(attachment)

    def __str__(self):
        return self.email.as_string()


class EmailConnection(object):
    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = SMTP('smtp.gmail.com', 587)
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.ehlo()
        self.connection.login('sender@gmail.com','*********')

    def send(self, message, from_=None, to=None):
        if type(message) == str:
            if from_ is None or to is None:
                raise ValueError('You need to specify `from_` and `to`')
            else:
                from_ = get_email(from_)
                to = get_email(to)
        else:
            from_ = message.email['From']
            if 'Cc' not in message.email:
                message.email['Cc'] = ''
            to_emails = [message.email['To']] + message.email['Cc'].split(',')
            to = [get_email(complete_email) for complete_email in to_emails]
            message = str(message)
        return self.connection.sendmail(from_, to, message)

    def close(self):
        self.connection.close()

def sendMails(admins):
    #static variales
    for admin in admins:
        to_email = admin[0]
        to_name = admin[1]

        print("sending mail to: ", to_email)
        name = "MONUR Home Security Solutions®"
        from_email = "###"
        password = "###"
        mail_server = "smtp.gmail.com" 
        subject = "Evinizde Tanınmayan Birisi Var!"

        attachments = list()

        for f in os.listdir("captured"):
            attachments.append(os.path.join("captured", f))


        #configure reciever and send mail
        
        print('Sunucuya Bağlanılıyor...')
        server = EmailConnection()
        print('{} adına, {} mail adresine sahip kişiye mail gönderilecek.'.format(to_name,to_email))
        message = """<font="Open Sans" size="8">Merhaba {},<br>
        Evinizde <b>tanınmayan</b> bir kişi tespit ettim.<br><br>
        Size bu kişinin kim olduğunu anlayabilmeniz için birkaç tane fotoğraf gönderdim.<br><br>
        Gönderdiğim fotoğrafları ekte bulabilirsiniz.<br></font>
        """.format(to_name)
        email = Email(from_='"{}" <{}>'.format(name, from_email), #from
                        to='"{}" <{}>'.format(to_name, to_email), #to
                        subject=subject, message=message, attachments=attachments)
        print('Gönderiliyor...')
        server.send(email)
        del email
        #disconnect
        print('Bağlantı Kesiliyor...')
        server.close()
            
        print('Gönderildi!')
