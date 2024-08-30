

### Brute force approach to finding tandem repeats in a sequence 
## By Jonas Riber Jørgensen, 2024

def brute_force_tandem_repeats(s):
    """
    Finds tandem repeats in a given string using an iterative approach.
    Finds all the possible repeats and their given lengths and positions. 
    So it runs in O(n^3). A faster version where length not checked can run in O(n^2).

    Args:
        s (str): The input string.
    Returns:
        A list of tuples where each tuple represents a tandem repeat in the format (substring, #repeats l, starting_index).

    Doctest examples:
        >>> brute_force_tandem_repeats("abcabcabcabcxyzxyz")
        [('abc', 4, 0), ('bca', 3, 1), ('cab', 3, 2), ('abc', 3, 3), ('bca', 2, 4), ('cab', 2, 5), ('abc', 2, 6), ('xyz', 2, 12), ('abcabc', 2, 0)]
        >>> brute_force_tandem_repeats("tatat")
        [('ta', 2, 0), ('at', 2, 1)]
        >>> brute_force_tandem_repeats("aaaaaaaa")
        [('aa', 4, 0), ('aa', 3, 1), ('aa', 3, 2), ('aa', 2, 3), ('aa', 2, 4), ('aaa', 2, 0), ('aaa', 2, 1), ('aaa', 2, 2), ('aaaa', 2, 0)]
    """
    n = len(s)
    repeats = []

    # iterating over all possible lengths within the string (potentially limit the pattern size?)
    for length in range(2, n // 2 + 1):
        # check each position as starting point
        for i in range(n - 2 * length + 1):
            substring = s[i:i + length]
            count = 0
            pos = i
            
            # count repeat consecutively
            while pos + length <= n and s[pos:pos + length] == substring: # we dont exceed n and substring matches
                count += 1
                pos += length
            
            # add to results if it repeats
            if count > 1:
                repeats.append((substring, count, i))

    return repeats