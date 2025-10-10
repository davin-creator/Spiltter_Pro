import pandas as pd
import numpy as np
import requests


url  = "http://api.coinapp.io/v2/assets"
header = {"Content-Type" : "application/json",
          "Accept-Encoding":"deflate"}


response = requests.get(url, headers=header)

print(response)