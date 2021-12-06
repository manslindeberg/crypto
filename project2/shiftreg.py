

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
            isfirst2 = 1
            history_2 = []
            while prev_2 != [0, 0, 0, 0]:
                temp = []
                for i in range(length):
                    if(prev_2[i] == 1):
                        temp.append(prev_5[i]+5)
                    else:
                        temp.append(prev_5[i])
                states.append(temp)
                prev_2 = LFSR(taps_2, length, base_2, prev_2, isfirst2)
                isfirst2 = 0
                history_2.append(prev_2.copy())
            prev_5 = LFSR(taps_5, length, base_5, prev_5, isfirst5)
            history_5.append(prev_5.copy())
            isfirst5 = 0
        else:
            print("avslut")
            continu = 0
    
    set_sets = set(states)
    print(len(set_sets))

    # unique_list = []
    # duplicates = 0
    # for state in states:
    #     if state in unique_list:
    #         duplicates +=1
    #         print("WTF!?!?")
    #         print(f"duplicate = {state}")
    #     else:
    #         unique_list.append(state)
    # print("duplicates = ", duplicates)

    # print(f"length h2: {len(history_2)}, len h5 = {len(history_5)}")
    # with open("sequences.txt", "w") as seq:
    #     print(f"Number of states: {len(states)}")
    #     while i < 2500:
    #         for index, state in enumerate(states):
    #             if i >= 2504: 
    #                 break
    #             i +=1
    #             print("state " + str(index) + " = ", state)
    #             for element in state:
    #                 seq.write(str(element))
                    