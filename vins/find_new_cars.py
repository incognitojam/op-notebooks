#!/usr/bin/env python3
from notebooks.ford.vins import load_csv
from notebooks.vins.cars_com import Make, Model, search_cars, SortBy, StockType


def find_new_cars():
  df_existing_vins = load_csv()
  existing_vins = set(df_existing_vins['vin'])

  extra_args = dict(
    page_size=25,
    stock_type=StockType.USED,
    sort=SortBy.NEWEST_LISTED,
  )

  # queries = [
  #   dict(models=[Model.FORD_BRONCO_SPORT]),
  #   dict(models=[Model.FORD_EDGE], year_min=2019),
  #   dict(models=[Model.FORD_ESCAPE, Model.FORD_ESCAPE_PHEV], year_min=2020),
  #   dict(models=[Model.FORD_E_TRANSIT]),
  #   dict(models=[Model.FORD_EXPLORER], year_min=2020),
  #   dict(models=[Model.FORD_F_150], year_min=2021),
  #   dict(models=[Model.FORD_F_150_LIGHTNING]),
  #   dict(models=[Model.FORD_MAVERICK]),
  #   dict(models=[Model.FORD_MUSTANG], year_min=2024),
  #   dict(models=[Model.FORD_MUSTANG_MACH_E]),
  #   dict(models=[Model.LINCOLN_AVIATOR], year_min=2020),
  #   dict(models=[Model.LINCOLN_CORSAIR], year_min=2020),
  #   dict(models=[Model.LINCOLN_NAUTILUS], year_min=2019),
  #   dict(models=[Model.LINCOLN_NAVIGATOR, Model.LINCOLN_NAVIGATOR_L], year_min=2022),
  # ]

  for query in [dict(makes=[Make.FORD, Make.LINCOLN], year_min=2019, page_size=100, page=page) for page in range(10)]:
    for car in search_cars(**dict(extra_args, **query)):
      if car.vin not in existing_vins:
        yield car


if __name__ == '__main__':
  import pandas as pd

  include=['make', 'model', 'year', 'trim', 'vin']
  cars = list(find_new_cars())
  if len(cars) == 0:
    print('No new cars found')
    exit(0)
  df = pd.DataFrame([car.model_dump(include=include) for car in cars])
  df['comment'] = df['year'].astype(str) + ' ' + df['make'] + ' ' + df['model'] + ' ' + df['trim']
  print(df.to_csv(columns=['comment', 'vin'], index=False))
