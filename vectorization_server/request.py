import requests
from skimage import io
import json
import matplotlib.pyplot as plt
import numpy as np


# resp = requests.post("http://localhost:3000/tosvg", files={"file":open('temp.png','rb')})

resp = requests.post("http://localhost:3000/tosvg", files={"file":open('temp.png','rb')})
json_load = resp.json()
a_restored = np.asarray(json_load["output"])
print(a_restored)
