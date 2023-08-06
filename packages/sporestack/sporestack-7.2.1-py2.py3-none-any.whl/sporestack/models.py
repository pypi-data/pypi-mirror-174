"""

SporeStack API supplemental models

"""


from typing import Optional

from pydantic import BaseModel


class NetworkInterface(BaseModel):
    ipv4: str
    ipv6: str


class Payment(BaseModel):
    txid: Optional[str]
    uri: Optional[str]
    usd: str
    paid: bool


class Flavor(BaseModel):
    # Unique string to identify the flavor that's sort of human readable.
    slug: str
    # Number of vCPU cores the server is given.
    cores: int
    # Memory in Megabytes
    memory: int
    # Disk in Gigabytes
    disk: int
    # USD cents per day
    price: int
    # IPv4 connectivity: "/32"
    ipv4: str
    # IPv6 connectivity: "/128"
    ipv6: str
    # Gigabytes of bandwidth per day
    bandwidth: int
