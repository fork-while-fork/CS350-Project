import itertools
import hasse_diagram

def all_possible_subsets(schema):
    """
        schema is a string of the one letter attribute labels and
        str_all_possible is a list of strings 
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
    print len(str_all_possible)
    print str_all_possible
    return str_all_possible

def calc_closure(subset, fds, schema):
    """
        subset is a string of one letter attribute labels
        fds is a list of functional dependencies
        schema is a string of the one letter attribute labels and
    """
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
    """
        subset is a string of one letter attribute labels
        fds is a list of functional dependencies
        schema is a string of the one letter attribute labels and
    """
    closure = calc_closure(subset, fds, schema)
    if closure == schema:
        return True
    else:
        return False

def is_key(s, superkeys):
    """
        subset is a string of one letter attribute labels (which we're testing
            to see if it's a key)
        superkeys is a list of strings where each string is a superkey
    """
    s = set(s)
    for superkey in superkeys:
        superkey = set(superkey)
        if superkey.issubset(s) and s != superkey:
            return False
    return True
    

def sort_by_length(x, y):
    """
        sorts strings in a list by size of the string
    """
    if len(x) > len(y):
        return 1
    elif len(x) == len(y):
        return 0
    else:
        return -1


def main():
    schema = "ABCDE"
    fds = [("AB", "D"),
           ("D", "C"),
           ("BC", "AD")]

    subsets = all_possible_subsets(schema)
    superkeys = [ subset for subset in subsets if is_superkey(subset, fds, schema) ]
    superkeys.sort(cmp=sort_by_length)

    keys = [ superkey for superkey in superkeys if is_key(superkey, superkeys) ]
    keys.sort()
    for key in keys:
        if key in superkeys:
            superkeys.remove(key)

    print "Superkeys:", superkeys
    print "Keys:     ", keys
        
    hasse_diagram.draw(subsets, superkeys, keys, fds)


if __name__ == "__main__":
    main()
