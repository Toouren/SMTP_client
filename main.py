import base64
import socket
import ssl
import client_worker
import re
import binascii
import time
import base64


file_exp_pattern = re.compile('\.(.*)')
file_exp = {'jpg':'image/jpg', 'png':'image/png', 'pdf':'application/pdf'}
sending_address = ''
point_pattern = re.compile('\n.\n')


def my_send(sock, message):
    print('C: ' + message.decode())
    sock.send(message)
    print('S: ' + sock.recv(1024).decode())

def get_file_exp(file_name):
    return file_exp_pattern.search(file_name).group(1)

def get_file_bytes(file_name):
    with open(f'C:\\smpt_client\\files\\{file_name}', 'rb') as file:
        return file.read()

def generate_attachment_bloc(name):
    attachment = f'''Content-Type: {file_exp[get_file_exp(name)]}
Content-transfer-encoding: base64
Content-Disposition: attachment;
 filename="{name}"

{base64.encodestring(get_file_bytes(name)).decode()}
'''
    return attachment


def get_n_points(matchobj):
    points = '.'*(len(matchobj.group(1))+1)
    return '\r\n' + points


def replace(text):
    points_pattern = re.compile('\r\n(\.?)')
    text = re.sub(points_pattern, get_n_points, text)
    return text


def construct_letter(senders_mail, sending_mails, theme, files_list, text):

    letter = f'''From: {senders_mail}
To: {sending_mails}
Subject: {theme}
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="C6y6NN0QaSkb14zK9VQuBtUq0M8SufNy"

--C6y6NN0QaSkb14zK9VQuBtUq0M8SufNy
Content-Type: text/plain

{replace(text)}
--C6y6NN0QaSkb14zK9VQuBtUq0M8SufNy
'''
    for file in files_list:
        if file != files_list[len(files_list)-1]:
            letter += generate_attachment_bloc(file)
            letter += '--C6y6NN0QaSkb14zK9VQuBtUq0M8SufNy\n'
        else:
            letter += generate_attachment_bloc(file)

    letter += '--C6y6NN0QaSkb14zK9VQuBtUq0M8SufNy--\n.\n'

    return letter


smtp_servers = {'yandex':'smtp.yandex.ru', 'mail':'smtp.mail.ru', 'rambler':'smtp.rambler.ru'}

parsed_data = client_worker.parser()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = ssl.wrap_socket(sock)
sock.connect((smtp_servers.get(parsed_data['host']), 465))
sock.recv(1024)

my_send(sock, b'EHLO mysmtpclient\n')
my_send(sock, b'AUTH LOGIN\n')

time.sleep(3)

login = base64.encodestring(parsed_data['senders_address_pass']['senders_mail'].encode())
my_send(sock, login)

time.sleep(3)

password = base64.encodestring(parsed_data['senders_address_pass']['senders_password'].encode())
my_send(sock, password)

time.sleep(3)

my_send(sock, f'MAIL FROM: {parsed_data["senders_address_pass"]["senders_mail"]}\n'.encode())

for addr in parsed_data['sending_addresses']:
    sending_address += addr + ', '
    my_send(sock, f'RCPT TO: {addr}\n'.encode())

time.sleep(3)

my_send(sock, b'DATA\n')

time.sleep(3)
#print(construct_letter(parsed_data['senders_address_pass']['senders_mail'],
                       #parsed_data['sending_addresses'], parsed_data['theme'],
                       #parsed_data['files_for_sending'], parsed_data['message']))

my_send(sock, construct_letter(parsed_data['senders_address_pass']['senders_mail'],
                               sending_address[:-2], parsed_data['theme'],
                               parsed_data['files_for_sending'], parsed_data['message']).encode())

#my_send(sock, construct_letter())

sock.close()
