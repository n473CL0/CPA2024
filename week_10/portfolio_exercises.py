def caesar_cipher(plain_text, shift):
    cipher_text = ""
    for c in plain_text:
        next_char = ord(c) + shift
        if next_char > ord('z'):
            next_char -= 26
        elif next_char < ord('a'):
            next_char += 26
        cipher_text += chr(next_char)
    return cipher_text


print(caesar_cipher("hello world", 3))