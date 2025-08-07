# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 21:13:51 2025

@author: russ
@model: o4-mini-high
"""

from datetime import datetime, timezone, timedelta

# Define PDT timezone (UTC-7)
pdt = timezone(timedelta(hours=-7))

# Create datetime for 2:12 AM PDT on July 4, 2025
dt_pdt = datetime(2025, 7, 4, 2, 12, tzinfo=pdt)

# Convert to UTC
dt_utc = dt_pdt.astimezone(timezone.utc)

# Print UTC time
print("UTC time:", dt_utc.strftime("%Y-%m-%d %H:%M:%S %Z"))

# Calculate milliseconds since Unix epoch
epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
milliseconds_since_epoch = int((dt_utc - epoch).total_seconds() * 1000)

# Print milliseconds
print("Milliseconds since epoch:", milliseconds_since_epoch)

# Return value (for use in an epoch start definition)
milliseconds_since_epoch
