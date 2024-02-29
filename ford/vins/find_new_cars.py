#!/usr/bin/env python3
import asyncio

import aiohttp
from tqdm.asyncio import tqdm

from notebooks.ford.vins import check_vin, load_csv
from notebooks.ford.vins.cars_com import Make, Model, SortBy, StockType, search_cars


async def find_new_cars():
  df_existing_vins = load_csv()
  existing_vins = set(df_existing_vins['vin'])

  session = aiohttp.ClientSession()
  extra_args = dict(
    stock_type=StockType.USED,
    sort=SortBy.NEWEST_LISTED,
    session=session,
  )
  page_args = [
    dict(page_size=100, page=page) for page in range(1, 101)
  ]

  # queries = [
  #   dict(makes=[Make.FORD], year_min=2019, page_size=50, page=page) for page in range(1, 2001)
  # ]

  queries = [
    dict(models=[Model.FORD_BRONCO_SPORT]),
    dict(models=[Model.FORD_EDGE], year_min=2019),
    dict(models=[Model.FORD_ESCAPE, Model.FORD_ESCAPE_PHEV], year_min=2020),
    dict(models=[Model.FORD_E_TRANSIT]),
    dict(models=[Model.FORD_EXPLORER], year_min=2020),
    dict(models=[Model.FORD_F_150], year_min=2021),
    dict(models=[Model.FORD_F_150_LIGHTNING]),
    dict(models=[Model.FORD_MAVERICK]),
    dict(models=[Model.FORD_MUSTANG], year_min=2024),
    dict(models=[Model.FORD_MUSTANG_MACH_E]),
    dict(models=[Model.LINCOLN_AVIATOR], year_min=2020),
    dict(models=[Model.LINCOLN_CORSAIR], year_min=2020),
    dict(models=[Model.LINCOLN_NAUTILUS], year_min=2019),
    dict(models=[Model.LINCOLN_NAVIGATOR, Model.LINCOLN_NAVIGATOR_L], year_min=2022),
  ]

  cars = []
  async with session:
    pages = await tqdm.gather(*[search_cars(**dict(extra_args, **query, **page)) for query in queries for page in page_args], desc='Searching for cars', unit='page')
    for page in pages:
      for car in page:
        try:
          check_vin(car.vin)
        except Exception:
          continue
        if car.vin in existing_vins:
          continue
        if car.make not in ('Ford', 'Lincoln'):
          continue
        cars.append(car)
  return cars


if __name__ == '__main__':
  import pandas as pd

  include=['make', 'model', 'year', 'trim', 'vin']

  cars = asyncio.run(find_new_cars())

  if len(cars) == 0:
    print('No new cars found')
    exit(0)

  df = pd.DataFrame([car.model_dump(include=include) for car in cars])
  df.drop_duplicates(subset=['vin'], inplace=True)
  df.fillna({ 'trim': '' }, inplace=True)
  df['comment'] = df['year'].astype(str) + ' ' + df['make'] + ' ' + df['model'] + ' ' + df['trim']
  print(df.to_csv(columns=['comment', 'vin'], index=False))
