# -*- coding: utf-8 -*-
   
"""
Created on Sun Jul  6 01:00:52 2025

@author: russ
@model: o3

# SurfaceLocation.py

A surface location wrapper.

Requires:
    pip install astropy numpy
"""
from __future__ import annotations
from dataclasses import dataclass  # , field
"""
from typing import Optional
"""
import numpy as np
from astropy import units as u
from astropy.coordinates import EarthLocation, CartesianRepresentation
from astropy.time import Time

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError


# ---------------------------------------------------------------------------
#  SurfaceLocation -- holds latitude/longitude (+ optional height) on a body
# ---------------------------------------------------------------------------
@dataclass
class SurfaceLocation:
    """
    A geodetic / planetocentric position on the surface of a Solar-System body.

    lat, lon are stored as astropy Quantities (angle units).
    alt is stored as an astropy Quantity (length, default 0 m).

    • Earth:  WGS-84 ellipsoidal latitude/longitude (positive-north, positive-east).
    • Moon / Mars:  IAU-2015 planetocentric lat & east lon, spherical radius model.
    """
    def __init__(self, body: str, lat: float, long: float, alt: float = 0.0):
        """
        Represents a location on or above a solar-system body.
        """
        self.body = body
        self.latitude = lat * u.deg
        self.longitude = long * u.deg
        self.altitude = alt * u.m
        """
    body: str
    lat: u.Quantity      # e.g. 37.4 * u.deg
    lon: u.Quantity      # e.g. -122.0 * u.deg   (negative = west)
    altitude: u.Quantity = 0 * u.m
    """
    # body-specific mean radii (IAU 2015 values; Earth omitted because EarthLocation
    # already has WGS-84)
    _MEAN_RADIUS = {
        "moon": 1_737.4 * u.km,
        "mars": 3_389.5 * u.km,
    }

    # ---------------------------------------------------------------------
    #  Convenience helpers
    # ---------------------------------------------------------------------
    def to_earthlocation(self) -> EarthLocation:
        """Return an astropy EarthLocation (only if body == 'earth')."""
        if self.body.lower() != "earth":
            raise ValueError("to_earthlocation is defined only for Earth")
        return EarthLocation(lat= self.lat, lon= self.lon, height= self.height)

    def to_cartesian(self, obstime: Time | None = None) -> CartesianRepresentation:
        """
        Cartesian representation (x,y,z) in meters from the body centre.
        • Earth: uses ITRS frame at obstime if supplied, else J2000.
        • Moon / Mars: simple spherical conversion using mean radius.
        """
        body = self.body.lower()
        if body == "earth":
            loc = self.to_earthlocation()
            # Convert to ITRS cartesian at the given epoch (or default)
            return loc.get_itrs(obstime or Time("J2000")).cartesian

        if body not in ("moon", "mars"):
            raise ValueError(f"No conversion defined for body '{self.body}'")

        r = self._MEAN_RADIUS[body] + self.height.to(u.km)
        lat_rad = self.lat.to(u.rad).value
        lon_rad = self.lon.to(u.rad).value
        x = r * np.cos(lat_rad) * np.cos(lon_rad)
        y = r * np.cos(lat_rad) * np.sin(lon_rad)
        z = r * np.sin(lat_rad)
        return CartesianRepresentation(x.to(u.m), y.to(u.m), z.to(u.m))
    
    @classmethod
    def from_place_name(
        cls,
        place_name: str,
        body: str = "Earth",
        user_agent: str = "surface_location_geocoder",
        timeout: int = 10
    ) -> "SurfaceLocation":
        """
        Geocode a place name into a SurfaceLocation.

        :param place_name: e.g. "The White House"
        :param body:       reference body name (default "Earth")
        :param user_agent: required by Nominatim
        :param timeout:    seconds before giving up
        :raises ValueError: if geocoding fails
        """
        geolocator = Nominatim(user_agent=user_agent, timeout=timeout)
        try:
            loc = geolocator.geocode(place_name)
        except GeocoderServiceError as e:
            raise ValueError(f"Geocoding service error: {e}")
        if loc is None:
            raise ValueError(f"Could not geocode place name: {place_name!r}")
        # Nominatim doesn’t supply altitude, so we default to 0.0
        return cls(body, loc.latitude, loc.longitude, altitude=0.0)

    def to_place_name(
        self,
        user_agent: str = "surface_location_geocoder",
        timeout: int = 10,
        exactly_one: bool = True
    ) -> str:
        """
        Reverse-geocode this SurfaceLocation back to a place name/address.

        :param user_agent: required by Nominatim
        :param timeout:    seconds before giving up
        :param exactly_one: if False, you get a list of matches
        :raises ValueError: if reverse lookup fails
        """
        geolocator = Nominatim(user_agent=user_agent, timeout=timeout)
        try:
            loc = geolocator.reverse(
                (self.latitude, self.longitude),
                exactly_one=exactly_one
            )
        except GeocoderServiceError as e:
            raise ValueError(f"Reverse geocoding service error: {e}")

        if loc is None:
            raise ValueError(
                f"Could not reverse geocode coordinates: "
                f"({self.latitude}, {self.longitude})"
            )
        # If exactly_one=False, `loc` is a list; handle that case if needed.
        return loc.address if exactly_one else [l.address for l in loc]
    
    # ----------------
    #  String helpers
    # ----------------
    def __str__(self) -> str:
        out = [f"{self.body} [{self.latitude}, {self.longitude}] @ {self.altitude}"]
        """
        if self.location:
            out.append(
                f" @ lat={self.location.lat.to_value(u.deg):.3f}°, "
                f"lon={self.location.lon.to_value(u.deg):.3f}°, "
                f"h={self.location.height.to(u.m).value:.0f} m"
            )
        """
        return "".join(out)

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
    print(giza)
    print(giza.to_place_name())

    # 2) Mars landing site (Gale Crater) on 12 Dec 2030 18:30 TDB
    gale = SurfaceLocation(
        body="mars",
        lat=-4.5895 * u.deg,   # south = negative
        long=137.4417 * u.deg,  # areocentric east longitude
        alt=-4500 * u.m,    # altitude relative to areoid
    )
    print(gale)