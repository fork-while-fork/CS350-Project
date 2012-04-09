import networkx as nx
import matplotlib.pyplot as plt
import draw_nodes as dn
import closures as c

def draw(nodelist, superkeys, keys):
    DG = nx.DiGraph()
    for node in nodelist:
        DG.add_node(node)
    DG.add_edge("A", "ABC")
    print dir(DG)

    #nodelist.sort(cmp=sort_by_length)
    lengths = set([ len(node) for node in nodelist ])
    d = {}
    for length in lengths:
        d[length] = [ node for node in nodelist if len(node) == length ]

    max_length = max(d.iterkeys())
    max_nodelist_length = max([ len(nodelist) for nodelist in d.itervalues() ])

    superkey_pos = {}
    key_pos = {}
    other_pos = {}
    master_pos = {}
    for i in xrange(1, 1+max_length):
        for node in d[i]:
            offset = (max_length - len(d[i]))  / 2.0
            master_pos[node] = [d[i].index(node) + offset, i]
            if node in keys:
                key_pos[node] = [d[i].index(node) + offset, i]
            elif node in superkeys:
                superkey_pos[node] = [d[i].index(node) + offset, i]
            else:
                other_pos[node] = [d[i].index(node) + offset, i]

    global_draw_args = {
                        "alpha": 0.25,
                        "node_shape": "s",
                        "edgecolors": "none",
                        "node_size": 2000
                       }
    plt.figure(1, [11, 8.5])

    dn.draw_networkx_nodes(DG, pos=superkey_pos, node_color="#0000FF", nodelist=superkeys, label="Superkey", **global_draw_args)
    dn.draw_networkx_nodes(DG, pos=key_pos, node_color="#FF0000", nodelist=keys, label="Key", **global_draw_args)
    dn.draw_networkx_nodes(DG, pos=other_pos, node_color="#AAAAAA", nodelist=list(other_pos.iterkeys()), label="Other", **global_draw_args)
    nx.draw_networkx_labels(DG, pos=master_pos)

    plt.legend(scatterpoints=1)
    plt.show()


if __name__ == "__main__":
    superkeys, keys = c.main()
    draw(c.all_possible_subsets("ABCDE"), superkeys, keys)
