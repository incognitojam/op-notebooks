#!/usr/bin/env python3
import asyncio
import json
import random
import urllib.parse
from enum import StrEnum
from typing import Literal

import aiohttp
from bs4 import BeautifulSoup
from pydantic import BaseModel


class SortBy(StrEnum):
  BEST_MATCH = 'best_match_desc'
  LOWEST_PRICE = 'list_price'
  HIGHEST_PRICE = 'list_price_desc'
  LOWEST_MILEAGE = 'mileage'
  HIGHEST_MILEAGE = 'mileage_desc'
  NEAREST_LOCATION = 'distance'
  BEST_DEAL = 'best_deal'
  NEWEST_YEAR = 'year_desc'
  OLDEST_YEAR = 'year'
  NEWEST_LISTED = 'listed_at_desc'
  OLDEST_LISTED = 'listed_at'


class StockType(StrEnum):
  NEW_AND_USED = 'all'
  NEW_AND_CERTIFIED = 'new_cpo'
  NEW = 'new'
  USED = 'used'
  CERTIFIED = 'cpo'


class Make(StrEnum):
  AUDI = 'audi'
  ACURA = 'acura'
  BMW = 'bmw'
  BUICK = 'buick'
  CADILLAC = 'cadillac'
  CHEVROLET = 'chevrolet'
  CHRYSLER = 'chrysler'
  DODGE = 'dodge'
  FORD = 'ford'
  GMC = 'gmc'
  GENESIS = 'genesis'
  HONDA = 'honda'
  HYUNDAI = 'hyundai'
  INFINITI = 'infiniti'
  JEEP = 'jeep'
  KIA = 'kia'
  LEXUS = 'lexus'
  LINCOLN = 'lincoln'
  MERCEDES_BENZ = 'mercedes_benz'
  MITSUBISHI = 'mitsubishi'
  NISSAN = 'nissan'
  POLESTAR = 'polestar'
  PORSCHE = 'porsche'
  RAM = 'ram'
  SUBARU = 'subaru'
  TOYOTA = 'toyota'
  VOLKSWAGEN = 'volkswagen'
  VOLVO = 'volvo'


class Model(StrEnum):
  FORD_BRONCO = 'ford-bronco'
  FORD_BRONCO_SPORT = 'ford-bronco_sport'
  FORD_E_TRANSIT = 'ford-e_transit'
  FORD_ECOSPORT = 'ford-ecosport'
  FORD_EDGE = 'ford-edge'
  FORD_ESCAPE = 'ford-escape'
  FORD_ESCAPE_PHEV = 'ford-escape_phev'
  FORD_EXPEDITION = 'ford-expedition'
  FORD_EXPEDITION_MAX = 'ford-expedition_max'
  FORD_EXPLORER = 'ford-explorer'
  FORD_F_150 = 'ford-f_150'
  FORD_F_150_LIGHTNING = 'ford-f_150_lightning'
  FORD_F_250 = 'ford-f_250'
  FORD_F_350 = 'ford-f_350'
  FORD_F_450 = 'ford-f_450'
  FORD_FIESTA = 'ford-fiesta'
  FORD_FLEX = 'ford-flex'
  FORD_FUSION = 'ford-fusion'
  FORD_FUSION_ENERGI = 'ford-fusion_energi'
  FORD_FUSION_HYBRID = 'ford-fusion_hybrid'
  FORD_GT = 'ford-gt'
  FORD_MAVERICK = 'ford-maverick'
  FORD_MUSTANG = 'ford-mustang'
  FORD_MUSTANG_MACH_E = 'ford-mustang_mach_e'
  FORD_RANGER = 'ford-ranger'
  FORD_SHELBY_GT350 = 'ford-shelby_gt350'
  FORD_SHELBY_GT500 = 'ford-shelby_gt500'
  FORD_TAURUS = 'ford-taurus'
  FORD_TRANSIT_CONNECT = 'ford-transit_connect'
  FORD_TRANSIT_150 = 'ford-transit_150'
  FORD_TRANSIT_250 = 'ford-transit_250'
  FORD_TRANSIT_350 = 'ford-transit_350'
  FORD_UTILITY_POLICE_INTERCEPTOR = 'ford-utility_police_interceptor'
  LINCOLN_AVIATOR = 'lincoln-aviator'
  LINCOLN_CONTINENTAL = 'lincoln-continental'
  LINCOLN_CORSAIR = 'lincoln-corsair'
  LINCOLN_MKC = 'lincoln-mkc'
  LINCOLN_MKT = 'lincoln-mkt'
  LINCOLN_MKZ = 'lincoln-mkz'
  LINCOLN_MKZ_HYBRID = 'lincoln-mkz_hybrid'
  LINCOLN_NAUTILUS = 'lincoln-nautilus'
  LINCOLN_NAVIGATOR = 'lincoln-navigator'
  LINCOLN_NAVIGATOR_L = 'lincoln-navigator_l'


class Vehicle(BaseModel):
  make: str
  model: str
  year: int
  trim: str | None
  # cat: str
  # customer_id: int
  # stock_type: Literal['New', 'Used']
  vin: str
  # seller_type: Literal['dealership']
  # certified_preowned: bool
  # listing_id: str
  # mileage: int | None
  sponsored: bool
  # nvi_program: bool
  # exterior_color: str | None
  # fuel_type: Literal['Bio Diesel', 'Diesel', 'Diesel (B20 capa', 'Diesel (B20 capable)', 'E85 Flex Fuel', 'Electric', 'Flexible Fuel', 'Gasoline', 'Hybrid', 'Other', 'Plug-In Hybrid', 'Regular Unleaded'] | None
  # msrp: str | None
  # sponsored_type: Literal['inventory_ad', 'standard']
  # price: int | None
  # bodystyle: Literal['', 'Cargo Van', 'Convertible', 'Coupe', 'Hatchback', 'Passenger Van', 'Pickup Truck', 'Sedan', 'SUV', 'Wagon']
  # cpo_indicator: bool
  # badges: list[Literal['cpo', 'fair_deal', 'good_deal', 'great_deal', 'hot_car', 'price_drop_in_cents']]
  # stock_sub: str
  # canonical_mnt: str | None = None

  def __str__(self) -> str:
    return f'Vehicle({self.model_dump()})'


semaphore = asyncio.Semaphore(8)


async def search_cars(
  keyword: str = None,
  list_price_max: int = None,
  list_price_min: int = None,
  makes: list[Make] = None,
  models: list[Model] = None,
  maximum_distance: int | Literal['all'] = 'all',
  zip: int = None,
  mileage_max: int = None,
  monthly_payment: int = None,
  sort: SortBy = SortBy.BEST_MATCH,
  stock_type: StockType = StockType.NEW_AND_USED,
  year_max: int = None,
  year_min: int = None,
  page_size: int = 20,
  page: int = None,
  session: aiohttp.ClientSession = None,
):
  params = {
    'keyword': keyword,
    'list_price_max': list_price_max,
    'list_price_min': list_price_min,
    'makes[]': set(make.value for make in makes) if makes else None,
    'models[]': set(model.value for model in models) if models else None,
    'maximum_distance': maximum_distance,
    'mileage_max': mileage_max,
    'monthly_payment': monthly_payment,
    'page': page,
    'page_size': page_size,
    'sort': sort,
    'stock_type': stock_type,
    'year_max': year_max,
    'year_min': year_min,
    'zip': zip,
  }
  query_string = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
  url = f'https://www.cars.com/shopping/results/?{query_string}'

  session = session or aiohttp.ClientSession()
  async with semaphore:
    await asyncio.sleep(random.random() * 0.5)
    async with session.get(url) as response:
      response.raise_for_status()
      text = await response.text()

  soup = BeautifulSoup(text, 'html.parser')
  element = soup.find('div', id='search-live-content')

  # TODO: validate this
  if not element:
    raise ValueError('No search results found')

  vehicles = []
  data_site_activity = json.loads(element.get('data-site-activity'))
  for data in data_site_activity['vehicleArray']:
    vehicle = Vehicle.model_validate(data)
    if vehicle.sponsored:
      continue
    vehicles.append(vehicle)

  return vehicles


def int_or_all(value: str | None) -> int | Literal['all']:
  return int(value) if value else 'all'


if __name__ == '__main__':
  import argparse

  import pandas as pd

  parser = argparse.ArgumentParser()
  parser.add_argument('--keyword', type=str, default=None)
  parser.add_argument('--list-price-max', type=int, default=None)
  parser.add_argument('--list-price-min', type=int, default=None)
  parser.add_argument('--make', type=Make, action='append', default=None)
  parser.add_argument('--model', type=Model, action='append', default=None)
  parser.add_argument('--maximum-distance', type=int_or_all, default=None)
  parser.add_argument('--zip', type=int, default=None)
  parser.add_argument('--mileage-max', type=int, default=None)
  parser.add_argument('--monthly-payment', type=int, default=None)
  parser.add_argument('--sort', type=SortBy, default=SortBy.BEST_MATCH)
  parser.add_argument('--stock-type', type=StockType, default=StockType.NEW_AND_USED)
  parser.add_argument('--year-max', type=int, default=None)
  parser.add_argument('--year-min', type=int, default=None)
  parser.add_argument('--page-size', type=int, default=20)
  parser.add_argument('--page', type=int, default=None)
  parser.add_argument('--format', choices=['dataframe', 'json', 'csv'], default='dataframe', help='output format')
  parser.add_argument('--separator', type=str, default=',', help='csv separator')
  parser.add_argument('--include', type=str, action='append', default=None, help='include columns')
  parser.add_argument('--exclude', type=str, action='append', default=None, help='exclude columns')
  args = parser.parse_args()

  if args.separator == '\\t':
    args.separator = '\t'

  if args.exclude and args.include:
    raise ValueError('Cannot specify both --exclude and --include')
  include, exclude = args.include, args.exclude
  if not include:
    exclude = (exclude or []) + ['sponsored']

  cars = asyncio.run(search_cars(
    keyword=args.keyword,
    list_price_max=args.list_price_max,
    list_price_min=args.list_price_min,
    makes=args.make,
    models=args.model,
    maximum_distance=args.maximum_distance,
    zip=args.zip,
    mileage_max=args.mileage_max,
    monthly_payment=args.monthly_payment,
    sort=args.sort,
    stock_type=args.stock_type,
    year_max=args.year_max,
    year_min=args.year_min,
    page_size=args.page_size,
    page=args.page,
  ))

  if args.format == 'json':
    print('[' + ','.join(car.model_dump_json(include=include, exclude=exclude) for car in cars) + ']')
  else:
    df = pd.DataFrame([vehicle.model_dump(include=include, exclude=exclude) for vehicle in cars])
    if args.format == 'dataframe':
      print(df.to_string(index=False))
    elif args.format == 'csv':
      print(df.to_csv(sep=args.separator, index=False))
