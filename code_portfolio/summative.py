from math import sin
from math import sqrt
# Use of csv library is optional- you can use it, but don't need to. 
import csv

'''
============================================
Portfolio exercise 1 - put your code for portfolio exercise 1 here. You should only need to change the '???' strings
============================================
'''

def comparisons(a, b):

    message = ''

    if a > b:
        message += "%.2f is greater than %.2f\n" % (a, b)
    if a < b:
        message += "%.2f is less than %.2f\n" % (a, b)
    if a == b:
        message += "%.2f is equal to %.2f\n" % (a, b)
    '''
    Note- we've changed this from being within 0.1% to just within 0.1. 
    You may need to change this code from previously submitted solutions.
    '''
    if b - a < 0.1 and b - a > -0.1:
        message += " %.2f is within 0.1 of %.2f" % (a, b)

    return message


'''
============================================
Portfolio Exercise 2 - put your code for portfolio exercise 2 here.
============================================
'''

def kepler():

    M = 1.54
    e = 0.3
    print('Mean anomaly M is',M)
    print('Eccentricity e is',e)

    # guess
    E = M

    for ii in range(10):
        E = M + e * sin(E)
        print('Iteration',ii,'value of E',E)
    print('Eccentric anomaly E is',E)
    print('E - e sin E is', E - e*sin(E))

    return E


'''
============================================
Portfolio Exercise 3 - put your code for portfolio exercise 3 here.
============================================
'''

names = ["Martin", "Arthur", "Hemma", "Josh"]
Q1 = [6, 3, 7, 4]
Q2 = [1, 8, 4, 7]
Q3 = [4, 4, 5, 3]

def total(questions):
    
    totals = [0, 0, 0, 0]
    
    for q in questions:
        for i in range(len(q)):
            totals[i] += q[i]
    
    return totals

def calc_mean(totals):

    return sum(totals)/len(totals)

def calc_std_dev(totals):

    u = calc_mean(totals)
    N = len(totals)

    standard_dev = 0

    for x in totals:

        standard_dev += (x - u) ** 2

    return sqrt(standard_dev / N)


def normalised(totals, u):

    return [x - u for x in totals]

def graded(mark, s):

    if mark < -1 * s:
        return "Fail"
    if mark < 0:
        return 'C'
    if mark < s:
        return 'B'
    return 'A'

def assign_grades():

    totals = total([Q1, Q2, Q3])

    mean = calc_mean(totals)
    std_dev = calc_std_dev(totals)

    norm_totals = normalised(totals, mean)
    grades = []
    
    for t in norm_totals:
        grades.append(graded(t, std_dev))

    #Please use the file below to save your output.
    grade_file = "grade_file.csv"

    with open(grade_file,'w') as f:

        f = csv.writer(f, lineterminator='\n')

        f.writerow(['mean', mean])
        f.writerow(['standard deviation', std_dev])
        
        for i in range(len(names)):
            f.writerow([names[i], grades[i]])

    pass


'''
============================================
Portfolio Exercise 4 - put your code for portfolio exercise 3 here.
============================================
'''

word_list_file = 'word_list.txt'

def caesar_cipher(text, shift):

    
    ciphertext = ""

    for c in text:
        if c < 'a' or c > 'z':
            raise Exception("Invalid character in message")


        if shift < 0:
            shift += 26

        next = ord(c) + shift

        if next > ord('z'):
            next -= 26

        ciphertext += chr(next)
    
    return ciphertext


def decode_word(word, common_words):

    for ii in range (0, 26):

        word_cc = caesar_cipher(text=word, shift=ii)
        if word_cc in common_words:
            return word_cc
        
    raise Exception(f"Can't decode word: {word}")

def decode_message(sentence, file):
    
    with open(file, 'r') as f:

        common_words = [line.rstrip('\n') for line in f]

    plain = ""

    try:

        for word in sentence.split():

            plain += decode_word(word, common_words) + ' '
        
        return plain.strip()
    
    except Exception as e:
       
       return str(e)


'''
============================================
Test functions - code below this line must not be modified
============================================
'''

def test_comparisons():

    print("Testing Portfolio exercise 1")
    assert comparisons(1, 2) == "1.00 is less than 2.00\n", "Test 1 failed: Your output was %s" % comparisons(1, 2)
    assert comparisons(2, 1) == "2.00 is greater than 1.00\n", "Test 2 failed: Your output was %s" % comparisons(2, 1)
    assert comparisons(2, 2) == "2.00 is equal to 2.00\n 2.00 is within 0.1 of 2.00", "Test 3 failed: Your output was %s" % comparisons(2, 2)
    assert comparisons(2.05, 2) == "2.05 is greater than 2.00\n 2.05 is within 0.1 of 2.00", "Test 4 failed: Your output was %s" % comparisons(2.05, 2)
    print("Test complete")


def test_kepler():

    print("Testing Portfolio exercise 2")
    eccentricity = 0.3 
    mean_anomaly = 1.54

    ecc_anomaly = kepler()
    kepler_err = ecc_anomaly - eccentricity*sin(ecc_anomaly) - mean_anomaly

    assert kepler_err**2 < (1e-4*mean_anomaly)**2, f'Equation not close enough: error is {kepler_err}'
    print("Test complete")


def test_assign_grades():
    
    print("Testing Portfolio exercise 3")
    with open("grade_file.csv", "r") as f:
        data = f.readlines()

    assert len(data) == 6, "File should contain 6 lines, but actually contains %d" % len(data)
    
    mean = float(data[0].split(',')[1])
    assert mean == 14.0, "Mean should be 14.0, but is actually %.3f" % mean

    standard_deviation = float(data[1].split(',')[1])
    assert standard_deviation > 1.87 and standard_deviation < 1.88, "Standard deviation should be between 1.87 and 1.88, but is actually %.3f" % standard_deviation

    martin_grade = data[2].split(',')[1].strip()
    assert martin_grade == 'Fail', "Martin's grade should be Fail, but is actually %s" % martin_grade

    arthur_grade = data[3].split(',')[1].strip()
    assert arthur_grade == 'B', "Arthur's grade should be B, but is actually %s" % arthur_grade

    hemma_grade = data[4].split(',')[1].strip()
    assert hemma_grade == 'A', "Hemma's grade should be A, but is actually %s" % hemma_grade

    josh_grade = data[5].split(',')[1].strip()
    assert josh_grade == 'B', "Josh's grade should be A, but is actually %s" % josh_grade
    print("Test complete")

def test_caesar_cipher():

    #The assert function will raise an error if the expression contained within it doesn't evaluate to True
    assert caesar_cipher('a', 1) == 'b', "Test 1 failed"
    assert caesar_cipher('a', 2) == 'c', "Test 2 failed"
    assert caesar_cipher('z', 1) == 'a', "Test 3 failed"
    assert caesar_cipher('a', -1) == 'z', "Test 4 failed"
    assert caesar_cipher('hello', 3) == 'khoor', "Test 5 failed"
    assert caesar_cipher('khoor', -3) == 'hello', "Test 6 failed"

    print("Encoding tests passed - great job!")

def test_decode_message():

    assert decode_message("khoor", word_list_file) == "hello", "Test 1 failed. Output was %s" % decode_message("khoor", word_list_file)
    assert decode_message("Khoor", word_list_file) == "Invalid character in message", "Test 2 failed. Output was %s" % decode_message("Khoor", word_list_file)
    assert decode_message("khoor khoor", word_list_file) == "hello hello", "Test 3 failed. Output was %s" % decode_message("khoor khoor", word_list_file)
    assert decode_message("puppy", word_list_file) == "Can't decode word: puppy", "Test 4 failed. Output was %s" % decode_message("puppy", word_list_file) 

    print("Decoding tests passed - well done")

def test_cipher():

    print("Testing Portfolio exercise 4")
    test_caesar_cipher()
    test_decode_message()
    print("Test complete")

def main():

    marks = 20

    try:
        test_comparisons()
        print("Test passed - well done.")
    except Exception as error:
        marks = marks - 5 
        print ("Test failed with error")
        print(error)

    try:
        test_kepler()
        print("Test passed - well done.")
    except Exception as error:
        marks = marks - 5 
        print ("Test failed with error")
        print(error)

    try:
        assign_grades()
        test_assign_grades()
        print("Test passed - well done.")
    except Exception as error:
        marks = marks - 5 
        print ("Test failed with error")
        print(error)

    try:
        test_cipher()
        print("Test passed - well done.")
    except Exception as error:
        marks = marks - 5 
        print ("Test failed with error")
        print(error)

    print("All tests complete")
    print("Total mark: %d" % marks)

main()





