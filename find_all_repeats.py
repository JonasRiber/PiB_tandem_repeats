def find_repeats(sequence):
    """
    finds all Tandem repeats within a string
    validate it ????
    """
    btrs = []
    n = len(sequence)
    for length in range(1, n // 2 + 1):  #maximum repeat length is n/2
        for i in range(n - 2 * length + 1):  # search each possible pair of repeats
            repeat1 = sequence[i:i+length]
            repeat2 = sequence[i+length:i+2*length]
            if repeat1 == repeat2: # if same, we report it
                btrs.append((sequence[i:i+2*length], length))
    return btrs