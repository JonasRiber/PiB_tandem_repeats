

### Brute force approach to finding tandem repeats in a sequence 
## By Jonas Riber Jørgensen, 2024

def brute_force_tandem_repeats(s):
    n = len(s)
    repeats = []

    # iterating over all possible lengths within the string (potentially limit the pattern size?)
    for length in range(1, n // 2 + 1):
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
                repeats.append((substring, count))

    return repeats


#######################
### Testing section ###
#######################

string = "abcabcabcabcxyzxyz"
print(brute_force_tandem_repeats(string))

# [('abc', 4), ('bca', 3), ('cab', 3), ('abc', 3), ('bca', 2), ('cab', 2), ('abc', 2), ('xyz', 2), ('abcabc', 2)]