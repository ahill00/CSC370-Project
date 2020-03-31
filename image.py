import matplotlib.pyplot as plt

from skimage import color, io
from skimage.feature import canny

image = img = io.imread('/Users/andy/code/csc508/car_ims/car.jpeg')
image = color.rgb2gray(image)

edges = canny(image, sigma=4)
edges1 = canny(image)
edges2 = canny(image, sigma=5)

# display results
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                    sharex=True, sharey=True)

ax1.imshow(image, cmap=plt.cm.gray)
ax1.axis('off')
ax1.set_title('noisy image', fontsize=20)

ax2.imshow(edges1, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title(r'Canny filter, $\sigma=1$', fontsize=20)

ax3.imshow(edges2, cmap=plt.cm.gray)
ax3.axis('off')
ax3.set_title(r'Canny filter, $\sigma=3$', fontsize=20)

fig.tight_layout()

plt.show()
