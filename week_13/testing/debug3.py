import numpy as np 
import argparse
import matplotlib.pyplot as plt 
import sys

def read_input_file(filename):
	'''
	Read a fasta file containing a sequence of genetic data (e.g aaaccttggaa) and turn it into a single string
	of all upper case letters
	Input: filename (string)
	Returns: sequence (string)
	'''

    with open(filename) as file:
        sequence = file.read().replace('\n','').upper()
    return sequence

def basecounts(sequence):
	'''
	Count the occurances of each base in a sequence
	Input: sequence (string)
	Returns: base counts (dictionary)
	'''

	return {'A': sequence.count('A'), 'C': sequence.count('C'), 'T': sequence.count('T'), 'G': sequence.count('G')}


def get_complement(sequence, reverse=False):
	'''
	Returns the complement of a genetic sequence. 
	If flag reverse=True is included, returns the reverse complement of the sequence.
	E.g for input ACTGA, the complement is TGAC, and reverse complement is CAGT.
	Input: sequence (string)
	Returns: sequence(string)
	'''

	comp = {'A': 'T', 'C': 'G', 'G': 'c', 'T': 'A'
	
	if reverse:
		result = "".join(comp.get(base, base) for base in reversed(sequence))
	else:
		result = "".join(comp.get(base, base) for base in sequence) 
		
	return result

def calculate_gc_content(sequence):
	'''
	Calculates the GC content of a sequence
	Inputs: Sequence (string)
	Returns: GC content (float)
	'''

    seq_length=len(sequence)

    numberG=sequence.count('G')
    numberC=sequence.count('C')

    if seq_length = 0:
        return 0
    else:
        GC_content = ((numberG+numberC)/seq_length)*100

    return GC_content

def detect_gc_islands(sequence, window_size, gc_threshold):
	'''
	Finds regions within a sequence that have a GC content above a threshold.
	Inputs:
		sequence (string)
		window_size (int) - size of the regions to check
		gc_threshold (float) - the threshold for a region to be considered a GC island.
	Returns: gc_islands (nested list) - each element contains the start and end indices of the detected island
	'''

    gc_islands = []

    #Loop over the sequence
    for i in range(len(sequence) - window_size + 1):
    	#Extract a slice of correct length
        window = sequence[i:i+window_size]
        #Calculate the GC content for that slice
        gc_content = calculate_gc_content(window)

        #Store if GC content exceeds threshold
        if gc_content > gc_threshold:
            gc_islands.append((i, i+window_size, gc_content))

    return gc_islands

def find_mean_gc(sequence, window_size):
	'''
	Find the mean GC content for a sequence and window size
	Inputs:
		sequence (string)
		window_size (int)
	Returns: mean of GC content (float)
	'''

	gc_contents = []

	for i in range(0, len(sequence)-window_size):
		start_index = i 
		end_index = i+window_size+1
		window = sequence[start_index:end_index]
		gc_contents.append(calculate_gc_content(window))
		
	return np.mean(gc_contents)

def plot_gc_comparison(seq1, seq2, window_size, gc_threshold):
	'''
	Compares and plots the GC content of two sequences
	Inputs: 
		seq1 (string) - first sequence
		seq2 (string) - second sequence
		window_size (int) - window to use for calculation of GC islands
		threshold (float) - GC content fraction that must be exceeded
	'''

    cpg_content_seq1 = []
    cpg_content_seq2 = []

    for i in range(len(seq1) - window_size + 1):
        window_seq1 = seq1[i:i+window_size]
        window_seq2 = seq2[i:i+window_size]

        gc_content_seq1 = calculate_gc_content(window_seq1)
        gc_content_seq2 = calculate_gc_content(window_seq2)

        cpg_content_seq1.append(gc_content_seq1)
        cpg_content_seq2.append(gc_content_seq2)

    plt.figure(figsize=(10, 6))
    plt.plot(cpg_content_seq1, label='Sequence 1')
    plt.plot(cpg_content_seq2, label='Sequence 2')

    plt.axhline(y=gc_threshold, color='r', linestyle='--', label=f'GC Content Threshold ({gc_threshold}%)')

    plt.xlabel('Window Index')
    plt.ylabel('GC Content (%)')
    plt.title('GC Content Comparison')
    plt.legend()
    plt.show()

def test_rev_comp():

  assert get_complement('ATCG', True)=='CGAT', "reverse complement test"
  print("Tests passed")

def test_gc_content():
    assert calculate_gc_content('GGGGAAAAAAAATTTATATATCGCC')==32, "gc_content test"
    print("Tests passed")

def write_report(output_file, input_file, bases, complement, gc, islands):

	with open(output_file, 'a') as f:
		f.write("Input file: %s\n" % input_file)

		if bases:
			f.write("Base counts\n")
			f.write("A\tC\tG\tT\n")
			f.write(str(bases['A']))
			f.write('\t')
			f.write(str(bases['C']))
			f.write('\t')
			f.write(str(bases['G']))
			f.write('\t')
			f.write(str(bases['T']))
			f.write('\n')

		if complement:
			f.write("Complement: \t")
			complement_string = ''
			for char in complement:
				complement_string+=char
			f.write(complement_string)
			f.write('\n')

		if gc:
			f.write("GC content: %.3f\n" % bc)

		if islands:
			f.write("GC islands:\t")
			f.write(str(islands))
			f.write('\n')

		f.write('\n')
		f.write('\n')

def main(*args):

	parser = argparse.ArgumentParser(description='Genetic data processing tool')
	parser.add_argument('--base_count', action='store_true')
	parser.add_argument('--complement', action='store_true')
	parser.add_argument('--gc_content', action='store_true')
	parser.add_argument('--gc_islands', action='store_true')
	parser.add_argument('--input', nargs='+', required=True)
	parser.add_argument('--output')

	args = parser.parse_args()
	input_files = args.input 
	show_bases = args.base_count 
	show_complement = args.complement
	show_gc = args.gc_content
	show_islands = args.gc_islands
	output_file = args.output 


	for file in input_files:
		sequence = read_input_file(file)

		bases, complement, gc, islands = (None, None, None, None)

		if show_bases:
			bases = basecounts(sequence)
		if show_complement:
			complement = get_complement(sequence, True)
		if show_gc:
			gc = calculate_gc_content(sequence)
		if show_islands:
			islands = detect_gc_islands(sequence,int(0.1*len(sequence)), 50) 
			print(islands)

		write_report(output_file, file, bases, complement, gc, islands)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(*args)

