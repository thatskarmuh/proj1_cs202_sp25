
from dataclasses import dataclass
import math
from typing import *
import sys
import unittest
sys.setrecursionlimit(10**6)

@dataclass(frozen=True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float


@dataclass(frozen=True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str


@dataclass(frozen=True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float


#region1 Long beach Metro (where evan lives)
rect1 = GlobeRect(lo_lat=33.3, hi_lat=34.5, west_long=-118.5, east_long=-118.0)
region1 = Region(rect=rect1, name="Long Beach Metro", terrain="other")
rc1 = RegionCondition(region=region1, year=2025, pop=3000000, ghg_rate=12000000.0)
#-----------------------------------------------------------------------------------------
#region2 Tokyo Metro
rect2 = GlobeRect(lo_lat=35.5, hi_lat=35.9, west_long=139.5, east_long=140.0)
region2 = Region(rect=rect2, name="Tokyo Metro", terrain="other")
rc2 = RegionCondition(region=region2, year=2025, pop=14000000, ghg_rate=50000000.0)
#-----------------------------------------------------------------------------------------
#region3 Hawaii ocean region/ central pacfic area
rect3 = GlobeRect(lo_lat=18.5, hi_lat=22.5, west_long=-161.0, east_long=-154.0)
region3 = Region(rect=rect3, name="Hawaii", terrain="ocean")
rc3 = RegionCondition(region=region3, year=2025, pop=1500000, ghg_rate=3000000.0)
#-----------------------------------------------------------------------------------------
#region4 near calpoly but not any place that was said in the tasks
rect4 = GlobeRect(lo_lat=34.1, hi_lat=35.5, west_long=-120.8, east_long=-120.4)
region4 = Region(rect=rect4, name="San Luis Obispo", terrain="other")
rc4 = RegionCondition(region=region4, year=2025, pop=51000, ghg_rate=200000.0)

region_conditions = [rc1, rc2, rc3, rc4]


def emissions_per_capita(rc:RegionCondition)-> float:
    if rc.pop==0:
        return 0.0
    return rc.ghg_rate / rc.pop

def area(gr:GlobeRect)-> float:
    r = 6378.1 #RADIUS EARTH IN KILOMETERS why am I yelling
    width= gr.east_long - gr.west_long
    if width < 0:
        width += 360

    width = math.radians(width)
    lo_lat = math.radians(gr.lo_lat)
    hi_lat =  math.radians(gr.hi_lat)

    return (r**2) * width * abs(math.sin(hi_lat) - math.sin(lo_lat))

def emissions_per_square_km(rc:RegionCondition)-> float:
    a = area(rc.region.rect)
    if a==0:
        return 0.0
    return rc.ghg_rate / a

def densest(rc_list: list[RegionCondition]) -> str:
    def densest_rc(lst: list[RegionCondition]) -> RegionCondition:
        if len(lst) == 1:
            return lst[0]

        first = lst[0]
        best_rest = densest_rc(lst[1:])

        first_density = first.pop / area(first.region.rect)
        rest_density = best_rest.pop / area(best_rest.region.rect)

        if first_density > rest_density:
            return first
        else:
            return best_rest

    return densest_rc(rc_list).region.name

def project_condition(rc:RegionCondition, years: int)-> RegionCondition:
    terrain= rc.region.terrain

    if terrain == "ocean":
        rate = 0.0001
    elif terrain == "mountains":
        rate = 0.0005
    elif terrain == "forest":
        rate = -0.00001
    else:
        rate = 0.0003

    new_year = rc.year + years

    if rc.pop == 0:
        new_pop = 0
        new_ghg = 0.0

    else:
        growth_factor = (1 + rate) ** years
        new_pop = int(rc.pop * growth_factor)
        new_ghg = rc.ghg_rate * (new_pop / rc.pop)

    return RegionCondition(
        region = rc.region,
        year = new_year,
        pop = new_pop,
        ghg_rate = new_ghg
    )
