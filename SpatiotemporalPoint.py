# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 01:00:52 2025

@author: russ
@model: o3

# universal_datetime.py

A minimal astronomical epoch + surface-location wrapper.

Requires:
    pip install astropy numpy
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, TypeAlias

# import numpy as np
from astropy import units as u
# from astropy.coordinates import EarthLocation, CartesianRepresentation
from astropy.time import Time
from SurfaceLocation import SurfaceLocation

# ---------------------------------------------------------------------------
#  SpatiotemporalPoint -- epoch (+ optional place on a body)
# ---------------------------------------------------------------------------
@dataclass
class SpatiotemporalPoint:
    """A timestamp anywhere, on (or above) any Solar-System body."""
    epoch: Time
    body: str = "earth"
    location: Optional[SurfaceLocation] = None

    # Optional metadata (e.g. description, ID) can be hung off this dict.
    meta: dict = field(default_factory=dict)

    # ----------------
    #  String helpers
    # ----------------
    def __str__(self) -> str:
        out = [f"{self.epoch.isot}  [{self.body}, scale={self.epoch.scale}]"]
        if self.location:
            out.append(
                f" @ lat={self.location.latitude.to_value(u.deg):.3f}°, "
                f"lon={self.location.longitude.to_value(u.deg):.3f}°, "
                f"h={self.location.altitude.to(u.m).value:.0f} m"
            )
        return "".join(out)

STPoint: TypeAlias = SpatiotemporalPoint

# ---------------------------------------------------------------------------
#  Quick sanity test when run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 1) Ancient Earth location (Great Pyramid of Giza) on 10 000 BCE midnight UTC
    giza = SurfaceLocation(
        body="earth",
        lat=29.9792 * u.deg,
        long=31.1342 * u.deg,
        alt=75 * u.m
    )

    t_ancient = SpatiotemporalPoint(
        epoch=Time(-1850000.5, format="jd", scale="utc"),
        body="earth",
        location=giza,
    )
    # print(t_ancient)
    # 2) Mars landing site (Gale Crater) on 12 Dec 2030 18:30 TDB
    gale = SurfaceLocation(
        body="mars",
        lat=-4.5895 * u.deg,   # south = negative
        long=137.4417 * u.deg,  # areocentric east longitude
        alt=-4500 * u.m,    # altitude relative to areoid
    )
    t_future = STPoint(
        epoch=Time("2030-12-12T18:30:00", scale="tdb"),
        body="mars",
        location=gale,
    )
    print(t_future)

"""    
    # 3) Cartesian check for the Mars location
    cart = gale.to_cartesian(t_future.epoch)
    print("Gale Crater (cartesian km):", cart.xyz.to(u.km))
"""