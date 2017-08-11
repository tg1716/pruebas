import matplotlib.pyplot as plt
import numpy as np

image = np.empty((1376,960,np.uint16))

image.data[:]=open('mapa1').read()

plt.imshow(image)
