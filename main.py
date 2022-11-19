import sys

numbers = '0123456789'
# offset_1 - количество не шифруемых чисел с левой стороны
# offset_2 - количество не шифруемых чисел с правой стороны
offset_1, offset_2 = 3, 2

# Пути к файлам, используемые, если запускать скрипт без указания путей к файлам
FILEPATHS_DEFAULT = {
    'input': r'phones.txt',
    'encrypted': r'encrypted.txt',
    'decrypted': r'decrypted.txt'
}


def encrypt_txt(filepath_input: str, filepath_output: str, key: int):
    def encrypt_phone(phone: str, key: int):
        phone_encrypted = ['0', *phone[:offset_1]]
        
        encrypted_part = []
        for i_phone in range(len(phone[offset_1:-offset_2])):
            n = phone[i_phone+offset_1]
            i_numbers = numbers.find(n)
            for _ in range(key):
                i_numbers += 1
                if i_numbers == len(numbers):
                    i_numbers = 0
            encrypted_part.append(str(numbers[i_numbers]))
        phone_encrypted += encrypted_part

        check_sum = sum([int(i) for i in phone[offset_1:-offset_2]])
        if check_sum < 10:
            check_sum = f'0{check_sum}'
        phone_encrypted += list(str(check_sum))

        phone_encrypted += phone[-offset_2:]
        return ''.join(phone_encrypted)

    with open(filepath_input, 'r') as f:
        phones = f.read().splitlines()
    phones_encrypted = '\n'.join([encrypt_phone(phone, key) for phone in phones])
    with open(filepath_output, 'w') as f:
        f.write(phones_encrypted)
    print(f'Phones from "{filepath_input}" was encrypted to "{filepath_output}"')


def decrypt_txt(filepath_input: str, filepath_output: str, key: int):
    def decrypt_phone(phone_encrypted: str, key: int):
        phone_encrypted = phone_encrypted[1:]
        phone_decrypted = [*phone_encrypted[:offset_1]]

        decrypted_part = []
        for i_phone in range(len(phone_encrypted[offset_1:-offset_2-2])):
            n = phone_encrypted[i_phone + offset_1]
            i_numbers = numbers.find(n)
            for _ in range(key):
                i_numbers -= 1
                if i_numbers == -1:
                    i_numbers = len(numbers) - 1
            decrypted_part.append(str(numbers[i_numbers]))
        phone_decrypted += decrypted_part

        check_sum = str(sum([int(i) for i in decrypted_part]))
        check_sum = f'0{check_sum}' if len(check_sum) == 1 else str(check_sum)
        real_check_sum = phone_encrypted[-offset_2-2:-offset_2]
        if check_sum != real_check_sum:
            print(f'ChecksumError with 0{phone_encrypted}')

        phone_decrypted += phone_encrypted[-offset_2:]
        return ''.join(phone_decrypted)

    with open(filepath_input, 'r') as f:
        phones_encrypted = f.read().splitlines()
    phones_decrypted = '\n'.join([decrypt_phone(phone_encrypted, key) for phone_encrypted in phones_encrypted])
    with open(filepath_output, 'w') as f:
        f.write(phones_decrypted)
    print(f'Values from "{filepath_input}" was decrypted to "{filepath_output}"')


def main():
    ms = """
Usage example:
    Encrypt: python main.py e 2 phones.txt encrypted.txt
    Decrypt: python main.py d 12 encrypted.txt decrypted.txt
Or use default paths to files like above:
    Encrypt: python main.py e 53
    Decrypt: python main.py d 754
"""
    match len(sys.argv):
        case 1:
            raise TypeError(f'Аргументы отсутствуют.\n{ms}')
        case 2:
            raise TypeError(f'Отсутствует ключ шифрования.\n{ms}')
        case 3:
            match sys.argv[1]:
                case 'e':
                    encrypt_txt(FILEPATHS_DEFAULT['input'], FILEPATHS_DEFAULT['encrypted'], int(sys.argv[2]))
                case 'd':
                    decrypt_txt(FILEPATHS_DEFAULT['encrypted'], FILEPATHS_DEFAULT['decrypted'], int(sys.argv[2]))
        case 4:
            raise TypeError(f'Не задан один из файлов.\n{ms}')
        case 5:
            match sys.argv[1]:
                case 'e':
                    encrypt_txt(sys.argv[3], sys.argv[4], int(sys.argv[2]))
                case 'd':
                    decrypt_txt(sys.argv[3], sys.argv[4], int(sys.argv[2]))


if __name__ == '__main__':
    main()
    # key = 3
    # encrypt('phones.txt', 'encrypted.txt', key=key)
    # decrypt('encrypted.txt', 'decrypted.txt', key=key)