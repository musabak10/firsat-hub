"""Scraper Sources Package"""
from .base import Source
from .youthall import YouthallSource
from .coderspace import CoderspaceSource
from .techcareer import TechcareerSource
from .patika import PatikaSource
from .kommunity import KommunitySource

__all__ = [
    "Source",
    "YouthallSource",
    "CoderspaceSource",
    "TechcareerSource",
    "PatikaSource",
    "KommunitySource",
]
