#!/usr/bin/env python
# coding: utf-8
# =============================================================================
# Sigma Jupyter Widget
# =============================================================================
#
#
from ipywidgets import DOMWidget, Output
from ipywidgets.embed import embed_minimal_html
from IPython.display import Image, display
from traitlets import Unicode, Dict, Int, Bool, Tuple, List
from collections.abc import Sequence, Mapping, Iterable
from ._frontend import module_name, module_version

from ipysigma.interfaces import get_graph_interface

# =============================================================================
# Constants
# =============================================================================
MAX_CATEGORY_COLORS = 10
DEFAULT_HEIGHT = 500
DEFAULT_NODE_SIZE_RANGE = (3, 15)
DEFAULT_EDGE_SIZE_RANGE = (0.5, 10)
DEFAULT_CAMERA_STATE = {"ratio": 1, "x": 0.5, "y": 0.5, "angle": 0}
SUPPORTED_NODE_TYPES = (int, str, float)
SUPPORTED_RANGE_BOUNDS = (int, str, float)
SUPPORTED_NODE_METRICS = {"louvain"}
SUPPORTED_UNDIRECTED_EDGE_TYPES = {"line", "slim"}
SUPPORTED_DIRECTED_EDGE_TYPES = SUPPORTED_UNDIRECTED_EDGE_TYPES | {"arrow", "triangle"}


# =============================================================================
# Helpers
# =============================================================================
def pretty_print_int(v):
    return "{:,}".format(int(v))


def extract_rgba_from_viz(viz_color):
    if "a" in viz_color:
        return "rgba(%s, %s, %s, %s)" % (
            viz_color["r"],
            viz_color["g"],
            viz_color["b"],
            viz_color["a"],
        )

    return "rgba(%s, %s, %s)" % (
        viz_color["r"],
        viz_color["g"],
        viz_color["b"],
    )


def is_indexable(value):
    return (
        not isinstance(value, (str, bytes))
        and hasattr(value, "__getitem__")
        and callable(value.__getitem__)
    )


def is_partition(value):
    return (
        isinstance(value, list)
        and len(value) > 0
        and isinstance(value[0], (set, frozenset, list))
    )


def resolve_metrics(name, target, supported):
    if not target:
        return {}

    if isinstance(target, Sequence) and not isinstance(target, (str, bytes)):
        metrics = {}

        for v in target:
            spec = v

            if isinstance(v, str):
                spec = {"name": v}

            metrics[spec["name"]] = spec

    elif isinstance(target, Mapping):
        metrics = {}

        for k, v in target.items():
            spec = v

            if isinstance(v, str):
                spec = {"name": v}

            metrics[k] = spec
    else:
        raise TypeError(
            name
            + " should be a list of metrics to compute or a dict mapping metric names to attribute names"
        )

    for v in metrics.values():
        metric_name = v["name"]
        if metric_name not in supported:
            raise TypeError(
                'unknown %s "%s", expecting one of %s'
                % (name, metric_name, ", ".join('"%s"' % m for m in supported))
            )

    return metrics


def resolve_range(name, target):
    if target is None:
        return

    if isinstance(target, SUPPORTED_RANGE_BOUNDS):
        return (target, target)

    if (
        isinstance(target, Sequence)
        and len(target) == 2
        and isinstance(target[0], SUPPORTED_RANGE_BOUNDS)
        and isinstance(target[1], SUPPORTED_RANGE_BOUNDS)
    ):
        if isinstance(target[0], str) and not isinstance(target[1], str):
            raise TypeError(name + " contain mixed type (min, max) info")

        return target

    raise TypeError(
        name + " should be a single value or a (min, max) sequence (list, tuple etc.)"
    )


def resolve_variable_kwarg(
    items, variable, name, target, item_type="node", is_directed=True
):

    # Partition
    if is_partition(target):
        partition = target
        target = {}

        for i, group in enumerate(partition):
            for item in group:
                target[item] = i

    # Attribute name
    if isinstance(target, str):
        variable["attribute"] = target

    # Mappping
    # NOTE: must be used before callable to handle stuff like g.degree
    elif is_indexable(target):
        mapping = target
        target = "$$%s" % name

        for item in items:
            if item_type == "node":
                try:
                    v = mapping[item["key"]]
                except (IndexError, KeyError):
                    v = None
            else:
                try:
                    v = mapping[(item["source"], item["target"])]
                except (IndexError, KeyError):
                    if not is_directed:
                        try:
                            v = mapping[(item["target"], item["source"])]
                        except (IndexError, KeyError):
                            v = None
                    else:
                        v = None

            if v is None:
                continue

            item["attributes"][target] = v

        variable["attribute"] = target

    # Callable
    elif callable(target):
        mapping = target
        target = "$$%s" % name

        for item in items:
            if item_type == "node":
                v = mapping(item["key"], item["attributes"])
            else:
                v = mapping(item["source"], item["target"], item["attributes"])

            if v is None:
                continue

            item["attributes"][target] = v

        variable["attribute"] = target

    # Fail
    else:
        raise TypeError(
            "%s should be an attribute name, or a mapping, or a partition, or a function"
            % name
        )


def check_zindex_int_return(fn):
    def wrapper(*args):
        z = fn(*args)

        if not isinstance(z, int):
            raise TypeError("zindex values should be None or an int")

        return z

    return wrapper


def zindex_sort_items(items, sorter, item_type="node", is_directed=True):
    if callable(sorter):

        def key(*args):
            return sorter(*args) or 0

    elif is_indexable(sorter):
        if item_type == "node":

            def key(n, _):
                return sorter.get(n) or 0

        else:

            def key(u, v, _):
                z = sorter.get((u, v))

                if z is None and not is_directed:
                    z = sorter.get((v, u))

                if not z:
                    z = 0

                return z

    else:
        if item_type == "node":

            def key(_, a):
                return a.get(sorter) or 0

        else:

            def key(_u, _v, a):
                return a.get(sorter) or 0

    safe_key = check_zindex_int_return(key)

    if item_type == "node":

        def item_key(item):
            return safe_key(item["key"], item["attributes"])

    else:

        def item_key(item):
            return safe_key(item["source"], item["target"], item["attributes"])

    items.sort(key=item_key)


def process_node_gexf_viz(attr):
    if "viz" not in attr:
        return

    viz = attr["viz"]

    # Size
    if "size" in viz and "size" not in attr:
        attr["size"] = viz["size"]

    # Position
    if "position" in viz and "x" not in attr and "y" not in attr:
        pos = viz["position"]

        if "x" in pos:
            attr["x"] = pos["x"]

        if "y" in pos:
            attr["y"] = pos["y"]

    # Color
    if "color" in viz and "color" not in attr:
        attr["color"] = extract_rgba_from_viz(viz["color"])

    del attr["viz"]


def process_edge_gexf_viz(attr):
    if "viz" not in attr:
        return

    viz = attr["viz"]

    # Thickness
    if "thickness" in viz and "size" not in attr:
        attr["size"] = viz["thickness"]

    # Color
    if "color" in viz and "color" not in attr:
        attr["color"] = extract_rgba_from_viz(viz["color"])

    del attr["viz"]


# =============================================================================
# Widget definition
# =============================================================================
class Sigma(DOMWidget):
    """
    Jupyter widget displaying an interactive interface that can be used to
    explore the given networkx graph using sigma.js.

    Args:
        graph (nx.Graph or nx.DiGraph or nx.MultiGraph or nx.MultiDiGraph):
            networkx graph to explore.
        height (int, optional): height of the widget in pixels. Cannot be less
            than 250px. Defaults to 500.
        start_layout (bool, optional): whether to automatically start the
            provided ForceAtlas2 layout when the widget is displayed.
            Defaults to False.
        node_color (str, optional): name of the node attribute that should
            be interpreted as a category to be used for node color. Note that
            a suitable color palette will be automatically generated for you.
            Defaults to None, i.e. will read the "color" attribute of nodes
            directly or use a grey color if none is to be found.
        node_size (str, optional): name of the node attribute that should be
            used for node size. Note the provided size is scaled using
            the range provided by the `node_size_range` kwarg.
            Defaults to "size".
        node_size_range ((number, number), optional): range for node size
            interpolation. Defaults to (2, 12).
        node_label (str, optional): name of the node attribute that will be used
            as node label. Defaults to "label".
        edge_color (str, optional): name of the edge attribute that should
            be interpreted as a category to be used for edge color. Note that
            a suitable color palette will be automatically generated for you.
            Defaults to None, i.e. will read the "color" attribute of edges
            directly or use a light grey color if none is to be found.
        edge_size (str, optional): name of the edge attribute that should be
            used for edge size. Note the provided size is scaled using
            the range provided by the `edge_size_range` kwarg.
            Defaults to "size".
        edge_size_range ((number, number), optional): range for edge size
            interpolation. Defaults to (0.5, 10).
        edge_label (str, optional): name of the edge attribute that will be used
            as edge label. Defaults to None, i.e. no label.
        camera_state (dict, optional): camera state of the widget, which is a dict
            of shape {x, y, ratio, angle}. Can be retrieved using the `get_camera_state`
            method. Defaults to {x: 0.65, y: 0.5, ratio: 1, angle: 0}.
        layout (dict, optional): dict mapping nodes to {x, y} positions.
            Defaults to None.
        layout_settings (dict, optional): settings for ForceAtlas2 layout.
            Defaults to None, i.e. using default settings.
        clickable_edges (bool, optional): whether to enable edge events so you can
            click on them to get information. This can be costly on large graphs.
            Defaults to False.
        process_gexf_viz (bool, optional): whether to process "viz" data typically
            found in gexf files so they can be displayed correctly.
            Defaults to True.
    """

    _model_name = Unicode("SigmaModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("SigmaView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    data = Dict({"nodes": [], "edges": []}).tag(sync=True)
    height = Int(DEFAULT_HEIGHT).tag(sync=True)
    start_layout = Bool(False).tag(sync=True)
    clickable_edges = Bool(False).tag(sync=True)
    snapshot = Unicode(allow_none=True).tag(sync=True)
    layout = Dict(allow_none=True).tag(sync=True)
    camera_state = Dict(DEFAULT_CAMERA_STATE).tag(sync=True)
    layout_settings = Dict(allow_none=True).tag(sync=True)
    node_metrics = Dict({}).tag(sync=True)
    edge_weight = Unicode(allow_none=True).tag(sync=True)
    selected_node = Unicode(allow_none=True).tag(sync=True)
    selected_edge = Tuple(allow_none=True).tag(sync=True)
    selected_node_category_values = List(allow_none=True).tag(sync=True)
    selected_edge_category_values = List(allow_none=True).tag(sync=True)
    sync_key = Unicode(allow_none=True).tag(sync=True)
    renderer_settings = Dict(
        {
            "labelGridCellSize": 250,
            "labelDensity": 1,
        }
    ).tag(sync=True)
    max_category_colors = Int(MAX_CATEGORY_COLORS).tag(sync=True)
    program_settings = Dict({"nodeBorderRatio": 0.1}).tag(sync=True)
    visual_variables = Dict(
        {
            "nodeLabel": {"type": "raw", "attribute": "label"},
            "nodeColor": {"type": "raw", "attribute": "color", "default": "#999"},
            "nodeBorderColor": {"type": "disabled"},
            "nodeSize": {
                "type": "continuous",
                "attribute": "size",
                "range": DEFAULT_NODE_SIZE_RANGE,
            },
            "edgeLabel": {"type": "disabled"},
            "edgeColor": {"type": "raw", "attribute": "color", "default": "#ccc"},
            "edgeSize": {
                "type": "continuous",
                "attribute": "size",
                "range": DEFAULT_EDGE_SIZE_RANGE,
            },
        }
    ).tag(sync=True)

    def __init__(
        self,
        graph,
        *,
        height=DEFAULT_HEIGHT,
        start_layout=False,
        node_color=None,
        node_raw_color="color",
        node_color_gradient=None,
        node_color_palette=None,
        default_node_color="#999",
        node_borders=False,
        node_border_color=None,
        node_raw_border_color="borderColor",
        node_border_color_gradient=None,
        node_border_color_palette=None,
        default_node_border_color="#fff",
        node_border_ratio=0.1,
        node_size="size",
        node_size_range=DEFAULT_NODE_SIZE_RANGE,
        node_label="label",
        node_metrics=None,
        node_zindex=None,
        edge_color=None,
        edge_raw_color="color",
        edge_color_gradient=None,
        edge_color_from=None,
        edge_color_palette=None,
        default_edge_color="#ccc",
        default_edge_type=None,
        edge_size="size",
        edge_size_range=DEFAULT_EDGE_SIZE_RANGE,
        edge_label=None,
        edge_weight="weight",
        edge_zindex=None,
        camera_state=DEFAULT_CAMERA_STATE,
        selected_node=None,
        selected_edge=None,
        selected_node_category_values=None,
        selected_edge_category_values=None,
        layout=None,
        layout_settings=None,
        clickable_edges=False,
        process_gexf_viz=True,
        label_density=1,
        label_grid_cell_size=250,
        label_rendered_size_threshold=None,
        max_category_colors=MAX_CATEGORY_COLORS,
        sync_key=None
    ):
        super(Sigma, self).__init__()

        # Validation
        if height < 250:
            raise TypeError("Sigma widget cannot have a height < 250 px")

        if not isinstance(max_category_colors, int) or max_category_colors < 0:
            raise TypeError("max_category_colors should be a positive integer")

        if selected_node is not None and selected_edge is not None:
            raise TypeError(
                "selected_node and selected_edge cannot be given at the same time"
            )

        if selected_node is not None:
            if not isinstance(selected_node, SUPPORTED_NODE_TYPES):
                raise TypeError("selected_node should be str, int or float")

            if selected_node not in graph:
                raise KeyError("selected_node does not exist in the graph")

        if selected_edge is not None:
            if (
                not isinstance(selected_edge, tuple)
                or len(selected_edge) != 2
                or not isinstance(selected_edge[0], SUPPORTED_NODE_TYPES)
                or not isinstance(selected_edge[1], SUPPORTED_NODE_TYPES)
            ):
                raise TypeError("selected_edge should be a (source, target) tuple")

            if not self.graph_interface.has_edge(*selected_edge):
                raise KeyError("selected_edge does not exist in the graph")

        if selected_node_category_values is not None and not isinstance(
            selected_node_category_values, Iterable
        ):
            raise TypeError(
                "selected_node_category_values should be an iterable of node keys"
            )

        if selected_edge_category_values is not None and not isinstance(
            selected_edge_category_values, Iterable
        ):
            raise TypeError(
                "selected_edge_category_values should be an iterable of edge keys"
            )

        node_size_range = resolve_range("node_size_range", node_size_range)
        node_color_gradient = resolve_range("node_color_gradient", node_color_gradient)
        node_border_color_gradient = resolve_range(
            "node_border_color_gradient", node_border_color_gradient
        )
        edge_size_range = resolve_range("edge_size_range", edge_size_range)
        edge_color_gradient = resolve_range("edge_color_gradient", edge_color_gradient)

        # Own
        self.graph = graph
        self.graph_interface = get_graph_interface(self.graph)

        # Traits
        self.height = height
        self.max_category_colors = max_category_colors
        self.start_layout = start_layout
        self.snapshot = None
        self.layout = None
        self.layout_settings = layout_settings
        self.clickable_edges = clickable_edges
        self.camera_state = camera_state
        self.selected_node = str(selected_node) if selected_node else None
        self.selected_edge = (
            (str(selected_edge[0]), str(selected_edge[1])) if selected_edge else None
        )
        self.selected_node_category_values = (
            list(selected_node_category_values)
            if selected_node_category_values
            else None
        )
        self.selected_edge_category_values = (
            list(selected_edge_category_values)
            if selected_edge_category_values
            else None
        )
        self.node_metrics = resolve_metrics(
            "node_metrics", node_metrics, SUPPORTED_NODE_METRICS
        )

        if layout is not None:
            if not isinstance(layout, dict):
                raise TypeError(
                    "layout should be a dict from nodes to {x, y} positions"
                )

            self.layout = layout

        is_directed = self.graph_interface.is_directed()
        is_multi = self.graph_interface.is_multi()

        # Serializing graph as per graphology's JSON format
        principal_component = None

        nodes = []
        self.node_type = None

        for node, attr in self.graph_interface.nodes():
            if principal_component and node not in principal_component:
                continue

            if self.node_type is None:
                self.node_type = type(node)

                if not isinstance(node, SUPPORTED_NODE_TYPES):
                    raise TypeError(
                        "ipysigma does not support graph with node keys which are not str, int or float (found a %s key)"
                        % self.node_type.__name__
                    )
            elif type(node) is not self.node_type:
                raise TypeError(
                    "ipysigma does not support mixed types for node keys (found %s and %s)"
                    % (self.node_type.__name__, type(node).__name__)
                )

            attr = attr.copy()

            if process_gexf_viz:
                process_node_gexf_viz(attr)

            serialized_node = {"key": node, "attributes": attr}

            nodes.append(serialized_node)

        edges = []

        for source, target, attr in self.graph_interface.edges():
            if principal_component and source not in principal_component:
                continue

            attr = attr.copy()

            if process_gexf_viz:
                process_edge_gexf_viz(attr)

            # NOTE: networkx multigraph can have keys on edges, but they
            # are not required to be unique across the graph, which makes
            # them pointless for graphology, gexf etc.
            serialized_edge = {"source": source, "target": target, "attributes": attr}

            if not is_directed:
                serialized_edge["undirected"] = True

            edges.append(serialized_edge)

        # Serializing visual variables
        visual_variables = self.visual_variables.copy()

        # Nodes
        if node_color is not None:
            variable = {"type": "category"}

            resolve_variable_kwarg(
                nodes,
                variable,
                "node_color",
                node_color,
                item_type="node",
                is_directed=self.graph_interface.is_directed(),
            )

            visual_variables["nodeColor"] = variable

            if node_color_palette is not None:
                if not isinstance(node_color_palette, Mapping):
                    raise TypeError(
                        "node_color_palette should be a mapping (i.e. a dict)"
                    )

                variable["palette"] = list(node_color_palette.items())

            elif node_color_gradient is not None:
                variable["type"] = "continuous"
                variable["range"] = node_color_gradient

        elif node_raw_color is not None:
            visual_variables["nodeColor"]["attribute"] = node_raw_color

        visual_variables["nodeColor"]["default"] = default_node_color

        if node_borders:
            visual_variables["nodeBorderColor"] = {
                "type": "raw",
                "attribute": node_raw_border_color,
            }

            if node_border_color is not None:
                variable = {"type": "category"}

                resolve_variable_kwarg(
                    nodes,
                    variable,
                    "node_border_color",
                    node_border_color,
                    item_type="node",
                    is_directed=self.graph_interface.is_directed(),
                )

                visual_variables["nodeBorderColor"] = variable

                if node_border_color_palette is not None:
                    if not isinstance(node_border_color_palette, Mapping):
                        raise TypeError(
                            "node_border_color_palette should be a mapping (i.e. a dict)"
                        )

                    variable["palette"] = list(node_border_color_palette.items())

                elif node_border_color_gradient is not None:
                    variable["type"] = "continuous"
                    variable["range"] = node_border_color_gradient

            elif node_raw_border_color is not None:
                visual_variables["nodeBorderColor"]["attribute"] = node_raw_border_color

            visual_variables["nodeBorderColor"]["default"] = default_node_border_color

        if node_size is not None:
            variable = {"type": "continuous", "range": node_size_range}

            resolve_variable_kwarg(
                nodes,
                variable,
                "node_size",
                node_size,
                item_type="node",
                is_directed=self.graph_interface.is_directed(),
            )

            visual_variables["nodeSize"] = variable

        if node_label is not None:
            variable = {"type": "raw"}

            resolve_variable_kwarg(
                nodes,
                variable,
                "node_label",
                node_label,
                item_type="node",
                is_directed=self.graph_interface.is_directed(),
            )

            visual_variables["nodeLabel"] = variable

        # Edges
        if edge_color is not None:
            variable = {"type": "category"}

            resolve_variable_kwarg(
                edges,
                variable,
                "edge_color",
                edge_color,
                item_type="edge",
                is_directed=self.graph_interface.is_directed(),
            )

            visual_variables["edgeColor"] = variable

            # Palette?
            if edge_color_palette is not None:
                if not isinstance(edge_color_palette, Mapping):
                    raise TypeError(
                        "edge_color_palette should be a mapping (i.e. a dict)"
                    )

                variable["palette"] = list(edge_color_palette.items())

            elif edge_color_gradient is not None:
                variable["type"] = "continuous"
                variable["range"] = edge_color_gradient

        elif edge_color_from is not None:
            if not self.graph_interface.is_directed():
                raise TypeError("edge_color_from only works with directed graphs")

            if edge_color_from not in ["source", "target"]:
                raise TypeError('edge_color_from should be "source" or "target"')

            visual_variables["edgeColor"] = {
                "type": "dependent",
                "value": edge_color_from,
            }

        elif edge_raw_color is not None:
            visual_variables["edgeColor"]["attribute"] = edge_raw_color

        visual_variables["edgeColor"]["default"] = default_edge_color

        if edge_size is not None:
            variable = {"type": "continuous", "range": edge_size_range}

            resolve_variable_kwarg(
                edges,
                variable,
                "edge_size",
                edge_size,
                item_type="edge",
                is_directed=self.graph_interface.is_directed(),
            )

            visual_variables["edgeSize"] = variable

        if edge_label is not None:
            variable = {"type": "raw"}

            resolve_variable_kwarg(
                edges,
                variable,
                "edge_label",
                edge_label,
                item_type="edge",
                is_directed=self.graph_interface.is_directed(),
            )

            visual_variables["edgeLabel"] = variable

        if edge_weight is not None:
            variable = {"type": "raw"}

            resolve_variable_kwarg(
                edges,
                variable,
                "edge_weight",
                edge_weight,
                item_type="edge",
                is_directed=self.graph_interface.is_directed(),
            )

            self.edge_weight = variable["attribute"]
        else:
            self.edge_weight = None

        self.visual_variables = visual_variables

        # Handling z-index
        if node_zindex is not None:
            zindex_sort_items(
                nodes, node_zindex, item_type="node", is_directed=is_directed
            )

        if edge_zindex is not None:
            zindex_sort_items(
                edges, edge_zindex, item_type="edge", is_directed=is_directed
            )

        # Building renderer settings
        renderer_settings = {
            "labelDensity": label_density,
            "labelGridCellSize": label_grid_cell_size,
        }

        if label_rendered_size_threshold is not None:
            renderer_settings[
                "labelRenderedSizeThreshold"
            ] = label_rendered_size_threshold

        if default_edge_type is not None:
            if is_directed and default_edge_type not in SUPPORTED_DIRECTED_EDGE_TYPES:
                raise TypeError(
                    'unsupported edge type "%s" for directed graphs' % default_edge_type
                )

            if (
                not is_directed
                and default_edge_type not in SUPPORTED_UNDIRECTED_EDGE_TYPES
            ):
                raise TypeError(
                    'unsupported edge type "%s" for undirected graphs'
                    % default_edge_type
                )

            renderer_settings["defaultEdgeType"] = default_edge_type

        self.renderer_settings = renderer_settings

        # Building webgl program settings
        self.program_settings = {"nodeBorderRatio": node_border_ratio}

        self.data = {
            "nodes": nodes,
            "edges": edges,
            "options": {
                "type": "directed" if is_directed else "undirected",
                "multi": is_multi,
            },
        }

        self.sync_key = sync_key

    def __repr__(self):
        return "Sigma(%s with %s nodes and %s edges)" % (
            self.graph_interface.name(),
            pretty_print_int(self.graph_interface.order()),
            pretty_print_int(self.graph_interface.size()),
        )

    def get_layout(self):
        """
        Method returning the layout computed by ForceAtlas2 in the widget.

        Note that if the layout was never displayed, this method will return None.

        Also note that if you never ran the layout this method will return the
        initial layout that will be random in the [0, 1) range if you did not
        provide starting positions yourself.

        Returns:
            dict: a dictionary mapping node keys to {x, y} positions.
        """
        if self.layout is None:
            return None

        return {self.node_type(n): p for n, p in self.layout.items()}

    def get_camera_state(self):
        """
        Method returning the current camera state of the widget.
        """
        return self.camera_state

    def get_selected_node(self):
        if self.selected_node is not None:
            return self.node_type(self.selected_node)

    def get_selected_edge(self):
        if self.selected_edge is not None:
            return (
                self.node_type(self.selected_edge[0]),
                self.node_type(self.selected_edge[1]),
            )

    def get_selected_node_category_values(self):
        return self.selected_node_category_values

    def get_selected_edge_category_values(self):
        return self.selected_edge_category_values

    def render_snapshot(self):
        """
        Method rendering and displaying a snasphot of the widget.

        This can be useful to save a version of the widget that can actually
        be seen in a static rendition of your notebook (when using nbconvert,
        for instance, or when reading the notebook on GitHub).

        Returns:
            Ipython.display.HTML: the snasphot as a data url in an img tag.
        """

        out = Output()
        out.append_stdout(
            "Rendering snapshot from widget (are you sure the widget is currently displayed?)..."
        )

        def on_update(change):
            if change.new is None:
                return

            out.clear_output()

            with out:
                display(Image(url=change.new))

            self.unobserve(on_update, "snapshot")

        self.observe(on_update, "snapshot")
        self.send({"msg": "render_snapshot"})

        return out

    def save_as_html(self, path, **kwargs):

        # Snapshot data unnecessarily adds weight here, let's drop it
        current_snapshot = self.snapshot
        self.snapshot = None

        embed_minimal_html(path, views=[self], **kwargs)

        self.snapshot = current_snapshot
