

def LFSR(taps, L, base, prev):
    original = [0 for _ in range(L)]
    original[L-1] = 1
    if not prev or prev == [0, 0, 0, 0]:
        isfirst = 1
        lfsr = [0 for _ in range(L)]
        lfsr[L-1] = 1
    else:
        lfsr = prev
        isfirst = 0

    if isfirst == 1 or not (lfsr == original):
        result = 0
        for x in range(L):
            if taps[x] != 0: 
                result = ( result + lfsr[x] ) % base
        lfsr.pop(0)
        lfsr.append(result)
    else:
        return [0 for _ in range(L)]
    return lfsr


if __name__ == '__main__':

    nbrStates = 10003
    taps_5 = [1, 0, 1, 1]
    taps_2 = [1, 0, 0, 1]
    length = 4
    base_5 = 5
    base_2 = 2
    states = []
    prev_2 = []
    prev_5 = []

    while len(states) < nbrStates:
        prev_2 = LFSR(taps_2, length, base_2, prev_2)
        prev_5 = LFSR(taps_5, length, base_5, prev_5)
        states.append([x + y for x, y in zip(prev_2, prev_5)])

    print(f"Number of states: {len(states)}")
    for index, state in enumerate(states):
        print("state " + str(index) + " = ", state)