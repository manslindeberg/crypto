

def LFSR(taps, L, base):
    lfsr = [1 for _ in range(L)]
    original = [x for x in lfsr]
    states = []
    i = 0
    while i == 0 or not lfsr == original:
        i = 1
        states.append(str(lfsr))
        result = 0
        for x in range(L):
            if taps[x] != 0: 
                result = ( result + lfsr[x] ) % base
        lfsr.pop(0)
        lfsr.append(result)
        print(lfsr)
    states.append(str([0 for _ in range(L)]))
    return states


if __name__ == '__main__':
    taps = [1, 0, 1, 1]
    length = 4
    base = 5
    states = LFSR(taps, length, base)

    print(f"Number of states: {len(states)}")
    for index, state in enumerate(states):
        print("state " + str(index) + " = ", state)