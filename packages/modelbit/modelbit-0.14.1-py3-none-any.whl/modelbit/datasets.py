from typing import Union, Any, List, cast, Dict
import pandas, io, pickle
from urllib.parse import quote_plus
from .utils import sizeOfFmt, timeago, timestamp, inDeployment
from .helpers import DatasetDesc, getJsonOrPrintError, isAuthenticated, getCurrentBranch
from .secure_storage import getS3DatasetCsvBytes, getS3DatasetPklBytes, getSecureDataGzip, getSecureDataZstd
from .ux import TableHeader, UserImage, renderTemplate


class TimedDatasetCache:

  def __init__(self, expireSeconds: int):
    self.expireSeconds = expireSeconds
    self.initTime = timestamp()
    self.cache: Dict[str, pandas.DataFrame] = {}

  def _maybeResetCache(self):
    if self.initTime + (self.expireSeconds * 1000) < timestamp():
      self.cache = {}
      self.initTime = timestamp()

  def set(self, key: str, val: pandas.DataFrame):
    self._maybeResetCache()
    self.cache[key] = val

  def get(self, key: str):
    self._maybeResetCache()
    return self.cache.get(key, None)


_datasetCache = TimedDatasetCache(5 * 60)


class DatasetList:

  def __init__(self):
    self._datasets: List[DatasetDesc] = []
    self._iter_current = -1
    resp = getJsonOrPrintError("jupyter/v1/datasets/list")
    if resp and resp.datasets:
      self._datasets = resp.datasets

  def _repr_html_(self):
    if not isAuthenticated():
      return ""
    return self._makeDatasetsHtmlTable()

  def __iter__(self):
    return self

  def __next__(self) -> str:
    self._iter_current += 1
    if self._iter_current < len(self._datasets):
      return self._datasets[self._iter_current].name
    raise StopIteration

  def _makeDatasetsHtmlTable(self):
    if len(self._datasets) == 0:
      return "There are no datasets to show."
    headers = [
        TableHeader("Name", TableHeader.LEFT, isCode=True),
        TableHeader("Owner", TableHeader.CENTER),
        TableHeader("Data Refreshed", TableHeader.RIGHT),
        TableHeader("SQL Updated", TableHeader.RIGHT),
        TableHeader("Rows", TableHeader.RIGHT),
        TableHeader("Bytes", TableHeader.RIGHT),
    ]
    rows: List[List[Union[str, UserImage]]] = []
    for d in self._datasets:
      rows.append([
          d.name,
          UserImage(d.ownerInfo.imageUrl, d.ownerInfo.name),
          timeago(d.recentResultMs) if d.recentResultMs != None else '',
          timeago(d.sqlModifiedAtMs) if d.sqlModifiedAtMs != None else '',
          _fmt_num(d.numRows),
          sizeOfFmt(d.numBytes)
      ])
    return renderTemplate("table", headers=headers, rows=rows)


def list():
  return DatasetList()


def _cacheKey(dsName: str):
  return f"{getCurrentBranch()}/{dsName}"


def get(dsName: str,
        filters: Union[Dict[str, List[Any]], None] = None,
        filter_column: Union[str, None] = None,
        filter_values: Union[List[Any], None] = None,
        optimize: bool = False):
  cacheKey = _cacheKey(dsName)
  df = _datasetCache.get(cacheKey)
  if df is None or not inDeployment():
    if inDeployment():
      df = _getFromS3(dsName, optimize)
    else:
      df = _getFromWeb(dsName, optimize)
    if df is not None:
      _datasetCache.set(cacheKey, df)
  if df is None:
    raise Exception(f"Unable to fetch dataset '{dsName}'")
  if filters is not None:
    return _filterDataset(df, filters)
  elif filter_column is not None and filter_values is not None:  # Back-compat
    return _filterDataset(df, {filter_column: filter_values})
  return _uncategorizeDf(df)


# returns copied df. Categories are used for compression and need to be removed before sending to customer
# code because some libs cannot handle category-types (e.g. btyd)
def _uncategorizeDf(df: pandas.DataFrame):
  df = df.copy()
  for col in df.columns:  # type: ignore
    if df[col].dtype == "category":  # type: ignore
      df[col] = df[col].astype(str)  # type: ignore
  return df


def _dfFromCsvStream(stream: Union[bytes, None]):
  if stream is None:
    return None
  return cast(
      pandas.DataFrame,
      pandas.read_csv(  # type: ignore
          io.BytesIO(stream), sep='|', low_memory=False, na_values=['\\N', '\\\\N']))


def _dfFromPkl(stream: Union[bytes, None]):
  if stream is None:
    return None
  return cast(pandas.DataFrame, pickle.loads(stream))


def _filterDataset(df: pandas.DataFrame, filters: Dict[str, List[Any]]):
  for filterCol, filterValues in filters.items():
    df = df[df[filterCol].isin(filterValues)]  # type: ignore
  return _uncategorizeDf(df)


def _getFromWeb(dsName: str, optimize: bool):
  data = getJsonOrPrintError(f'jupyter/v1/datasets/get?dsName={quote_plus(dsName)}')
  if not data:
    return None
  if data.dsrPklDownloadInfo and optimize:
    return _dfFromPkl(getSecureDataZstd(data.dsrPklDownloadInfo, dsName))
  if data.dsrDownloadInfo:
    return _dfFromCsvStream(getSecureDataGzip(data.dsrDownloadInfo, dsName))
  if not isAuthenticated():
    return None
  return None


def _getFromS3(dsName: str, optimize: bool):
  if optimize:
    pklBytes = getS3DatasetPklBytes(dsName)
    if pklBytes is not None:
      return _dfFromPkl(pklBytes)
  csvBytes = getS3DatasetCsvBytes(dsName)
  if csvBytes is not None:
    return _dfFromCsvStream(csvBytes)
  raise Exception('Version not found.')


def _fmt_num(num: Union[int, Any]):
  if type(num) != int:
    return ""
  return format(num, ",")
