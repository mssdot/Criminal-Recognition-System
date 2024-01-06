import numpy as np 
import pickle
import cv2
from datetime import datetime
import os
from os import listdir 
from PIL import Image as Img
from numpy import asarray
from numpy import expand_dims
from keras_facenet import FaceNet
import requests

class Model:
	def __init__(self ): 
		# import database of trained faces.
		myfile = open("datafinal3.pkl", "rb")
		self.database = pickle.load(myfile)
		myfile.close()
		self.oncecreatefolder= True # for video processing
		self.folder=  ''
		self.oncecreatefolder2= True # for video processing
		self.folder2=  ''
#.......................................................IMAGE......................................................................		
	#create a function to precoess new imgae
	def process(self,imagepath):
		folder=self.createFolder()

		HaarCascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml' )
		MyFaceNet = FaceNet()
		gbr1 = cv2.imread(imagepath)
		identity=''
		faces = HaarCascade.detectMultiScale(gbr1,1.1,4) 
		for (x1,y1,w,h) in faces:
			x1, y1 = abs(x1), abs(y1)
			x2, y2 = x1 + w, y1 + h 
			gbr = cv2.cvtColor(gbr1,cv2.COLOR_BGR2RGB)
			gbr = Img.fromarray(gbr)
			gbr_array = asarray(gbr)
			face = gbr_array[y1:y2, x1:x2]                        
			
			face = Img.fromarray(face)                       
			face = face.resize((160,160))
			face = asarray(face)
			
			#face = face.astype('float32')
			#mean, std = face.mean(), face.std()
			#face = (face - mean) / std
			
			face = expand_dims(face, axis=0)
			signature = MyFaceNet.embeddings(face)    
			min_dist=100
			
			detectedList  = []
			for key, value in self.database.items() :
				dist = np.linalg.norm(value-signature)
				if dist < min_dist:
					min_dist = dist
					identity = key

				 

			cv2.putText(gbr1,identity.title(), (x1,y1),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
			cv2.rectangle(gbr1,(x1,y1),(x2,y2), (0,255,0), 2)
			 
			cv2.imwrite(os.path.join(folder,f'criminal is {identity.title()}.jpg'),gbr1)
		if(identity==''):	 
			return [folder,'unknown']
		return [folder,identity]

	def createFolder(self): 
		current_datetime = datetime.now()

		date_time_string = current_datetime.strftime("%Y_%m_%d_%H%M%S")
		folder_name = date_time_string
		output_directory = '/home/student/Desktop/VE/IMAGE OUTPUT' 

		# Create the full path for the new folder
		new_folder_path = os.path.join(output_directory, folder_name)

		# Check if the folder already exists
		if not os.path.exists(new_folder_path): 
			os.makedirs(new_folder_path)
		print(new_folder_path)
		return new_folder_path	 

	def sendImgEmail(self,dirlist,to_email):
		
		data = {
		    "to_email": to_email,
		    "subject": "Criminal Detection From Image File",
		    "body": "",
			"dirlist":dirlist
		}
		response = requests.post("http://localhost:5000/send_email", data=data )
		return response

	#....................................................................video....................................................

	def videoprocess(self,gbr1):
		if self.oncecreatefolder:
			self.folder=self.createVideoFolder()	
			self.oncecreatefolder = False
		detectedList = []

		#gbr2 = cv2.resize(gbr1, (600, 600))
		HaarCascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml' )
		MyFaceNet = FaceNet()
		wajah = HaarCascade.detectMultiScale(gbr1, 1.1, 4)

		for (x1, y1, w, h) in wajah:
			x1, y1 = abs(x1), abs(y1)
			x2, y2 = x1 + w, y1 + h
			gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
			gbr = Img.fromarray(gbr)
			gbr_array = asarray(gbr)
			face = gbr_array[y1:y2, x1:x2]
			face = Img.fromarray(face)
			face = face.resize((160, 160))
			face = asarray(face)

			face = expand_dims(face, axis=0)
			signature = MyFaceNet.embeddings(face)
			min_dist = 100
			identity = ''

			for key, value in self.database.items():
				dist = np.linalg.norm(value - signature)
				if dist < min_dist:
					min_dist = dist
					identity = key

			cv2.putText(gbr1, identity, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
			cv2.rectangle(gbr1, (x1, y1), (x2, y2), (0, 255, 0), 2)
			if identity.lower() != 'unknown'  :
				if identity.lower() not in detectedList:
					detectedList.append(identity.lower())
					cv2.imwrite(os.path.join(self.folder, f'criminal is {identity}.jpg'), gbr1)
			 
		return [gbr1,detectedList,self.folder]

	def createVideoFolder(self): 
		current_datetime = datetime.now()

		date_time_string = current_datetime.strftime("%Y_%m_%d_%H%M%S")
		folder_name = date_time_string
		output_directory = '/home/student/Desktop/VE/VIDEO OUTPUT' 

		# Create the full path for the new folder
		new_folder_path = os.path.join(output_directory, folder_name)

		# Check if the folder already exists
		if not os.path.exists(new_folder_path): 
			os.makedirs(new_folder_path)
		print(new_folder_path)
		return new_folder_path	
	def sendVidEmail(self,dirlist,to_email):
		data = {
			"to_email": to_email,
			"subject": "Criminal Detection From Video File",
			"body": "",
			"dirlist":dirlist
		}
		response = requests.post("http://localhost:5000/send_email", data=data )
		return response


	#..............................................webcam.....................................................
	def webcamprocess(self,gbr1):
		if self.oncecreatefolder2:
			self.folder2=self.createCamFolder()	
			self.oncecreatefolder2 = False
		detectedList = []
		 
		
		#gbr1 = cv2.resize(gbr1, (600, 600))
		HaarCascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml' )
		MyFaceNet = FaceNet()
 

		wajah = HaarCascade.detectMultiScale(gbr1,1.1,4)
    
		for (x1,y1,w,h) in wajah:
			x1, y1 = abs(x1), abs(y1)
			x2, y2 = x1 + w, y1 + h
			gbr = cv2.cvtColor(gbr1,cv2.COLOR_BGR2RGB)
			gbr = Img.fromarray(gbr)
			gbr_array = asarray(gbr)
			face = gbr_array[y1:y2, x1:x2]                        
			
			face = Img.fromarray(face)                       
			face = face.resize((160,160))
			face = asarray(face)
			
			#face = face.astype('float32')
			#mean, std = face.mean(), face.std()
			#face = (face - mean) / std
			
			face = expand_dims(face, axis=0)
			signature = MyFaceNet.embeddings(face)    
			min_dist=100
			identity=''
			for key, value in self.database.items() :
				dist = np.linalg.norm(value-signature)
				if dist < min_dist:
				    min_dist = dist
				    identity = key
				
			cv2.putText(gbr1,identity, (x1,y1),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
			cv2.rectangle(gbr1,(x1,y1),(x2,y2), (0,255,0), 2)
			if identity != 'Unknown' or identity != 'unknown':
				if identity.lower() not in detectedList:
					detectedList.append(identity.lower())
					cv2.imwrite(os.path.join(self.folder2, f'criminal is {identity}.jpg'), gbr1)
		return [gbr1,detectedList,self.folder2]

	def getfoldername(self):
		print(self.folder2)
		return self.folder2

	def createCamFolder(self): 
		current_datetime = datetime.now()

		date_time_string = current_datetime.strftime("%Y_%m_%d_%H%M%S")
		folder_name = date_time_string
		output_directory = '/home/student/Desktop/VE/WEBCAM OUTPUT' 

		# Create the full path for the new folder
		new_folder_path = os.path.join(output_directory, folder_name)

		# Check if the folder already exists
		if not os.path.exists(new_folder_path): 
			os.makedirs(new_folder_path)
		print(new_folder_path)
		return new_folder_path	

	def sendCamEmail(self,dirlist,to_email):
		data = {
		    "to_email": to_email,
		    "subject": "Criminal Detection From WebCam  ",
		    "body": "",
			"dirlist":dirlist
		}
		response = requests.post("http://localhost:5000/send_email", data=data )
		return response
