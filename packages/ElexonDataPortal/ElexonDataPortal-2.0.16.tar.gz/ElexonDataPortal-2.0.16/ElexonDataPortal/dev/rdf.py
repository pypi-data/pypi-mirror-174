# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/11-rdf.ipynb (unless otherwise specified).

__all__ = []

# Cell
import yaml
import requests
import matplotlib.pyplot as plt

from datacatalogtordf import Catalog
from oastodcat import OASDataService

import networkx as nx
from rdflib import Graph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph