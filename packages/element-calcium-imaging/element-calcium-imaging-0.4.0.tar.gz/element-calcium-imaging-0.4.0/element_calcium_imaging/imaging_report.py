import datajoint as dj
from .plotting import cell_plot

schema = dj.Schema()

imaging = None


def activate(
    schema_name, imaging_schema_name, *, create_schema=True, create_tables=True
):
    """Activate this schema

    Args:
        schema_name (str): schema name on the database server to activate the `imaging_report` schema
        imaging_schema_name (str): schema name of the activated imaging element for which this imaging_report schema will be downstream from
        create_schema (bool): When True (default), create schema in the database if it does not yet exist.
        create_tables (bool): When True (default), create tables in the database if they do not yet exist.

    Note:
        "activation" of this imaging_report module should be evoked by one of the imaging modules only
    """
    global imaging
    imaging = dj.create_virtual_module("imaging", imaging_schema_name)

    schema.activate(
        schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=imaging.__dict__,
    )


@schema
class ScanLevelReport(dj.Computed):
    """Grayscale plotly figure of average scan with cells shown atop transparently in color.
    Figures are stored in the JSON string format."""

    definition = """
    -> imaging.Segmentation
    ---
    cell_overlayed_image: longblob
    """

    def make(self, key):
        image_fig = cell_plot.plot_cell_overlayed_image(imaging, key)
        self.insert1({**key, "cell_overlayed_image": image_fig.to_json()})


@schema
class TraceReport(dj.Computed):
    """Activity trace (Fluorescence, dff) figures. Figures are stored in the JSON string format."""

    definition = """
    -> imaging.Segmentation.Mask
    ---
    cell_traces: longblob
    """

    def make(self, key):
        trace_fig = cell_plot.plot_cell_traces(imaging, key)
        self.insert1({**key, "cell_traces": trace_fig.to_json()})
