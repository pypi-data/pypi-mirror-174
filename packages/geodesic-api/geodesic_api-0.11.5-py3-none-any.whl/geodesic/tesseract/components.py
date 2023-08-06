import re
import datetime
from typing import List, Union
import warnings
from dateutil.parser import isoparse
import numpy as np
from geodesic.account.projects import ProjectDescr
from geodesic.bases import APIObject
from geodesic.descriptors import BoolDescr, DTypeDescr, DatetimeDescr, DatetimeIntervalDescr, DictDescr, FloatDescr, \
    IntDescr, ListDescr, NumberDescr, RegexDescr, StringDescr, TupleDescr, TypeConstrainedDescr, BaseDescr, \
    URLDescr
from geodesic.entanglement.dataset import Dataset, DatasetDescr
from geodesic.stac import Item, Feature
from geodesic.utils import datetime_to_utc

__all__ = [
    "GlobalProperties",
    "AssetSpec",
    "Container",
    "Step",
    "StepInput",
    "StepOutput",
    "Webhook",
    "Bucket",
    "Equal",
    "User",
    "TemporalBinning",
    "StridedBinning",
    "OutputBand",
    "OutputTimeBins",
    "ReduceMethod",
    "NearestSelection",
    "RangeSelection",
    "BinSelection",
    "TimeBinSelection"
]


bin_size_re = re.compile(r'^\d+(ms|us|ns|[YMWDhms]){1}')


class Equal(APIObject):
    """Temporal binning with equal bin size (either by count or size)
    """
    bin_size = RegexDescr(bin_size_re, doc="the bin size, in time units for each bin")
    bin_count = IntDescr(doc="the count of bins to create")


class User(APIObject):
    """Temporal binning by user specified bins.
    """
    omit_empty = BoolDescr(doc="don't create a space for empty bins in resulting output")

    def __init__(self, **spec):
        self.omit_empty = False
        self._bins = None
        super().__init__(**spec)

    @property
    def bins(self):

        if self._bins is not None:
            return self._bins
        b = self.get('bins', [])
        if not isinstance(b, list):
            raise ValueError("bins must be a list of list of datetimes")
        out = []
        for d in b:
            if d is None:
                raise ValueError("bin cannot be None")
            dates = d
            try:
                out.append([d for d in map(isoparse, dates)])
            except Exception as e:
                raise e
        self._bins = out
        return out

    @bins.setter
    def bins(self, v: List[List[Union[datetime.datetime, str]]]):
        b = []
        for d in v:
            if len(d) != 2:
                raise ValueError("bins must be a list of pairs of start/end datetime bin edges")

            if isinstance(d[0], str):
                for dt in d:
                    try:
                        isoparse(dt)
                    except Exception as e:
                        raise ValueError("bin edges must be datetimes or parsable rfc3339 strings") from e
                b.append(list(d))

            elif isinstance(d[0], datetime.datetime):
                b.append([datetime_to_utc(dt).isoformat() for dt in d])
        self._set_item('bins', b)


class TemporalBinning(APIObject):
    """Temporal binning is a class to represent the temporal binning in a series request.

    Args:
        spec(dict): The dict to initialize the class with.
    """
    equal = TypeConstrainedDescr((Equal, dict), doc="specify Equal time binning")
    user = TypeConstrainedDescr((User, dict), doc="specify time bins defined by User time binning")
    reference = StringDescr(doc="reference the time bins to another asset in the Job")


class Webhook(APIObject):
    """A webhook triggered on completion of a step in a Tesseract Job

    NotImplemented

    A future version of Tesseract will allow webhooks when a job step has completed, which will POST
    information to a url with specified headers and credentials
    """

    url = URLDescr(doc="url")
    headers = DictDescr(doc="dictionary with string keys to string values headers to pass along: {'key': 'value'}")
    credentials = StringDescr(doc="name of the credential to use (geodesic.accounts.Credential)")


class Container(APIObject):
    """A container that runs arbitrary code to execute a model for aggregation, machine learning, etc

    NotImplemented

    """
    repository = StringDescr(doc="the docker repository to pull from", default="docker.io")
    image = StringDescr(doc="the name of the image to use")
    tag = StringDescr(doc="the tag of the image to use")
    pull_secret_credential = StringDescr(doc="name of the credential to use to pull the container")
    args = DictDescr(doc="additional arguments to pass to the inference function (NOT IMPLEMENTED)")


class BinSelection(APIObject):
    """Selection of a time bin based on a datetime or index
    """
    # reference asset - which time bins it'll draw from (StepOutput only)
    reference_asset = StringDescr(doc="which asset to reference the time bins. For step outputs")

    datetime = DatetimeDescr(doc="datetime to use for selection")
    index = IntDescr(doc="datetime to use for selection")


class StridedBinning(APIObject):
    """Create output time bins based on a from, duration, stride, offset, and count
    """
    from_selection = TypeConstrainedDescr((BinSelection, dict), coerce=True, dict_name="from", doc="from where the bins"
                                          " being. Either an index or a datetime")
    from_end = BoolDescr(doc="use the right end of the bin if True")
    duration = RegexDescr(bin_size_re, doc="the bin size, in time units for each bin")
    stride = RegexDescr(bin_size_re, doc="the stride (step forward), in time units between each bin")
    count = IntDescr(doc="how many bins")
    offset = RegexDescr(bin_size_re, doc="the offset from the first date to start the bins")

    def __init__(self,
                 from_selection=BinSelection(),
                 from_end=False,
                 duration=None,
                 stride=None,
                 count=None,
                 offset=None):

        self.from_selection = from_selection
        self.from_end = from_end
        self.duration = duration
        self.stride = stride
        if offset is None:
            offset = stride
        self.offset = offset
        self.count = count


class RangeSelection(APIObject):
    """Selection of bins between a start and an end
    """
    from_index = IntDescr(dict_name="from", doc="starting point of bin selection in a range")
    to_index = IntDescr(dict_name="to", doc="ending point of bin selection in a range")

    def __init__(self, from_index=None, to_index=None):
        self.from_index = from_index
        self.to_index = to_index


class NearestSelection(APIObject):
    """Selection of the nearest bin to a specified before/after point
    """
    before = DatetimeDescr(doc="select the nearest bin BEFORE this value")
    after = DatetimeDescr(doc="select the nearest bin AFTER this value")


class ReduceMethod(APIObject):
    """Reduce along time bin dimension into a single bin
    """
    op = StringDescr(one_of=['min', 'max', 'mean', 'sum', 'first', 'last'], doc="reduction operation on time bins")


class TimeBinSelection(APIObject):
    """A description of which time bins to select from the input
    """
    # Only one of the following can be set
    all = BoolDescr(doc="select all time bins from input")
    index = IntDescr(doc="the index of the time bin to select")
    since = TypeConstrainedDescr((BinSelection, dict), coerce=True, doc="select all bins since this selection")
    until = TypeConstrainedDescr((BinSelection, dict), coerce=True, doc="select all bins before this selection")
    range = TypeConstrainedDescr((RangeSelection, dict), coerce=True, doc="selection all bins in a range")
    nearest = TypeConstrainedDescr((NearestSelection, dict), coerce=True, doc="select the nearest time bin")

    # Reduce along time dimension with this operation
    reduce = TypeConstrainedDescr((ReduceMethod, dict), coerce=True, doc="reduce along time dimension before sending"
                                  " to model. This will send a single time bin (NOT IMPLEMENTED)")


class OutputBand(APIObject):
    """An output bin, either a name or STAC eo band
    """
    band_name = StringDescr(doc="the name of the bin")
    eo_band = DictDescr(doc="an eo:band object of information about this band")


class OutputTimeBins(APIObject):
    """How to define what the output time bins are for a step output
    """
    nontemporal = BoolDescr(doc="nontemporal; there will only be one single bin created")
    user = TypeConstrainedDescr((User, dict), coerce=True, doc="user defined bin edges")
    strided = TypeConstrainedDescr((StridedBinning, dict), coerce=True, doc="build bins by defining a from, duration,"
                                   " stride, offset, and count")


class StepInput(APIObject):
    """An input for a processing step
    """
    asset_name = StringDescr(doc="name of the asset to use as input")
    spatial_chunk_shape = TupleDescr(doc="the shape of each chunk of input for this step in row/column space")
    type = RegexDescr(r"((?:tensor)|(?:features)|(?:records))", doc="the type of input")
    overlap = IntDescr(doc="number of pixels of overlap to apply when tiling the inputs")
    bands = ListDescr(item_type=(int, float), coerce_items=True, doc="band index/ID of the bands to select from input")
    time_bin_selection = TypeConstrainedDescr((TimeBinSelection, dict), coerce=True, doc="which time bins should be"
                                              " selected from the input")


class StepOutput(APIObject):
    """An output for a processing step
    """
    asset_name = StringDescr(doc="name of an asset this step emits")
    type = RegexDescr(r"((?:tensor)|(?:features)|(?:records))", doc="the type of output")
    chunk_shape = TupleDescr(
        doc="the shape of the output from this asset from the container. Even if the container performs a reduction, "
            "please specify the full dimensions in the order (time, band/feature, rows, columns). (1, 1, 1, 1) for "
            " scaler output",
        min_len=4,
        max_len=4)
    pixel_dtype = DTypeDescr(doc="the dtype of this ouptut asset")
    fill_value = TypeConstrainedDescr((int, float, str, complex), doc="the fill value for this output asset")
    trim = IntDescr(doc="the number of border pixels to remove from output of the model. This typically"
                        " should match the overlap in the step input, but for cases like models that upsample"
                        " (e.g. superresolution), this should trim off a different value.")
    output_time_bins = TypeConstrainedDescr((OutputTimeBins, dict), coerce=True, doc="how to generate output time bins")
    output_bands = ListDescr(item_type=(OutputBand, dict), coerce_items=True, doc="band names or STAC eo:band objects")


class Step(APIObject):
    """A step in a Tesseract Job

    NotImplemented

    """
    name = StringDescr(doc="the name of this step")
    type = StringDescr(doc="the type of this step (model, rechunk)")
    inputs = ListDescr(item_type=(StepInput, dict), doc="a list of inputs for this step")
    outputs = ListDescr(item_type=(StepOutput, dict), doc="a list of outputs for this step")
    container = TypeConstrainedDescr((Container, dict))
    gpu = BoolDescr(doc="make the step run on a machine with GPU resources", default=False)
    workers = IntDescr(doc="number of workers to run for this step")


class Bucket(APIObject):
    url = StringDescr(doc="a storage URL, (e.g. s3://bucket/prefix or gs://bucket/prefix). If this is specified,"
                      " you do not need to specify prefix, platform, bucket, region, account or domain")
    prefix = StringDescr(doc="all output will be written to this prefix")
    platform = StringDescr(doc="the platform for this bucket (aws, gcp, azure)")
    bucket = StringDescr(doc="name of the bucket or container")
    region = StringDescr(doc="storage region (AWS)")
    credentials = StringDescr(doc="credentials to access this bucket")
    account = StringDescr(doc="the azure storage account name (e.g. storageaccount)")
    domain = StringDescr(doc="the azure storage domain (e.g. us.core.windows.net)")
    requester_pays = BoolDescr(doc="requester pays to access bucket", default=False)


class GlobalProperties(APIObject):
    """GlobalProperties that will be applied to all assets if they have empty values

    Only contains a subset of the parameters for an asset.

    Args:
        **spec(dict): A dictionary that can be used to initialize the object. Optional.
    """

    shape = TupleDescr(doc="the shape of the output for this asset (rows, columns)", min_len=2, max_len=2)
    pixel_size = TupleDescr(doc="the size of each pixel in the output SRS (x, y)", min_len=2, max_len=2)
    pixel_dtype = DTypeDescr(doc="output pixel dtype")
    chip_size = IntDescr(doc="size of the chips to break work into (default=512, max=2000)")
    project = ProjectDescr(doc="the project the source dataset belongs to. You must have read access to this project")
    output_no_data = ListDescr(
        item_type=(int, float, complex),
        doc="set the value to be ignored and treated as nodata in the output")
    compression = RegexDescr(regex=r'((?:zlib)|(?:blosc)|(?:none))', doc="the compression algorithm for output data")
    datetime = DatetimeIntervalDescr(doc="the datetime interval to be used to query for matching data")
    temporal_binning = TypeConstrainedDescr((TemporalBinning, dict), doc="the temporal binning strategy")

    def __init__(self, **spec):

        self._compression = None
        self._project = None
        self._datetime = None
        self._output_no_data = None
        self._temporal_binning = None

        for k, v in spec.items():
            setattr(self, k, v)


resample_options = [
    'nearest',
    'bilinear',
    'cubic',
    'cubicspline',
    'lanczos',
    'average',
    'mode',
    'max',
    'min',
    'median',
    'q1',
    'q3',
    'sum',
    'NEAREST',
    'BILINEAR',
    'CUBIC',
    'CUBICSPLINE',
    'LANCZOS',
    'AVERAGE',
    'MODE',
    'MAX',
    'MIN',
    'MEDIAN',
    'Q1',
    'Q3',
    'SUM'
]


class FeatureAggregation(APIObject):
    """FeatureAggregation specifies how features should be handled while rasterizing
    """
    value = TypeConstrainedDescr((str, float, int, complex))
    aggregation_rules = ListDescr(item_type=str)
    groups = ListDescr(item_type=dict)


class AssetSpec(APIObject):
    """AssetSpec is a class to represent the requested output assets in a tesseract job.

    Args:
        **spec(dict): A dictionary that can be used to initialize the object. Optional.

    """
    name = StringDescr(doc="name of this asset")
    dataset = DatasetDescr(doc="the dataset to derive this asset from")
    assets = ListDescr(item_type=str, doc="the assets within the dataset to use. "
                                          "Each will be separate band(s)/feature(s)")
    asset_band_counts = ListDescr(item_type=(int,), doc="list of band counts for each asset. If empty, Tesseract will"
                                                        " infer from the dataset spec or assume it's 1 and return"
                                                        " a warning")
    resample = StringDescr(
        one_of=resample_options,
        doc=f"resampling method to use, one of {', '.join(resample_options)}")
    project = ProjectDescr(doc="the project the source dataset belongs to. You must have read access to this project")
    shape = TupleDescr(doc="the shape of the output for this asset (rows, columns)", min_len=2, max_len=2)
    pixel_size = TupleDescr(doc="the size of each pixel in the output SRS (x, y)", min_len=2, max_len=2)
    pixel_dtype = DTypeDescr(doc="output pixel dtype")
    chip_size = IntDescr(doc="size of the chips to break work into (default=512, max=2000)")
    compression = StringDescr(one_of=['zlib', 'blosc', 'none'], doc="the compression algorithm for output data")
    input_no_data = ListDescr(
        item_type=(int, float, complex, str),
        doc="set the value to be ignored and treated as nodata in the input")
    output_no_data = ListDescr(
        item_type=(int, float, complex, str),
        doc="set the value to be ignored and treated as nodata in the output")
    ids = ListDescr(item_type=(int, str), doc="list of item IDs to be used to query from the specified dataset")
    datetime = DatetimeIntervalDescr(doc="the datetime interval to be used to query for matching data")
    query = DictDescr(doc="a dictionary formatted like"
                          "https://github.com/radiantearth/stac-api-spec/"
                          "blob/master/item-search/README.md#query-extension"
                          "to be used to filter input data")
    filter = DictDescr(doc="a dictionary representing a JSON CQL2 filter as defined by the OGC spec: "
                           "https://github.com/opengeospatial/ogcapi-features/tree/master/cql2")
    feature_aggregation = TypeConstrainedDescr(
        (FeatureAggregation, dict), doc="how features should be aggregated into a resulting raster see REST API docs"
                                        " for further info: https://docs.seerai.space/tesseract/v1/index.html")
    stac_items = ListDescr(item_type=(dict, Feature, Item), doc="a list of Tesseract features/items to use in lieu"
                                                                " of a query", dict_name='items')
    as_feature = BoolDescr(doc="treat items as features (e.g. for Rasterize) instead of STAC items (usually Warp)")
    fill_value = NumberDescr(doc="anywhere there is no calculated data, will be replaced with this")
    temporal_binning = TypeConstrainedDescr((TemporalBinning, dict), doc="the temporal binning strategy")
    hooks = ListDescr(item_type=(Webhook, dict), doc="webhooks to be called when asset is completed")

    def __init__(self, **spec):
        # Set defaults
        self.resample = 'nearest'
        self.fill_value = 0
        self.pixel_dtype = np.float32
        self.compression = 'blosc'
        self.project = 'global'

        for k, v in spec.items():
            if k == 'items':
                k = 'stac_items'
            setattr(self, k, v)


class AssetSpecListDescr(BaseDescr):
    """a list of validated AssetSpecs

    AssetSpecListDescr is a list of AssetSpec items, this sets/returns a list no matter what,
    it doesn't raise an attribute error.

    __get__ returns the list, creating it on the base object if necessary
    __set__ sets the list after validating that it is a list
    """

    def _get(self, obj: object, objtype=None) -> list:
        # Try to get the private attribute by name (e.g. '_assets')
        assets = getattr(obj, self.private_name, None)
        if assets is not None:
            # Return it if it exists
            return assets

        try:
            assets = self._get_object(obj)

            isAssetSpec = True
            for asset in assets:
                if not isinstance(asset, AssetSpec):
                    isAssetSpec = False
                    break
            if not isAssetSpec:
                self._set(obj, assets)
                return self._get(obj)

        except KeyError:
            assets = []
            self._set_object(obj, assets)
        setattr(obj, self.private_name, assets)
        return assets

    def _set(self, obj: object, value: object) -> None:
        assets = [
            AssetSpec(**asset) for asset in value
        ]
        setattr(obj, self.private_name, assets)
        self._set_object(obj, assets)

    def _validate(self, obj: object, value: object) -> None:
        if not isinstance(value, (list, tuple)):
            raise ValueError(f"'{self.public_name}' must be a tuple or list")
        if len(value) > 0:
            for asset in value:
                if not isinstance(asset, (dict, AssetSpec)):
                    raise ValueError(f"each value must be a dict/AssetSpec, not '{type(asset)}'")


class Warning(APIObject):
    title = StringDescr(doc="short description of the warning")
    detail = StringDescr(doc="detailed description of the warning")
    severity = StringDescr(doc="severity of the warning", default='LOW')

    def warn(self):
        warnings.warn(f"{self.title} (severity={self.severity}): {self.detail}")


class JobResponse(APIObject):
    job_id = StringDescr(doc="id of the submitted Tesseract Job")
    dataset = TypeConstrainedDescr((Dataset, dict), doc="the generated dataset from this job", coerce=True)
    item = TypeConstrainedDescr((Item, Feature, dict), doc="STAC Item for this job's output", coerce=True)
    n_quarks = IntDescr(doc="nubmer of quarks produced")
    n_steps = IntDescr(doc="nubmer of steps in this job")
    n_edges = IntDescr(doc="number of edges in the graph")
    avg_quark_size_bytes = FloatDescr(doc="average size of a quark, in bytes")
    warnings = ListDescr(item_type=(Warning, dict),
                         doc="any warnings returned while planning the job", coerce_items=True)

    def warn(self):
        """Shows all warnings that came from this job
        """
        for warning in self.warnings:
            warning.warn()
