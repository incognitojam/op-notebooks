from functools import cache

from openpilot.selfdrive.car.docs_definitions import split_name
from openpilot.selfdrive.car.ford.values import CAR, CAR_INFO


@cache
def find_openpilot_platform(car_name: str) -> str | None:
  make, model, year = split_name(car_name)

  for platform, car_infos in CAR_INFO.items():
    # TODO: handle Focus Mk3 vs Mk4 (pass market as arg?)
    if platform == CAR.FOCUS_MK4:
      continue

    car_infos = car_infos if isinstance(car_infos, list) else [car_infos]
    for car_info in car_infos:
      if car_info.make.upper() != make:
        continue
      if car_info.model != model:
        continue
      if year not in car_info.year_list:
        continue
      return platform

  return None
