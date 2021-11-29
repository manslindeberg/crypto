import os

def LFSR(taps, L, base, prev, isfirst):
    original = [0, 0, 0, 1]

    lfsr = prev

    if isfirst == 1 or not (lfsr == original):
        result = 0
        for x in range(L):
            if taps[x] != 0:
                result = ( result + ( lfsr[x] * taps[x] )) % base
        lfsr.pop(0)
        lfsr.append(result)
    else:
        return [0 for _ in range(L)]
    return lfsr


if __name__ == '__main__':

    taps_5 = [2, 0, 2, 1]
    taps_2 = [1, 0, 0, 1]
    length = 4
    base_5 = 5
    base_2 = 2
    states = []
    prev_2 = [0, 0, 0, 1]
    prev_5 = [0, 0, 0, 1]
    history_2 = []
    history_5 = []
    continu = 1
    isfirst5 = 1

    while continu:
        if prev_5 != [0, 0, 0, 0]:
            prev_2 = [0, 0, 0, 1]
            history_5.append(prev_5.copy())
            isfirst2 = 1
            while prev_2 != [0, 0, 0, 0]:
                states.append([x + y for x, y in zip(prev_2, [x*2 for x in prev_5])])
                prev_2 = LFSR(taps_2, length, base_2, prev_2, isfirst2)
                isfirst2 = 0
                history_2.append(prev_2.copy())
            prev_5 = LFSR(taps_5, length, base_5, prev_5, isfirst5)
            isfirst5 = 0
        else:
            print("avslut")
            continu = 0
        
    #print(f"length h2: {len(history_2)}, len h5 = {len(history_5)}")
    with open("sequences.txt", "w") as seq:
        print(f"Number of states: {len(states)}")
        for index, state in enumerate(states):
            print("state " + str(index) + " = ", state)
            for e in state:
                seq.write(str(e))
            # if index < len(states):
            #     seq.write(" ")