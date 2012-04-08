import itertools

def all_possible_subsets(schema):
    """
        all_possible_subsets(schema) returns str_all_possible
        where str_all_possible is a list of strings 
        where each string is a possible subset of schema
    """
    all_possible = set()
    for i in xrange(1, len(schema) + 1):
        for j in itertools.combinations(schema, i):
            all_possible.add(j)
    str_all_possible = []
    for i in all_possible:
        i = list(i)
        str_all_possible.append("".join(i))
    return str_all_possible

def calc_closure(subset, fds, schema):
    closure = subset
    for i in range(len(fds)):
        for fd in fds:
            if fd[0] in closure:
                if len(fd[1]) > 1:
                    for ch in fd[1]:
                        closure += ch
                else:
                    closure += fd[1]
        # Sort and remove duplicates before next run
        closure = "".join(sorted(set(closure)))
    return closure

def is_superkey(subset, fds, schema):
    closure = calc_closure(subset, fds, schema)
    if closure == schema:
        return True
    else:
        return False

def is_key(s, superkeys):
    s = set(s)
    for superkey in superkeys:
        superkey = set(superkey)
        if superkey.issubset(s) and s != superkey:
            return False
    return True
    

def sort_by_length(x, y):
    if len(x) > len(y):
        return 1
    elif len(x) == len(y):
        return 0
    else:
        return -1


if __name__ == "__main__":
    schema = "ABCDE"
    fds = [("AB", "D"),
           ("D", "C"),
           ("BC", "AD")]

    subsets = all_possible_subsets(schema)
    superkeys = [ subset for subset in subsets if is_superkey(subset, fds, schema) ]
    superkeys.sort(cmp=sort_by_length)
    print "Superkeys:", superkeys

    keys = [ superkey for superkey in superkeys if is_key(superkey, superkeys) ]
    print "Keys:     ", keys

