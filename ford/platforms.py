from functools import cache

from openpilot.selfdrive.car.docs_definitions import split_name
from openpilot.selfdrive.car.ford.values import CAR


@cache
def find_openpilot_platform(car_name: str) -> str | None:
  make, model, year = split_name(car_name)

  for platform in CAR:
    # TODO: handle Focus Mk3 vs Mk4 (pass market as arg?)
    if platform == CAR.FOCUS_MK4:
      continue

    if not platform.config.car_info:
      continue

    car_infos = platform.config.car_info if isinstance(platform.config.car_info, list) else [platform.config.car_info]
    for car_info in car_infos:
      if car_info.make.upper() != make:
        continue
      if car_info.model != model:
        continue
      if year not in car_info.year_list:
        continue
      return platform

  return None
