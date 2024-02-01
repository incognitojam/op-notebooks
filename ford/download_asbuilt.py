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
    'Cookie': 'UserCountry=marketID=105&language=EN-US&country=NLD&ParentCode=EU &IsSelected=YES; RT="z=1&dm=www.motorcraftservice.com&si=c7bd2411-0aaf-4fc9-8b4d-c0b830993637&ss=ls3gqg7a&sl=0&tt=0"; __RequestVerificationToken=bCHzIFsRgCrFCVCgG9er03rtTmhmYGjAj_XEeHaIY-oVk9gGFo2PtkoMK2fOpbIbkxQtvckPPyz2NQOHlzyIZkOjJ-Y1; wrawrsatrsrweasrdxsf=06468a1510ed4bf1a11dc058c4c53a72=WUBEw87awMZXw8L2Ini3Jp4SdZu4Uhl20IeeEgfBvyohT68FYykqQMf0cVQbUBDgsVLOvGLwwm6QrUncrWMTmF1djdNaFHaW+Srf37bESTf7TLeHEljJ5aUkaVPFekYK9WeoJaPRnU96ftw0ettsYrZGry1JxhS1YFZm+LYAVet/eR6zmcxAX39zuRG4hgf382Io7kvENAOOgnFhfq0mcg==; wrawrsatrsrweasrdxsfw2ewasjret=; dtCookie=v_4_srv_27_sn_0152DB0F5AC35D5E937DBCFF36811CDB_perc_100000_ol_0_mul_1_app-3A80b5fb30b8203a4c_1_rcs-3Acss_0; ak_bmsc=0D183638ECFDCABCE0CA556B21D05FC0~000000000000000000000000000000~YAAQje1lX/zEuWCNAQAAJRCeZRZbAnBMBRn7ObiQi071SyYlr+fQzWJrFuJG1+7RpiH26i8lpF+WocTYXPcmRWcjdaHizZMmE3ocdT8efpFWKZfkyeDDAsrUK6EyTo9Rx4FWEhQzIzgcJw5NhBsCjBn94fwGqE7Q0ifQ5zFrHrEhvbqqX6j0RsbsWga54P9Aac32wKMaoeuwhQ2Lmc8+UmPBn0Qr2h5f0lpre5SdoWnWT3AGUvH5QdxM02/EXonGZNzkJIW9tuRgLQKiH5k5ydABGF65Vj8Ul6Yweff0EJkQX6qQKaER/ncTGCMIGDqvh4pkfKA7YLm7UWlvRh83tBhg3IEcMVXF9KDpEI0+9JOoVqEvMxZuVEuFtdKi1N5MoqqcgnXRn5FogO8HQ5o3/u/V8y54hrlHjJEjKrgaen+aPP/mkOCmQu32xAH7QfndjH35RLp38w0zAJIGQWG71rRdMdl1pyLzWq4shGUm/l2/mFN//iYdrFvwl3fJAtieAxDJFe0lC6zM+9s=; rxVisitor=1706806858273DTNP3A3CS9E9DKMG9RID1POOSE318AI4; dtPC=27$406877680_310h-vMCRPQPMWODURFPONTCMTHDJGMGJEIPOV-0e0; rxvt=1706808678959|1706806858274; dtSa=true%7CC%7C-1%7CSubmit%7C-%7C1706806882482%7C406877680_310%7Chttps%3A%2F%2Fwww.motorcraftservice.com%2FAsBuilt%2FDetails%7C%7C%7C%7C; bm_sv=CE7099B476D6565FCFA51A5C4EADCA9D~YAAQje1lXwXMuWCNAQAADWueZRbM7NrqA37QJFRg5eRxL2rBL39uqlrQftQ+cNU8RQIV9Jx3YLqyJnHNX2ddEGH6Y5zKbuLqyG168770V3pn5N9LKjw1zr33ZmYO60sbHuNFcDmnyKzbJBNRCyPk7xWfqgOAnMLU386eJ0KwIAAk4tRF3ALSBFDWE1YJXKzkWut6MEVp07khbxv5ee9UOFhHeN9ENBIdDRfldQ8W7VCxwlzsbhAbtGikXeyrzgTMVGFjHoFjrheBN/Z8~1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
  }
  data = {
    '__RequestVerificationToken': 'ffaCs0jGPKTeEIgATxforhsaKO5OwYOLgGi5rPH52Y3nJIDGopV79x6hf3MyDbf3lybXSpISnbxKOqjKu4-SnZ_he8k1',
    'VIN': vin,
    'CaptchaDeText': '06468a1510ed4bf1a11dc058c4c53a72',
    'CaptchaInputText': 'PNH',
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
