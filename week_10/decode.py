

def CipherCaeser(text, shift):

    assert shift < 26 and shift > -26, "shift must be within -26 and 26"

    ciphertext = ""

    for c in text:
        if shift < 0:
            shift += 26

        next = ord(c) + shift

        if next > ord('z'):
            next -= 26

        ciphertext += chr(next)
    
    return ciphertext


def EnigmaForWord(word, common):

    for ii in range (0, 26):

        word_cc = CipherCaeser(text=word, shift=ii)
        if word_cc in common:
            return word_cc
        
    raise Exception(f"Can't decode word: {word}")


def EngimaForSentence(sentence, common):
    
    plain = ""

    for word in sentence.split():
        plain += EnigmaForWord(word, common) + ' '
    
    return plain.strip()
    

with open('word_list.txt', 'r') as f:

    words = [line.rstrip('\n') for line in f]


tests = ['khoor', 
         'Khoor', 
         'puppy', 
         'khoor khoor']

for test in tests:
    try:
        print(EngimaForSentence(test, words))
    except Exception as e:
        print(e)



