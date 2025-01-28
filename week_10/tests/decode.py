''' Task 1 - Caesar cipher
Write your code for implementing the Caesar cipher here.
'''
def caesar_cipher(text, shift):

    ciphertext = ""

    for c in text:
        if c.lower() != c:
              raise Exception("Invalid character in message")

        if shift < 0:
            shift += 26

        next = ord(c) + shift

        if next > ord('z'):
            next -= 26

        ciphertext += chr(next)
    
    return ciphertext


'''
The code below is a test function for your code. It will run automatically when you run the script. Do not modify it. 
To pass this assignment, your code must pass all the tests.
'''

def test_caesar_cipher():

	#The assert function will raise an error if the expression contained within it doesn't evaluate to True
	assert caesar_cipher('a', 1) == 'b', "Test 1 failed"
	assert caesar_cipher('a', 2) == 'c', "Test 2 failed"
	assert caesar_cipher('z', 1) == 'a', "Test 3 failed"
	assert caesar_cipher('a', -1) == 'z', "Test 4 failed"
	assert caesar_cipher('hello', 3) == 'khoor', "Test 5 failed"
	assert caesar_cipher('khoor', -3) == 'hello', "Test 6 failed"

	print("Encoding tests passed - great job!")

''' Task 2 - Decoding
Write your code for decoding a message when we don't know the shift. 
You are given a list of words that the message may be composed of. 
Your code should work by *brute force* i.e it should check all possible shifts until it finds a match
'''


def decode_word(word, word_list):

    for ii in range (0, 26):

        word_cc = caesar_cipher(text=word, shift=ii)
        if word_cc in word_list:
            return word_cc
        
    raise Exception(f"Can't decode word: {word}")

def decode_sentence(sentence, word_list):
    
    plain = ""

    for word in sentence.split():
        plain += decode_word(word, word_list) + ' '
    
    return plain.strip()


def decode_message(message, word_list):
      
	try:
		return decode_sentence(message, word_list)
	except Exception as e:
		return str(e)

word_list_filename = 'allowed_words.txt'

with open(word_list_filename, 'r') as f:
      
	  word_list_file = [line.rstrip('\n') for line in f]

'''
The code below is a test function for task 2. It will run automatically when you run the script. Do not modify it.
To pass this assignment, your code must pass all the tests.
'''


def test_decode_message():

	assert decode_message("khoor", word_list_file) == "hello", "Test 1 failed. Output was %s" % decode_message("khoor", word_list_file)
	assert decode_message("Khoor", word_list_file) == "Invalid character in message", "Test 2 failed. Output was %s" % decode_message("Khoor", word_list_file)
	assert decode_message("khoor khoor", word_list_file) == "hello hello", "Test 3 failed. Output was %s" % decode_message("khoor khoor", word_list_file)
	assert decode_message("puppy", word_list_file) == "Can't decode word: puppy", "Test 4 failed. Output was %s" % decode_message("puppy", word_list_file) 

	print("Decoding tests passed - well done")

'''
The main function here just calls both test functions one after the other. 
You do not need to modify this.
Note that running this code without any changes will produce an error- this is *not* a mistake in the script. 
If you've understood and completed the lab exercises, you should be able to see why this error occurs
and what you need to do to fix it.
'''


def main():

	test_caesar_cipher()
	test_decode_message()

main()
