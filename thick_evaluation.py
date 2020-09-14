#####################################################
                                                    
# written by Rija Tonny C. Ramarolahy               
                                                     
# 2020                                               
                                                    
# email: rija@aims.edu.gh / minuramaro@gmail.com   
                                                     
#####################################################



import cv2
import numpy as np
import matplotlib.pyplot as plt
#import tensorflow as tf
import sys 
import time 


### function to look for overlapping 
### intersection between two rectangles
def calculateIntersection(a0, a1, b0, b1):
	if a0 >= b0 and a1 <= b1: # Contained
		intersection = a1 - a0
	elif a0 < b0 and a1 > b1: # Contains
		intersection = b1 - b0
	elif a0 < b0 and a1 > b0: # Intersects right
		intersection = a1 - b0
	elif a1 > b1 and a0 < b1: # Intersects left
		intersection = b1 - a0
	else: # No intersection (either side)
		intersection = 0

	return intersection


def parasite_detection(image):

	model_name = 'models/CNN_thick_imgs.h5'
	try:
		model = tf.keras.models.load_model(model_name)
		model.compile(optimizer='adam',loss='binary_crossentropy',
						metrics=['accuracy'])
		print('Model loaded successfully')
	except:
		print('Model not found')


	t = time.time()
	#try:
	#	image = cv2.imread(image_name)
	#except:
	#	print('Image not found')
	image_copy = image.copy()
	gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY) 

	#find of the plasmodium candidate in the image
	blur = cv2.GaussianBlur(gray, (3,3), 0)
	## the two following threshold methods work but better result with the first.
	ret, thresh = cv2.threshold(blur, 125, 255, cv2.THRESH_BINARY_INV)
	#thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7,7)
	

	cnt, hier = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	count_candidate = 0
	count_plasmodium = 0

	#predicting the plasmodium canditates by our model 
	listold=[(0,0,0,0)]
	for c in cnt:
		overlap = False
		x, y, w, h = cv2.boundingRect(c)
		if w < 30 or h < 30:  #taking out the white blood cells
			x = np.where(x > 10, x - 10, x)
			y = np.where(y > 10, y - 10, y)
			w = 20
			h = 20 
			xmax = x+w
			ymax = y+h
			AREA = (xmax-x)*(ymax-y)

			# look the overlapping
			for xold, yold, xmaxold, ymaxold in listold:
				width = calculateIntersection(xold, xmaxold, x, xmax)        
				height = calculateIntersection(yold, ymaxold, y, ymax)        
				area = width * height
				ratio = area / AREA
				if ratio > 0.1:   # if area of intersection is > 0.1 don't take the new rectangle
					overlap = True
			if not overlap:
				count_candidate += 1
				Roi = image[y:y+h, x:x+w]
				Roi_image = cv2.resize(Roi,(50,50)) / 255.
				Roi_tf = tf.expand_dims(Roi_image, 0)
					
				label = model.predict(Roi_tf)
				label = np.where(label[0] > 0.5, 1, 0 )
				cv2.rectangle(image_copy, (x,y), (x+w+5, y+h+5),(0, 255, 255), 2)  ### yellow rectangle for the candidate 															plasmodium
				if label == 1:
					cv2.rectangle(image_copy, (x,y), (x+w, y+h),(0, 0, 255), 2)   ### red rectangle for the plasmodium by the 																model
					count_plasmodium += 1                
        
			xold = x 
			yold = y
			xmaxold = x+w
			ymaxold = y+h
			listold.append((xold,yold,xmaxold,ymaxold))


	elapsed_time = time.time() - t
            
	#cv2.imwrite(image_name+'detection.png', image_copy)
	print('Time for detection: ', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
	print('Number of candidate plasmodium: ', count_candidate)
	print('Number of plasmodium from the model: ', count_plasmodium)

	#plt.figure(figsize=(10,10))
	#plt.imshow(cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB))
	#plt.axis('off')
	#plt.show()
	return image_copy,count_plasmodium

''''
if __name__ == '__main__':
	model_name = sys.argv[1]
	image_name = sys.argv[2]
	try:
		model = tf.keras.models.load_model(model_name)
		model.compile(optimizer='adam',loss='binary_crossentropy',
						metrics=['accuracy'])
		print('Model loaded successfully')
	except:
		print('Model not found')
	parasite_detection(image_name=image_name, model=model)
'''	
	












