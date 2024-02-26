#!/usr/bin/env python3
import asyncio
import io
import re
import zipfile

import aiohttp
from bs4 import BeautifulSoup

from notebooks.ford.vbf import get_vbf_path


class DownloadError(Exception):
  pass


class TemporaryServerError(Exception):
  pass


FILE_NOT_FOUND = re.compile(r'File \((?P<filename>.*)\) Not Found')


async def _download(filename: str, session: aiohttp.ClientSession) -> bytes:
  async with session.post(
    url='https://www.fordtechservice.dealerconnection.com/vdirs/wds/PCMReprogram/DSFM_DownloadFile.asp',
    headers={'content-type': 'application/x-www-form-urlencoded'},
    data=f'filename={filename}',
  ) as response:
    response.raise_for_status()

    if response.content_length == 1172:
      raise TemporaryServerError()

    content_disposition = response.headers.get('Content-Disposition')
    if isinstance(content_disposition, str):
      response_filename = content_disposition.split('=')[1]
      if response_filename.startswith(filename):
        # there is some junk HTML at the end
        data = await response.read()
        split_data = data.split(b'<html>', 1)
        return split_data[0]

    page = await response.text()
    soup = BeautifulSoup(page, 'lxml')
    field_label = soup.find('td', {'class': 'FieldLabel'})
    if not field_label:
      print(page)
      raise DownloadError('Unable to parse response')

    error_msg = field_label.text.strip()

    not_found = FILE_NOT_FOUND.search(error_msg)
    if not_found:
      filename = not_found.group('filename')
      raise FileNotFoundError(f'File {filename} not found')

    # TODO: handle other error messages
    raise DownloadError(error_msg)


async def _safe_download(filename: str, session: aiohttp.ClientSession, retries: int) -> bytes:
  attempts = 0
  while True:
    try:
      return await _download(filename, session)
    except TemporaryServerError:
      attempts += 1
      if attempts == retries:
        raise
      print(f'Retrying download ({attempts}/{retries})')
      await asyncio.sleep(0.2)


async def download_vbf(filename: str, retries: int = 10) -> bool:
  vbf_path = get_vbf_path(filename)
  if vbf_path.is_file() and vbf_path.stat().st_size > 0:
    return False

  async with aiohttp.ClientSession(cookie_jar=aiohttp.DummyCookieJar()) as session:
    vbf_zip = await _safe_download(filename, session, retries=retries)

  with open(vbf_path, 'wb') as f, zipfile.ZipFile(io.BytesIO(vbf_zip)) as zf:
    names = zf.namelist()
    assert len(names) == 1, f'Expected 1 file in ZIP, got {len(names)}: {names}'

    for name in names:
      if name.lower().startswith(filename.lower()) or name.lower().endswith('.vbf'):
        f.write(zf.read(name))
        return True
    raise FileNotFoundError(f'VBF file {filename} not found in ZIP: {names}')


if __name__ == '__main__':
  import argparse
  import asyncio

  parser = argparse.ArgumentParser()
  parser.add_argument('filename', type=str, help='Filename to download')
  parser.add_argument('--retries', type=int, default=10, help='Number of retries')
  args = parser.parse_args()

  asyncio.run(download_vbf(args.filename, args.retries))
