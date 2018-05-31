import re
import codecs


def parser():
    result = dict()

    host_pattern = re.compile('@(.*)\.')
    pattern_for_matching = re.compile(
        'Working mail:\n(?P<senders_address>.*\n.*)\n\nAddresses:\n(?P<sending_addresses>(.*\n)*)'
        'Theme:\n(?P<theme>.*)\n\nFiles:\n(?P<sending_files>(.*\n)*)')

    senders_address = dict()
    addresses = list()
    theme = ''
    files_for_sending = list()
    host = ''
    message = ''

    config_file_info = ''

    with open('C:\\smpt_client\\files\\config.txt', 'r', encoding='utf-8') as file:
        config_file_info = file.read()

    print(config_file_info)

    full_match = pattern_for_matching.match(config_file_info)

    senders_address['senders_mail'], senders_address['senders_password'] = \
        full_match.group('senders_address').split(';')[0].replace('\n', ''), \
        full_match.group('senders_address').split(';')[1].replace('\n', '')

    for addr in full_match.group('sending_addresses').split(';'):
        addresses.append(addr.replace('\n', ''))

    theme = full_match.group('theme').replace('\n', '')

    for file in full_match.group('sending_files').split(';'):
        files_for_sending.append(file.replace('\n', ''))

    host = host_pattern.search(senders_address.get('senders_mail')).group(1)

    with open('C:\\smpt_client\\files\\message.txt', 'rb') as file:
        message = file.read().decode()

    result['senders_address_pass'], result['sending_addresses'], result['theme'], \
    result['files_for_sending'], result['host'], result['message'] \
        = senders_address, addresses, theme, \
          files_for_sending, host, message

    #print(senders_address)
    #print(addresses)
    #print(theme)
    #print(files_for_sending)
    #print(host)
    #print(message)

    return result

if __name__ == '__main__':
    print(parser())