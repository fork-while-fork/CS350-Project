"""
    Had to modify some of the drawing code to achieve the result that I needed.
"""
def draw_networkx_nodes(G, pos,
                        nodelist=None,
                        node_size=300,
                        node_color='r',
                        node_shape='o',
                        alpha=1.0,
                        cmap=None,
                        vmin=None,
                        vmax=None,
                        ax=None,
                        linewidths=None,
                        **kwds):
    try:
        import matplotlib.pylab as pylab
        import numpy
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise


    if ax is None:
        ax=pylab.gca()

    if nodelist is None:
        nodelist=G.nodes()

    if not nodelist or len(nodelist)==0:  # empty nodelist, no drawing
        return None

    try:
        xy=numpy.asarray([pos[v] for v in nodelist])
    except KeyError as e:
        raise nx.NetworkXError('Node %s has no position.'%e)
    except ValueError:
        raise nx.NetworkXError('Bad value in node positions.')



    node_collection=ax.scatter(xy[:,0], xy[:,1],
                               s=node_size,
                               c=node_color,
                               marker=node_shape,
                               cmap=cmap,
                               vmin=vmin,
                               vmax=vmax,
                               alpha=alpha,
                               linewidths=linewidths,
                               **kwds)

#    pylab.axes(ax)
    pylab.sci(node_collection)
    node_collection.set_zorder(2)
    return node_collection

def draw_networkx_labels(G, pos,
                         labels=None,
                         font_size=12,
                         font_color='k',
                         font_family='sans-serif',
                         font_weight='normal',
                         alpha=1.0,
                         ax=None,
                         **kwds):
    """Draw node labels on the graph G.

    Parameters
    ----------
    G : graph
       A networkx graph 

    pos : dictionary, optional
       A dictionary with nodes as keys and positions as values.
       If not specified a spring layout positioning will be computed.
       See networkx.layout for functions that compute node positions.
       
    font_size : int
       Font size for text labels (default=12)

    font_color : string
       Font color string (default='k' black)

    font_family : string
       Font family (default='sans-serif')

    font_weight : string
       Font weight (default='normal')

    alpha : float
       The text transparency (default=1.0) 

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.  


    Examples
    --------
    >>> G=nx.dodecahedral_graph()
    >>> labels=nx.draw_networkx_labels(G,pos=nx.spring_layout(G))

    Also see the NetworkX drawing examples at
    http://networkx.lanl.gov/gallery.html


    See Also
    --------
    draw()
    draw_networkx()
    draw_networkx_nodes()
    draw_networkx_edges()
    draw_networkx_edge_labels()
    """
    try:
        import matplotlib.pylab as pylab
        import matplotlib.cbook as cb
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        ax=pylab.gca()

    if labels is None:
        labels=dict( (n,n) for n in G.nodes())

    # set optional alignment
    horizontalalignment=kwds.get('horizontalalignment','center')
    verticalalignment=kwds.get('verticalalignment','center')

    text_items={}  # there is no text collection so we'll fake one        
    for n, label in labels.items():
        (x,y)=pos[n]
        y -= 0.1
        if not cb.is_string_like(label):
            label=str(label) # this will cause "1" and 1 to be labeled the same
        t=ax.text(x, y,
                  label,
                  size=font_size,
                  color=font_color,
                  family=font_family,
                  weight=font_weight,
                  horizontalalignment=horizontalalignment,
                  verticalalignment=verticalalignment,
                  transform = ax.transData,
                  clip_on=True,
                  )
        text_items[n]=t

    return text_items
