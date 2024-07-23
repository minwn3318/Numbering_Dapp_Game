from flask import Flask, request, jsonify
import requests
import json
from urllib.parse import urlparse
from Network_node1 import Blockchain, MerkleTree

