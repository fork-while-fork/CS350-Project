import networkx as nx
import matplotlib.pyplot as plt
import draw_nodes as dn
import closures as c

def draw(nodelist, superkeys, keys, fds):
    DG = nx.DiGraph()
    for node in nodelist:
        DG.add_node(node)
    DG.add_edge("A", "ABC")

    #nodelist.sort(cmp=sort_by_length)
    lengths = set([ len(node) for node in nodelist ])
    d = {}
    for length in lengths:
        d[length] = [ node for node in nodelist if len(node) == length ]

    lengths = list(lengths)
    lengths.sort()
    lengths.remove(lengths[-1])
    print lengths
    important_edges = []
    for length in lengths:
        for node1 in d[length]:
            for node2 in d[length+1]:
                if set(node1).issubset(set(node2)):
                    DG.add_edge(node1, node2)
                    if node1 in keys or node1 in superkeys:
                        important_edges.append((node1, node2))

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

    global_draw_args = { "node_shape": "." }

    plt.figure(1, [11, 8.5])

    nx.draw_networkx_edges(DG, pos=master_pos, arrows=None, edge_color="#AAAAAA", style="dotted")
    nx.draw_networkx_edges(DG, edgelist=important_edges, pos=master_pos, arrows=None, edge_color="#AAAAAA")
    dn.draw_networkx_nodes(DG, pos=superkey_pos, node_color="#0000FF", nodelist=superkeys, label="Superkey", **global_draw_args)
    dn.draw_networkx_nodes(DG, pos=key_pos, node_color="#FF0000", nodelist=keys, label="Key", **global_draw_args)
    dn.draw_networkx_nodes(DG, pos=other_pos, node_color="#FFFFFF", nodelist=list(other_pos.iterkeys()), label="Other", **global_draw_args)
    dn.draw_networkx_labels(DG, pos=master_pos, horizontalalignment="center", verticalalignment="top")

    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    plt.text(xmin + 0.1, ymax - 0.15, r"Functional Dependencies", weight="bold")
    for ypos, fd in enumerate(fds):
        plt.text(xmin + 0.1, ymax - 0.15*(ypos+2), r"%s$\rightarrow$%s" % (fd[0], fd[1]))
    plt.legend(scatterpoints=1)
    plt.yticks([])
    plt.xticks([])
    plt.show()
