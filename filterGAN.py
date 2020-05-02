from skimage import io
filename =  '/home/alecrimi/Dokumente/temo/samples_949_1.png'
cell = io.imread(filename)
from skimage.restoration import denoise_tv_chambolle
io.imshow(denoise_tv_chambolle(cell, weight=0.2, multichannel=True))
