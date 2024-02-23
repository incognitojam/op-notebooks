#!/usr/bin/env python3
import asyncio
import json
import xml.etree.ElementTree as ET

import aiohttp
from bs4 import BeautifulSoup


semaphore = asyncio.Semaphore(16)


def json_to_xml(json_obj, parent):
  if isinstance(json_obj, dict):
    for key in json_obj:
      sub_obj = json_obj[key]
      if key.startswith('@'):
        parent.set(key[1:], sub_obj)
      elif key == '#text':
        parent.text = sub_obj
      elif isinstance(sub_obj, list):
        for elem in sub_obj:
          child = ET.SubElement(parent, key)
          json_to_xml(elem, child)
      else:
        child = ET.SubElement(parent, key)
        json_to_xml(sub_obj, child)
  elif isinstance(json_obj, list):
    for sub_obj in json_obj:
      child = ET.SubElement(parent, parent.tag)
      json_to_xml(sub_obj, child)
  else:
    parent.text = json_obj


async def download(vin: str, session: aiohttp.ClientSession) -> str:
  async with semaphore:
    async with session.post(
      url='https://www.motorcraftservice.com/AsBuilt/Details',
      headers={
        'accept': 'text/html,application/xhtml+xml',
        'accept-encoding': 'gzip, deflate, br',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'UserCountry=marketID=152&language=EN-US&country=GBR&ParentCode=EU &IsSelected=YES; __RequestVerificationToken=G4Qq1c8wteFy3vmfacTj4xhu3i1RGDBxEXxL0Jnj6dnyFQz1VmC0E5_XVeu8q2CkykBYybDcmGygktBsix0fmylQqWc1; wrawrsatrsrweasrdxsf=96c9ca9ee35948c4957bdfd6301d6da9=WUBEw87awMZXw8L2Ini3Jp4SdZu4Uhl20IeeEgfBvyohT68FYykqQMf0cVQbUBDgsVLOvGLwwm6QrUncrWMTmF1djdNaFHaW+Srf37bESTfneoBcaEHiJslEdgOksUjWtD0Zij8sM/iCRkh9IJsojREzlBo2DcawUS0jn3kkFZ3z5g5BOtF3CAIOc1FbT7KHlzLXh280npQsGCaQA43TaA==;',
      },
      data={
        '__RequestVerificationToken': 'emYDuwE0L1ImTV6beppJBZpxeeo9o0bR6Kr61Aq3-nnRn6UyactyAnfO_7NV1FfEKebt5B8wE7F0TbMXslDAfZZIUr41',
        'VIN': vin,
        'CaptchaDeText': '96c9ca9ee35948c4957bdfd6301d6da9',
        'CaptchaInputText': 'QTD',
      },
      timeout=14,
    ) as response:
      response.raise_for_status()
      text = await response.text()

  # get input[name="asbuiltJson"] attribute value
  soup = BeautifulSoup(text, 'lxml')

  try:
    json_container = soup.find('input', {'name': 'asbuiltJson'})
    if json_container is None:
      print(text)
      raise ValueError('No asbuiltJson found')
    asbuilt_json = json_container.attrs['value']
    data = json.loads(asbuilt_json)

    # generate XML from JSON
    root = ET.Element('AS_BUILT_DATA')
    json_to_xml(data['AS_BUILT_DATA'], root)
    asbuilt_xml = ET.tostring(root, encoding='unicode', method='xml')
  except Exception as e:
    print(f'{vin=}')
    raise e

  return asbuilt_xml


async def main(vin: str):
  async with aiohttp.ClientSession(cookie_jar=aiohttp.DummyCookieJar()) as session:
    asbuilt_xml = await download(vin, session)
  print(asbuilt_xml)


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('vin', help='VIN')
  args = parser.parse_args()

  asyncio.run(main(args.vin))
