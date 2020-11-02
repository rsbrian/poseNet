s = [1, 3, 2, 4]


def find_sum(s, t):
    i = 0
    j = len(s) - 1
    while i < j:
        x = s[i] + s[j]
        if x > t:
            j -= 1
        elif x < t:
            i += 1
        else:
            return "Yes"
    return "No"


def find_sum_hash_table(s, t):
    h = []
    for i in range(len(s)):
        if s[i] in h:
            return True
        h.append(s[i])
    return False


sol = find_sum_hash_table(s, 8)
print(sol)
