def find_btr(sequence):
    """
    finds all Tandem repeats within a string
    validate it ????
    """
    btrs = []
    n = len(sequence)
    for length in range(1, n // 2 + 1):  # Maximum repeat length is n/2
        for i in range(n - 2 * length + 1):  # Search each possible pair of repeats
            repeat1 = sequence[i:i+length]
            repeat2 = sequence[i+length:i+2*length]
            # Check if they are the same, allowing for mutations (e.g. up to 1 mutation allowed here)
            if repeat1 == repeat2:  # Allow 1 mutation
                btrs.append((sequence[i:i+2*length], length))
    return btrs