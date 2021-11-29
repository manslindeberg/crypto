import time

def LFSR5(gf: int =  5):
    STATE = [0,0,0,1]
    INIT_STATE = STATE.copy()
    SEQUENCE = []
    STATES = []
    counter = 0

    while True:
        if STATE == INIT_STATE and counter != 0:
            STATE = [0,0,0,0]
            STATES.append(tuple(STATE.copy()))
            SEQUENCE.append(STATE.pop(0))
            break
        else:
            counter +=1
            STATES.append(tuple(STATE.copy()))
            new_val = (2*STATE[0] + 2*STATE[2] + STATE[3]) % gf
            SEQUENCE.append(STATE.pop(0))
            STATE.append(new_val)
    return SEQUENCE

def LFSR2(gf: int =  2):
    STATE = [0,0,0,1]
    INIT_STATE = STATE.copy()
    STATES = []
    SEQUENCE = []
    counter = 0
    while True:
        if STATE == INIT_STATE and counter != 0:
            STATE = [0,0,0,0]
            STATES.append(tuple(STATE.copy()))
            SEQUENCE.append(STATE.pop(0))
            break
        else:
            counter +=1
            STATES.append(tuple(STATE.copy()))
            new_val = (STATE[0] + STATE[3]) % gf
            SEQUENCE.append(STATE.pop(0))
            STATE.append(new_val)
    return SEQUENCE

def is_unique(sequence):
    unique_sequences = []
    for i in range(0, len(sequence) - 3):
        seq = []
        for j in range(0, 4):
            seq.append(sequence[i+j])
        if seq in unique_sequences:
            return False
        else:
            unique_sequences.append(seq)
    return True

if __name__ == '__main__':
    lfsr5 = LFSR5()
    lfsr2 = LFSR2()
    
    lfsrseq2 = []
    lfsrseq5 = []

    seq = "" 
    for i in range(0,626):
        lfsrseq2 += list(lfsr2)
    for i in range(0,17):
        lfsrseq5 += list(lfsr5)
    for i in range(0,10003):
        if lfsrseq2[i] == 1:
            seq +=(str(lfsrseq5[i] + 5))
        else:
            seq+=(str(lfsrseq5[i]))
        f = open("seq.txt", "w")
        f.write(str(seq))
        f.close()
