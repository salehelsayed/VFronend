import networkx as nx
import numpy as np
from bokeh.io import show, output_file
from bokeh.plotting import figure, from_networkx
from bokeh.models import (
    MultiLine, Circle, HoverTool, TapTool, BoxSelectTool,
    LabelSet, ColumnDataSource
)

output_file("graph.html")

G = nx.MultiGraph()
G.add_edge('A', 'B')
G.add_edge('A', 'B')
G.add_edge('A', 'C')
G.add_edge('B', 'C')
G.add_edge('C', 'D')
G.add_edge('D', 'A')
G.add_edge('E', 'A')
G.add_edge('E', 'B')
G.add_edge('E', 'C')
G.add_edge('E', 'D')

# Using figure with plot_width and plot_height
plot = figure(
    width=800, height=800,
    x_range=(-2, 2), y_range=(-2, 2),
    tools="hover,tap,box_select",
    tooltips=[("Node", "@index")]
)

graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))

graph_renderer.node_renderer.glyph = Circle(radius=10, radius_units='screen', fill_color='skyblue')
graph_renderer.edge_renderer.glyph = MultiLine(line_color="gray", line_alpha=0.8, line_width=2)

plot.renderers.append(graph_renderer)

nodes = list(G.nodes())
x = np.array([graph_renderer.layout_provider.graph_layout[node][0] for node in nodes])
y = np.array([graph_renderer.layout_provider.graph_layout[node][1] for node in nodes])

source = ColumnDataSource({'x': x, 'y': y, 'name': nodes})

labels = LabelSet(
    x='x', y='y', text='name', source=source,
    background_fill_color='white', text_align='center'
)
plot.add_layout(labels)

show(plot)
