# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 20:49:55 2025

@author: russ
@model: o3
"""

import time
import threading

class SnowflakeGenerator:
    """
    Twitter Snowflake 64-bit ID generator implementation.
    
    REALagentic.AI Changes:
        1. UTC time: 2025-07-04 09:12:00 UTC
           Milliseconds since epoch: 1751620320000
    """
    # def __init__(self, datacenter_id: int, worker_id: int, twepoch: int = 1288834974657): # Twitter: 
    def __init__(self, datacenter_id: int, worker_id: int, reepoch: int = 1751620320000): # REALagentic.AI: July 4, 2025
        # Bit allocations
        self.datacenter_id_bits = 5
        self.worker_id_bits = 5
        self.sequence_bits = 12

        # Maximum values
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

        # Bit shifts
        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_left_shift = (
            self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits
        )

        # Validate IDs
        if not (0 <= datacenter_id <= self.max_datacenter_id):
            raise ValueError(f"datacenter_id must be between 0 and {self.max_datacenter_id}")
        if not (0 <= worker_id <= self.max_worker_id):
            raise ValueError(f"worker_id must be between 0 and {self.max_worker_id}")

        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = 0
        self.last_timestamp = -1
        self.reepoch = reepoch
        self.lock = threading.Lock()

    def _time_gen(self) -> int:
        """
        Return current time in milliseconds.
        """
        return int(time.time() * 1000)

    def _til_next_millis(self, last_timestamp: int) -> int:
        """
        Block until the next millisecond.
        """
        timestamp = self._time_gen()
        while timestamp <= last_timestamp:
            timestamp = self._time_gen()
        return timestamp

    def get_id(self) -> int:
        """
        Generate the next Snowflake ID.
        """
        with self.lock:
            timestamp = self._time_gen()

            # Handle clock rollback
            if timestamp < self.last_timestamp:
                raise Exception(
                    f"Clock moved backwards. Refusing to generate id for {self.last_timestamp - timestamp}ms"
                )

            if timestamp == self.last_timestamp:
                # Same millisecond: increment sequence
                self.sequence = (self.sequence + 1) & self.sequence_mask
                if self.sequence == 0:
                    # Sequence overflow: wait for next millisecond
                    timestamp = self._til_next_millis(self.last_timestamp)
            else:
                # New millisecond: reset sequence
                self.sequence = 0

            self.last_timestamp = timestamp

            # Compose ID
            sf_id = (
                ((timestamp - self.reepoch) << self.timestamp_left_shift)
                | (self.datacenter_id << self.datacenter_id_shift)
                | (self.worker_id << self.worker_id_shift)
                | self.sequence
            )
            return sf_id

# Default generator (customize IDs as needed)
_default_snowflake = SnowflakeGenerator(datacenter_id=0, worker_id=0)


def snowflake() -> int:
    """
    Generate a new Snowflake ID using Twitter's 64-bit implementation
    as modified by REALagentic AI.
    """
    return _default_snowflake.get_id()


# Example usage
if __name__ == "__main__":
    # Generate 5 sample IDs
    for _ in range(5):
        print(snowflake())
    time.sleep(2)
    for _ in range(5):
        print(snowflake())

"""
What implementation of Snowflake IDs does X.com use today?
Thought for 47 seconds
X (Snowflake) in mid-2025: still the classic 64-bit layout
X (formerly Twitter) still issues 64-bit, time-ordered “Snowflake” IDs for every Tweet, DM, user, media object, list, Collection item, etc. The public API, data archives and on-site HTML all expose the same structure announced in 2010 and documented today on the X developer site:

Field	Bits	Description	Notes
Sign / reserved	1	Always 0 so the number fits in a signed 64-bit int	—
Timestamp	41	Milliseconds since the X epoch 128 883 497 4657 ms (4 Nov 2010 01:42:54.657 UTC)	Covers ≈ 69 years ⇒ rolls over in 2080
Machine ID	10	Identifies the Snowflake worker; in Twitter’s reference code this is split 5 bits datacenter + 5 bits worker	Up to 1024 distinct workers
Sequence	12	Per-worker counter that resets each millisecond	Up to 4 096 IDs per worker per ms

Total: 64 bits (63 useful). The IDs are sortable and can be decoded back to UTC time. All modern client libraries must read the string version (id_str) because the integer exceeds JavaScript’s 53-bit safe range. 
developer.x.com
developer.x.com
en.wikipedia.org

What hasn’t changed
Epoch & bit split: No public evidence (as of July 2025) that X moved to a new epoch, added more bits, or adopted a 128-bit variant. Internal services may split the 10 “machine” bits differently, but the external 64-bit shape is stable.

Return fields: Every object still carries both id (64-bit) and id_str (decimal string). Developer docs, updated 2025, highlight exactly the same behaviour. 
developer.x.com

Example decode
Snowflake 1851515326581916096 (Elon Musk post April 2024):

Strip sign → 63 bits

Timestamp bits → 1701736398955 ms → 2023-12-04 17:13:18.955 UTC

Machine + sequence bits → decode to the generating worker and per-ms counter.

Why X hasn’t outgrown 64 bits yet
Capacity: 1024 workers × 4096 IDs / ms = ≈ 4.2 billion IDs per second—far above peak site traffic.

Back-compat: trillions of existing Snowflakes sit in caches, URLs, JSON archives, and 3rd-party databases.

Sorting & sharding logic across hundreds of internal services assumes the 64-bit layout.

Alternatives X could adopt (none announced)
Scheme	Pros	Cons
Extended-Snowflake (96-/128-bit)	Future-proof, room for larger worker pools, nanosecond precision	Breaks existing clients & storage unless a new field is added
ULID/KSUID	Lexicographically sortable strings, >128 b entropy	26–27 char text, not compact ints; extra migration layer
Mixed radix (base62 or base36) Snowflake	Shorter URLs	Added encoding/decoding overhead

If X ever decided to migrate, the most likely path would be an “id2_str” or “snowflake64” → “snowflake128” dual-field period, mirroring the original move from 32-bit to Snowflake in 2010.

Bottom line: As of July 2025, X.com still generates 64-bit Snowflake IDs with the original 41-10-12 bit allocation and the same 2010 epoch. No public documentation or API change suggests a new format.
"""

