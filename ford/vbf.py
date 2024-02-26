import atexit
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path

from tinydb import Query, TinyDB
from tinydb.operations import delete

VBF_DIR = Path(__file__).parent / 'data' / 'vbf'
VBF_DIR.mkdir(exist_ok=True)


@dataclass
class VBF:
  filename: str
  'The name of the VBF file'

  seen: bool
  'Whether the VBF file has been seen in the wild'

  downloaded: bool
  'Whether the VBF file has been downloaded'

  def __post_init__(self):
    assert self.seen or self.downloaded, 'VBF must be seen in the wild or downloaded (to avoid making the database unnecessarily large)'


class DownloadError(StrEnum):
  UNKNOWN_ERROR = 'Unknown Error'
  FILE_NOT_FOUND = 'File Not Found'
  TEMPORARY_SERVER_ERROR = 'Temporary Server Error'


@dataclass
class Download:
  filename: str
  'The name of the VBF file'

  error: str | None
  'The error message, if any'

  timestamp: int
  'The timestamp of the download attempt'

  @property
  def success(self) -> bool:
    return self.error is None

  @staticmethod
  def now(filename: str, error: DownloadError = None) -> 'Download':
    return Download(filename=filename, error=error, timestamp=int(datetime.now().timestamp()))


def get_vbf_path(filename: str) -> Path:
  return VBF_DIR / f'{filename.upper()}.VBF'


def vbf_exists(filename: str) -> bool:
  return get_vbf_path(filename).is_file()


class VBFDatabase:
  def __init__(self):
    self.db = db = TinyDB(VBF_DIR / 'vbf.json')

    # all known VBF files (either seen in the wild or downloaded)
    self.vbfs = self.db.table('vbfs')

    # append-only record of all download attempts
    self.downloads = self.db.table('downloads')

    def cleanup():
      db.close()
    atexit.register(cleanup)

  def scan(self) -> None:
    known_vbf_filenames = [vbf.filename for vbf in self.get_vbfs()]

    vbfs_to_insert = []
    downloads_to_insert = []
    for filename in VBF_DIR.iterdir():
      if filename.name == 'vbf.json':
        continue
      if not filename.is_file():
        print(f'Skipping non-file: {filename}')
        continue
      if not filename.name.endswith('.VBF'):
        print(f'Skipping non-VBF file: {filename}')
        continue
      if filename.name in known_vbf_filenames:
        continue
      vbfs_to_insert.append(VBF(filename=filename.name, seen=False, downloaded=True))
      downloads_to_insert.append(Download.now(filename.name))

    self.insert_vbfs(vbfs_to_insert)
    self.insert_downloads(downloads_to_insert)
    print(f'Found {len(vbfs_to_insert)} new VBF files')

  def get_vbf(self, filename: str) -> VBF | None:
    Q = Query()
    vbf = self.vbfs.get(Q.filename == filename)
    if vbf is None:
      return None
    return VBF(**vbf)

  def get_vbfs(self) -> list[VBF]:
    return [VBF(**vbf) for vbf in self.vbfs.all()]

  def insert_vbf(self, vbf: VBF) -> None:
    self.vbfs.insert(asdict(vbf))

  def insert_vbfs(self, vbfs: list[VBF]) -> None:
    self.vbfs.insert_multiple(asdict(v) for v in vbfs)

  def update_vbf(self, vbf: VBF) -> None:
    self.vbfs.update(asdict(vbf), Query().filename == vbf.filename)

  def get_downloads(self, filename: str, min_timestamp: int = 0) -> list[Download]:
    Q = Query()
    downloads = self.downloads.search(Q.filename == filename and Q.timestamp >= min_timestamp)
    return [Download(**d) for d in downloads]

  def get_all_downloads(self) -> list[Download]:
    return [Download(**d) for d in self.downloads.all()]

  def insert_download(self, download: Download) -> None:
    self.downloads.insert(asdict(download))

  def insert_downloads(self, downloads: list[Download]) -> None:
    self.downloads.insert_multiple(asdict(v) for v in downloads)


DB = VBFDatabase()
DB.scan()
