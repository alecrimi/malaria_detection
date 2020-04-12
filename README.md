# Current progress on our Malaria project
The idea is to have a complete system for acquisition, detection and report of malaria cases

![Overview](https://github.com/alecrimi/malaria_detection/blob/master/overview.jpg)

Acquisition is carried out by blood smear stained with Giemsa (protocol below) and visualized on a microscope with USB camera.
Captured images and then processed and feeded to a pretrained DeepLearning architecture.
Ultimately the diagnosis is mapped on a GIS system by using ArcPy.
The deeplearning architecture should run on a normal PC, a RaspberryPI or be integrated into an Android app.
 
<img src="https://github.com/alecrimi/malaria_detection/blob/master/overall.jpg" width="200" height="220" /> 

 
Giemsa Staining (thin film protocol):
- On a clean dry microscopic glass slide, make a thin film of the specimen (blood) and leave to air dry.
- Dip the smear (2-3 dips) into pure methanol for fixation of the smear, leave to air dry for 30seconds
- Flood the slide with the Giemsa stain solution.
- Flush with tap water and leave to dry
Different solution and time with Giemsa stain solution can be used, [check this report] (https://journals.sagepub.com/doi/full/10.1258/td.2010.100218?casa_token=8rA9Ezu6CvAAAAAA:313ryHWFaL0Vbv5aWVptYuDoTZbwm-RwrkZobBYeJXn6DmkMn8OfjxqmNO5IbyBKmK9exSdxkkfEDQ) 

GoogleColab with VGG19 without finetuning:
https://colab.research.google.com/drive/1CUcsmtg9S9ryJZAZrQsAf7e5ouUK4gL8#scrollTo=-NJ2CxM2Rf5d
<img src="https://github.com/alecrimi/malaria_detection/blob/master/FB_IMG_1582996617130.jpg" width="200" height="260" />
