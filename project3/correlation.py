from typing import List
import numpy as np
from matplotlib import pyplot as plt
import collections
from itertools import combinations

def lfsr(taps: List[int], init_state: List[int], length: int) -> List[int]:
	
	for tap in taps:
		if max(taps) > len(init_state):
			print('The length of the lfsr is shorter than the tap indexes.')
			return -1
			
	state = init_state.copy()
	sequence = []

	for _ in range(0, length):
		new_val = 0
		for tap in taps:
			new_val += state[len(init_state)-tap] 
		new_val = new_val % 2
		sequence.append(state.pop(0))
		state.append(new_val)
	return sequence

def corr_prob(str1, str2):
    dist = 0
    if len(str1) != len(str2):
        print("Strings must be same length")
        return "njet"
    for char1, char2 in zip(str1, str2):
        dist += int(char1, 2) ^ int(char2, 2)
    return (1 - dist/len(str1))

##Find the nbr_elements most deviating (from 0.5) elements and return them
def find_max_dev(cor1, cor2, cor3, nbr_elements):
    nbr_elements = int(nbr_elements/2)
    sorted1 = [(index, e) for index, e in enumerate(cor1)]
    sorted2 = [(index, e) for index, e in enumerate(cor2)]
    sorted3 = [(index, e) for index, e in enumerate(cor3)]
    sorted1.sort(key=lambda x:x[1])
    sorted2.sort(key=lambda x:x[1])
    sorted3.sort(key=lambda x:x[1])

    max_values = [sorted1[0:int(nbr_elements)] + sorted1[len(sorted1) - 1 - nbr_elements: len(sorted1)], 
    sorted2[0:nbr_elements] + sorted2[len(sorted2) - 1 - nbr_elements: len(sorted2)], 
    sorted3[0:nbr_elements] + sorted3[len(sorted3) - 1 - nbr_elements: len(sorted3)]]
    
    ret1 = [(index, prob) for (index, prob) in sorted1 if (index, prob) in max_values[0]]
    ret2 = [(index, prob) for (index, prob) in sorted2 if (index, prob) in max_values[1]]
    ret3 = [(index, prob) for (index, prob) in sorted3 if (index, prob) in max_values[2]]
    return [ret1, ret2, ret3]

##Generate keystream from three lfsr sequences
def gen_keystream(seq1, seq2, seq3):
    keystream = []
    for candidate in zip(seq1, seq2, seq3):
        counted = collections.Counter(candidate)
        keystream.append(max(counted, key=counted.get))
    return keystream


if __name__ == '__main__':
    keystream =  '1110100000011111001000001100010111011010011100001000101100110001100111100001000001011111010001010111101110101101101000101010101111001011011100011000111100000111101111101110110000101010010101101'
    stream_len = len(keystream)
    N = 10 #Number of outliers (Cannot be larger than 2**13) 
    c1 = [1,2,4,6,7,10,11,13]
    c2 = [2,4,6,7,10,11,13,15]
    c3 = [2,4,5,8,10,13,16,17]
    c1_pow = 2**13
    c2_pow = 2**15
    c3_pow = 2**17
    cor1 = []
    sequences1 = []
    cor2 = []
    sequences2 = []
    cor3 = []
    sequences3 = []

    ##Calculate all probabilities
    for init_state in range(1, c3_pow):
        if init_state < c1_pow:
            sequences1.append(lfsr(c1, [int(i) for i in '{0:013b}'.format(init_state)], stream_len))
            cor1.append(corr_prob(keystream, "".join([str(digit) for digit in sequences1[init_state-1]])))
        if init_state < c2_pow:
            sequences2.append(lfsr(c2, [int(i) for i in '{0:015b}'.format(init_state)], stream_len))
            cor2.append(corr_prob(keystream, "".join([str(digit) for digit in sequences2[init_state-1]])))
        sequences3.append(lfsr(c3, [int(i) for i in '{0:017b}'.format(init_state)], stream_len))
        cor3.append(corr_prob(keystream, "".join([str(digit) for digit in sequences3[init_state-1]])))

    ##Take out outliers N largest and lowest and add their sequences
    outliers = find_max_dev(cor1, cor2, cor3, N)
    print("Max outliers 1 = ", max(outliers[0], key=lambda x:x[1]))
    print("Max outliers 2 = ", max(outliers[1], key=lambda x:x[1]))
    print("Max outliers 3 = ", max(outliers[2], key=lambda x:x[1]))

    print("\nMax prob 1 = ", max(cor1))
    print("Max prob 2 = ", max(cor2))
    print("Max prob 3 = ", max(cor3))
    
    sequences = [[],[],[]]
    for element in outliers[0]:
        sequences[0].append(sequences1[element[0]])
    for element in outliers[1]:
        sequences[1].append(sequences2[element[0]])
    for element in outliers[2]:
        sequences[2].append(sequences3[element[0]])
    print("\nlen seq = ", len(sequences[0]))
    
    ##Generate keystreams for all sequences
    keystreams = []
    keystreams += [gen_keystream(sequences[0][i], sequences[1][i], sequences[2][i]) for i in range(len(sequences[0]))]
    #max_keystream = [gen_keystream()]
    
    for stream in keystreams:
        stream_string = ''.join([str(digit) for digit in stream])
        if stream_string == keystream:
            print("\nKey found: ", stream_string, "\n")
            ind = keystreams.index(stream)
            print(f"keystream nbr: {ind} which corresponds to sequences: \nseq1: {sequences[0][ind]}, \nseq2: {sequences[1][ind]}, \nseq3: {sequences[1][ind]}\n")
            print(f"Which corresponds to values: {outliers[0][ind][1]}, {outliers[1][ind][1]}, {outliers[2][ind][1]}\n")
            print(f"And initial states:\nstate1: {[int(i) for i in '{0:013b}'.format(outliers[0][ind][0])]}\nstate2: {[int(i) for i in '{0:013b}'.format(outliers[1][ind][0])]}\nstate3: {[int(i) for i in '{0:013b}'.format(outliers[2][ind][0])]}")
        #print("\nNot a key: \n", stream_string, "\nShould be: \n", keystream)

    #Plot results
    # fig, (corr1, corr2, corr3) = plt.subplots(3)
    # fig.suptitle('Probabilities')
    # corr1.plot(np.array([i for i in range(len(cor1))]), np.array(cor1), 'o', color='black')
    # corr2.plot(np.array([i for i in range(len(cor2))]), np.array(cor2), 'o', color='blue')
    # corr3.plot(np.array([i for i in range(len(cor3))]), np.array(cor3), 'o', color='red')

    # ##Plot outliers
    # fig2, (out1, out2, out3) = plt.subplots(3)
    # fig2.suptitle('Outliers')
    # out1.plot(np.array([element[0] for element in outliers[0]]), np.array([element[1] for element in outliers[0]]), 'o', color='black')
    # out2.plot(np.array([element[0] for element in outliers[1]]), np.array([element[1] for element in outliers[1]]), 'o', color='blue')
    # out3.plot(np.array([element[0] for element in outliers[2]]), np.array([element[1] for element in outliers[2]]), 'o', color='red')

    # plt.show()