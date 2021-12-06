from typing import List
import numpy as np
from matplotlib import pyplot as plt

def lfsr(taps: List[int], init_state: List[int], length: int) -> List[int]:
	
	for tap in taps:
		if max(taps) > len(init_state):
			print('The length of the lfsr is shorter than the tap indexes.')
			return -1
			
	state = init_state.copy()
	sequence = []
	counter = 0

	for _ in range(0, length):
		new_val = 0
		for tap in taps:
			new_val += state[tap-1] 
		new_val = new_val % 2
		sequence.append(state.pop(0))
		state.append(new_val)
	return sequence

def majority_function(lfsrs: List[List[int]]) -> List[int]:
	key_stream = []
	length = len(lfsrs[0])
	for i in range(1, len(lfsrs)):
		if len(lfsrs[i]) != length:
			print("Sequences has different length.")
			return
		length = len(lfsrs[i])	
		
	for i in range(0,length):
		values = []
		for lfsr in lfsrs:
			values.append(lfsr[i])
		key_stream.append(count_binary_majority(values))
	return key_stream


def count_binary_majority(values: List[int]) -> int:
	zeros = 0
	ones = 0
	
	if len(values) % 2 == 0:
		print('Number of values must be odd.')
		return -1
	for value in values:
		if value == 1:
			ones += 1
		elif value == 0:
			zeros += 1
		else:
			print("Method 'count_binary_sequence' only supports binary digits.")
			return -1
	if ones > zeros:
		return 1
	else:
		return 0

def bin_to_list(binary_string: str) -> List[int]:
	binary_list = []
	for digit in binary_string:
		if digit == '0':
			binary_list.append(0)
		elif digit == '1':
			binary_list.append(1)
		else:
			print('Non-binary digits not allowed.')
			return -1
	return binary_list

def hamming2(first, second):
	assert len(first) )) len(second)
	return sum(c1 != c2 for c1, c2 in zip(first, second)
if __name__ == '__main__':
	c1 = [1,2,4,6,7,10,11,13]
	c2 = [2,4,6,7,10,11,13,15]
	c3 = [2,4,5,8,10,13,16,17]
		
	c1_length = 13
	c2_length = 15
	c3_length = 17
	
	with open("key_stream.txt", 'r') as key_stream_file:
		key_stream_str = key_stream_file.readline().rstrip('\n')
	
	key_stream_length = len(key_stream_str)
	key_stream = np.array(bin_to_list(key_stream_str))
	
	plt.title('C1 Correlation')
	plt.xlabel('State')
	plt.ylabel('Estimated Correlation')
	
	est_correlations_1 = []
	for init_state in range(1, 2**13):
		u1 = lfsr(c1, [int(i) for i in '{0:013b}'.format(init_state)], key_stream_length)
		hamming_distance = np.count_nonzero(u1!=key_stream)
		correlation = 1 - hamming_distance/key_stream_length
		est_correlations_1.append(correlation)
		
	est_correlations_np = np.array(est_correlations_1)	
	#plt.plot(np.array([i for i in range(1,2**13)]), est_correlations_np) 
	#plt.show()
	
	print(f'Estimated initial state 1: {max(est_correlations_1)}')
	
	c1_init_state = est_correlations_1.index(max(est_correlations_1)) + 1
	
	est_correlations_2 = []
	for init_state in range(1, 2**15):
		u2 = np.array(lfsr(c2, [int(i) for i in '{0:015b}'.format(init_state)], key_stream_length))
		hamming_distance = np.count_nonzero(u2!=key_stream)
		correlation = 1 - hamming_distance/key_stream_length
		est_correlations_2.append(correlation)	
	
	est_correlations_np = np.array(est_correlations_2)	
	plt.plot(np.array([i for i in range(1,2**15)]), est_correlations_np) 	
	plt.show()

	print(f'Estimated initial state 2: {max(est_correlations_2)}')
	
	c2_init_state = est_correlations_2.index(max(est_correlations_2)) + 1
	
	est_correlations_3 = []
	for init_state in range(1, 2**17):
		u3 = np.array(lfsr(c3, [int(i) for i in '{0:017b}'.format(init_state)], key_stream_length))
		hamming_distance = np.count_nonzero(u3!=key_stream)
		correlation = 1 - hamming_distance/key_stream_length
		est_correlations_3.append(correlation)	
	est_correlations_np = np.array(est_correlations_3)	
	# plt.plot(np.array([i for i in range(1,2**17)]), est_correlations_np) 	
	# plt.show()
	print(f'Estimated initial state 3: {max(est_correlations_3)}')
	
	c3_init_state = est_correlations_3.index(max(est_correlations_3)) + 1
	
	u1 = np.array(lfsr(c1, [int(i) for i in '{0:013b}'.format(c1_init_state)], key_stream_length))
	u2 = np.array(lfsr(c2, [int(i) for i in '{0:015b}'.format(c2_init_state)], key_stream_length))
	u3 = np.array(lfsr(c3, [int(i) for i in '{0:017b}'.format(c3_init_state)], key_stream_length))
	
	sequence = majority_function([u1,u2,u3])
	print("".join([str(elem) for elem in sequence]))
	print(key_stream_str)
