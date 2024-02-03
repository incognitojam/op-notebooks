#!/usr/bin/env python3
import json
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup


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


def download(vin: str) -> str:
  url = 'https://www.motorcraftservice.com/AsBuilt/Details'
  headers = {
    'Host': 'www.motorcraftservice.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '209',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Origin': 'https://www.motorcraftservice.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.motorcraftservice.com/AsBuilt',
    'Cookie': 'UserCountry=marketID=105&language=EN-US&country=NLD&ParentCode=EU &IsSelected=YES; RT="z=1&dm=www.motorcraftservice.com&si=c7bd2411-0aaf-4fc9-8b4d-c0b830993637&ss=ls66quid&sl=0&tt=0"; __RequestVerificationToken=IJ3LNyeQ9Tm2lqr7ieBf_qJOnyLxKBC0Od1O6GZ9zuVm2SPCXG-eGswKOOCYYd1hz8jRBVzUYyZC8uVbOX4mBtMZiz01; wrawrsatrsrweasrdxsf=d07deda9a7264aea9a03a7744e95152e=WUBEw87awMZXw8L2Ini3Jp4SdZu4Uhl20IeeEgfBvyohT68FYykqQMf0cVQbUBDgsVLOvGLwwm6QrUncrWMTmF1djdNaFHaW+Srf37bESTfwDwOxOHZIdR2TlueUWIGKSPV/L3wtwQnzRL9DnfjIT/umDx2s4r9O6orm5243MuFMBlwHjm5nIWwCVSxF1RaeOfhzi0Tc0FcL0B/cYYBabA==; wrawrsatrsrweasrdxsfw2ewasjret=; dtCookie=v_4_srv_31_sn_07A8968CB6F2F772151BFA5340A554C4_perc_100000_ol_0_mul_1_app-3A80b5fb30b8203a4c_1_rcs-3Acss_0; ak_bmsc=E738915FABE185E57861EC68F435C7AE~000000000000000000000000000000~YAAQje1lXwoxG2GNAQAANQNubxb7C2jy/cZR6kJBNkqZlACRJXp399XHXUWlJl5Cduc5pjZudelZCPqrE9u28qGupKbFgT6Q2ne5uYcLZvvbkwV2HGAMACgyKE2KT97HzjbdsbW2aFd3Wqew6gdmYcus55THTUKunqDqF5Cuf76lSu7igw9btaHZUV1oduOin5bBj3Cr6pT5ETVpWoLUn5DOJXswZh2uupWfA8gBmmsGLPo4bLzmJLh86sn7QzG2WlducHuc0L834swMVifZ2btQLy15AYIGZtQL93Y9OJYBroHbDAz4WNpLnkhJaQA4TSURH9i9Q4ntw9ohcBd0E32oRju51XLPur1mEt0jO8/yVfZNmx/TQv00DMO6lhOkuEKV6P/dvR2JnL4bnJWwooSH+hKhgKGmN3nhg6OEukRRT52rEOSEhyIwhJKIEm4kTom7sXvVvQS8H62eholWPlnTyb9lKwRYkCP88r670OBrCpeV2BEQvYfyenDdFPv1EVEe2pfROYRIMTRsMA==; rxVisitor=1706971479969CNISR5SJIR0NKK08M4R9PMORKDJN8KTN; dtPC=31$571479967_579h-vKKFDILPSKKABWKCQGRHSGFJHAPLJMDNQ-0e0; rxvt=1706973286639|1706971479970; dtSa=true%7CC%7C-1%7CSubmit%7C-%7C1706971491093%7C571479967_579%7Chttps%3A%2F%2Fwww.motorcraftservice.com%2FAsBuilt%7C%7C%7C%7C; bm_sv=E94B1B2ABEFCFEFA4DBABB8B958D612A~YAAQje1lX8w0G2GNAQAAVSdubxbuGpkiKmQvWS57rZgEygElTifvQiz99z+Losh+gfDZbmxtN9SIuqtHxyiJkIOMuceKBG7v94yNMZkyVxnTWQRPx6V4Ho8JsY9nQKwjKX5wWhdH4EuxvwjWx5/ZBPG7A8Va/vM9rNS0F3kbceeRVpzkIBnZMoYVY5KvPgbtmGhlbBk1hvJKt41CJ7JNUbGekRsBGBD1v72JAS4Tgdugne6am7CziH0H5hOGdAmLRgUddWLmZeZxNp4=~1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
  }
  data = {
    '__RequestVerificationToken': 'iJx284Zd4B5R-62D1A5BanfVCkcnK4L1VEFphASPS7oGRQlRoUk-eWwiKhT5Q-c7WsKFHzNcqcLoNrrO5DFJM9fv5Nk1',
    'VIN': vin,
    'CaptchaDeText': 'd07deda9a7264aea9a03a7744e95152e',
    'CaptchaInputText': 'PLH',
  }
  response = requests.post(url, headers=headers, data=data, timeout=12)
  if response.status_code != 200:
    raise ValueError(f'Invalid response: {response.status_code}')

  # get input[name="asbuiltJson"] attribute value
  soup = BeautifulSoup(response.text, 'lxml')

  asbuilt_json = soup.find('input', {'name': 'asbuiltJson'}).attrs['value']
  data = json.loads(asbuilt_json)

  # generate XML from JSON
  root = ET.Element('AS_BUILT_DATA')
  json_to_xml(data['AS_BUILT_DATA'], root)
  asbuilt_xml = ET.tostring(root, encoding='unicode', method='xml')

  return asbuilt_xml


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('vin', help='VIN')
  args = parser.parse_args()

  asbuilt_xml = download(args.vin)
  print(asbuilt_xml)
