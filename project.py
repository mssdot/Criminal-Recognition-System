import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import filedialog ,messagebox
import os 
from model import  Model
import cv2
 
import numpy as np
from keras_facenet import FaceNet
import pickle
from datetime import datetime
import requests

class MajorProject:
	def __init__(self,name="Criminal Detection System"):
		
		# emai tomail name setup...............
		self.toMail  ='mss182311@gmail.com'


		#image library methods
		self.model = Model()

		#gui
		self.root = tk.Tk()
		self.root.title(name)	
		#self.root.title(name)
		self.root.config(bg= "black") #000807
			

		
		#................................................
		# Set the window size to be 400 pixels wide and 300 pixels tall
		width = 1000
		height = 650
		self.width = 1000
		self.height = 650

		# Calculate the screen width and height
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()

		# Calculate the x and y coordinates for the Tkinter window to be centered
		x = (screen_width - width) // 2
		y = (screen_height - height) // 2
 

		# Set the geometry of the window
		self.root.geometry(f"{width}x{height}+{x}+{y}")
		#root.geometry("400x300")
		
		#...........................................................................................

 		#top frame for heading
		self.topframe = tk.Frame(self.root, width=width, height=20, bg="purple")
		self.topframe.grid(row=0, column=0, padx=0, pady=5,columnspan=4, sticky='nsew')

		#heading
		label = tk.Label(self.topframe, text='Criminal Detection Smart System', anchor='center', justify='center' ,bg='black' ,fg='white',font=("Arial", 30,'bold'))
		label.pack(expand=True, fill='both') 

		#...........................................................................................
		#left frame for gif image
		self.leftframe = tk.Frame(self.root, width=600, height=height-20, bg="green")
		self.leftframe.grid(row=1, column=0, padx=0, pady=0)
		self.leftframe.config(bg="black")
 
		#background image:
		 
		self.gif_path = '/home/student/Desktop/VE/guiimg/1.gif'
		self.info = Image.open(self.gif_path) 
		self.frames = self.info.n_frames  # number of frames

		# Create a list to store PhotoImage objects for each frame
		self.photoimage_objects = [tk.PhotoImage(file=self.gif_path, format=f"gif -index {i}") for i in range(self.frames)]

		# Create a Label widget to display the animated background
		self.background_label = tk.Label(self.leftframe,bg="black")
		self.background_label.grid( row=0, column=0)
		self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

		# Variable to keep track of the current frame
		self.current_frame = 0

		# Start the animation
		self.animation()

		#...........................................................................................
		#right frame
		self.rightframe = tk.Frame(self.root, width=500, height=height-20, bg="black")
		self.rightframe.grid(row=1, column=1, padx=0, pady=0)
		
		#buttons:image , video, camera
		self.btnimg = tk.Button(self.rightframe, text="Image", command=self.imgbtn,bg="Yellow",fg="black").grid( row=0, column=0, padx=110, pady=20, ipadx=40, ipady=10)
		self.btnvid = tk.Button(self.rightframe, text="Video", command=self.vidbtn,bg="Yellow",fg="black").grid( row=	1, column=0, padx=80, pady=20, ipadx=40, ipady=10)
		self.btncam = tk.Button(self.rightframe, text="Camera", command=self.cambtn,bg="Yellow",fg="black").grid( row=2, column=0, padx=80, pady=20, ipadx=40, ipady=10)
 
		
		 
		 #...........................................................................................
		#Image frame when img button gets clciked.
		self.ImgFrame = tk.Frame(self.root, width=width, height=height  ) 
		 

		 #...........................................................................................
		#Video frame when vid button gets clciked.
		
		self.VidFrame = tk.Frame(self.root, width=1000, height=height , bg="pink") 
 
		 

		 #...........................................................................................
		#Camera frame when vid button gets clciked.
		
		self.CamFrame = tk.Frame(self.root, width=1000, height=height , bg="green") 
 
		
 


		# Bind the 'q' key event to the close_window function
		self.root.bind('<Key>', self.close_window)















#.....................................................Image methods..............................	 



	def imgbtn(self):
		# Hide the existing frames
		self.topframe.grid_forget()
		self.leftframe.grid_forget()
		self.rightframe.grid_forget()

		# Show the new frame
		self.ImgFrame.grid(row=0, column=1 )	 
		self.root.config(bg= "black") 
		self.afterimgbtnclick( )
	def afterimgbtnclick(self):


		#topframe : filebox , back btn
		self.topimgframe = tk.Frame(self.ImgFrame, width=self.width, height=30, bg="gray")
		self.topimgframe.grid(row=0, column=0, padx=0, pady=0,columnspan=4, sticky='nsew')

		
		self.backimg1 = tk.PhotoImage(file="back.png")
		self.backimg = tk.Button(self.topimgframe, image=self.backimg1 , command=self.backToMainWindow1  ).grid( row=0, column=0 ,padx=5)

		self.fileopen = tk.Button(self.topimgframe, text="Open File" ,command=self.open_file_dialog).grid( row=0, column=1  ,padx=5 ,sticky="e")
		
		self.emailimglabel=tk.Label(self.topimgframe  ,bg='gray')
		self.emailimglabel.grid(row=0, column=2,padx=5 ,sticky="e" )
		
		#space:
		self.spaceimgframe = tk.Frame(self.ImgFrame, width=1000, height=5, bg="black").grid(row=1, column=0, padx=0, pady=0,columnspan=4, sticky='nsew')

		#lefttop
		self.leftimgframe = tk.Frame(self.ImgFrame, width=400, height=self.height-30, bg="yellow")
		self.leftimgframe.grid(row=2, column=0, padx=0, pady=0)

		

		#leftframe.1 >> for input image
		self.inputimageframe = tk.Frame(self.leftimgframe, width=400, height=300, bg="gray")
		self.inputimageframe.grid_propagate(0)
		self.inputimageframe.grid(row=0, column=0, padx=0, pady=0 ,  sticky='nsew')
		self.inputimagelabel=tk.Label(self.leftimgframe,text="No Image is Selected" ,bg='gray')
		self.inputimagelabel.grid(row=0, column=0 )
		self.photox= None
		self.inputimage = tk.Label(self.inputimageframe  )
		self.inputimage.grid(row=1, column=0  ,padx=0, pady=0)
		
		#leftframe.2 >> for criminals detected list
 
		self.criminallistframe = tk.Frame(self.leftimgframe, width=400, height=300, bg="red")
		self.criminallistframe.grid_propagate(0)
		self.criminallistframe.grid(row=1, column=0, padx=0, pady=0 ,  sticky='nsew')
		
		self.criminalnameHeading=tk.Label(self.criminallistframe ,text='Detected Criminal Names       ' ,bg='pink',fg='red'  ,font=("Comic Sans MS", 20,'bold') )
		self.criminalnameHeading.grid(row=0, column=0, padx=0, pady=2,   sticky='nsew' ) 
		
		self.criminalname=tk.Label(self.criminallistframe  ,bg='red',fg='black',  anchor="center",font=("Georgia", 24 )  )
		self.criminalname.grid(row=1, column=0, padx=0, pady=3,  sticky='nsew' )
 
		
		self.emailsentimg = tk.Label(self.criminallistframe  )
		self.emailsentimg.grid(row=2, column=0  ,padx=0, pady=0) 

		#right>>output image
		self.rightimgframe = tk.Frame(self.ImgFrame, width=600, height=self.height-30, bg="pink")
		self.rightimgframe.grid(row=2, column=1, padx=0, pady=0)
		
		#Right.1: output heading:
		
		self.outputimgheadingFrame=tk.Frame(self.rightimgframe, width=600, height=50, bg='#f11212')
		self.outputimgheadingFrame.grid_propagate(0) 
		self.outputimgheadingFrame.grid(row=0, column=0, padx=0, pady=0 ,  sticky='nsew')
		self.outputimgheading=tk.Label(self.outputimgheadingFrame ,text='          IMAGE OUTPUT' ,bg='#f11212',fg='black' ,anchor="center" ,font=("Comic Sans MS", 25,'bold') )
		self.outputimgheading.grid(row=0, column=0, padx=0, pady=0,   sticky='nsew' ) 

		#Right.2 : output image
		self.outputimgframe=tk.Frame(self.rightimgframe, width=600, height=550, bg="#B6C4B6")
		self.outputimgframe.grid_propagate(0)
		self.outputimgframe.grid(row=1, column=0  ,padx=0, pady=0)
		
		self.outputimagelabel=tk.Label(self.rightimgframe  ,bg='#B6C4B6')
		self.outputimagelabel.grid(row=1, column=0 )
		
		self.outputimg = tk.Label(self.outputimgframe  )
		self.outputimg.grid(row=0, column=0  ,padx=0, pady=0) 
		#outputimage()

		 
		  
		
	"""
	
	"""
		 
	def open_file_dialog(self):
		self.inputimage.config(image="")
		self.outputimg.config(image="") 
		file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
		if file_path:
			# Do something with the selected file path (e.g., open or process the file)
			print(f"Selected file: {file_path}")
			self.display_image(file_path)
		
	def display_image(self,file_path):
		image = Image.open(file_path) 
		resized_image = image.resize((400, 300) )
		self.photox = ImageTk.PhotoImage(resized_image) 
		self.inputimage.config(image=self.photox)
		self.inputimagelabel.destroy()
		self.outputimagelabel.config(text="Processing.....")
		# call () to create outputimg folderand in that create a folder acc to timedate and we weill put output image in tis folder.
		 
		# call  processing() on source imgae  and store output img in above created folder
		folderpath=self.model.process(file_path)
		 
		#pass outimage path to below function.
		self.outputimage(folderpath )

		#place email label at topframe
		self.emailimglabel.config(  text = 'Email Sending')
		# call method to send email the output photo
		response= self.model.sendImgEmail(folderpath,self.toMail)
		if response.status_code == 200:
			result = response.json()
			if result["status"] == "success":
				messagebox.showinfo("Email Sent", "Email sent successfully!")
			else:
				messagebox.showerror("Error", "Failed to send email.")
		else:
			messagebox.showerror("Error", "Failed to connect to the server.")

		#remove email label at topframe
		self.emailimglabel.config(  text = '')

	def outputimage(self,folder_path):

		files = os.listdir(folder_path[0])
		for file_name in files:
			img_path = os.path.join(folder_path[0],file_name)
			image = Image.open(img_path) 
			resized_image = image.resize((600, 550) )
			self.photoxx = ImageTk.PhotoImage(resized_image) 
			self.outputimg.config(image=self.photoxx)
			self.outputimagelabel.destroy()
			
			self.criminalname.config(text= folder_path[1].title(), bg='#f4a603')


#.....................................................video methods..............................

	def vidbtn(self):
		# Hide the existing frames
		
		self.topframe.grid_forget()
		self.leftframe.grid_forget()
		self.rightframe.grid_forget()

		# Show the new frame
		self.VidFrame.grid(row=0, column=1 )	 
		self.aftervidbtnclick()
		
	def aftervidbtnclick(self):
		#topframe : backbtn, filebox , play video , email label
		self.cap = None
		self.topvidframe = tk.Frame(self.VidFrame, width=self.width, height=30, bg="gray")
		self.topvidframe.grid(row=0, column=0, padx=0, pady=0,columnspan=4, sticky='nsew') 	
		#back button
		self.backimg2 = tk.PhotoImage(file="back.png")
		self.backvid = tk.Button(self.topvidframe, image=self.backimg2, command=self.backToMainWindow2 ).grid( row=0, column=0 )

		self.fileopen2 = tk.Button(self.topvidframe, text="Open Video" ,command=self.open_file_dialog2).grid( row=0, column=1  ,padx=5 ,sticky="e")
		
		
 
		self.sendemail= tk.Button(self.topvidframe, text="Send Email" ,command=self.sendVidEmail).grid( row=0, column=3  ,padx=5 ,sticky="e")

		self.emailvidlabel=tk.Label(self.topvidframe  ,bg='gray')
		self.emailvidlabel.grid(row=0, column=3,padx=5 ,sticky="e" )

		


		#space:
		self.spacevidframe = tk.Frame(self.VidFrame, width=1000, height=5, bg="blue").grid(row=1, column=0, padx=0, pady=0,columnspan=4, sticky='nsew')


		#left:videoframe
		self.leftvidframe = tk.Frame(self.VidFrame, width=800, height=self.height-30, bg="black")
		self.leftvidframe.grid_propagate(0)
		self.leftvidframe.grid(row=2, column=0, padx=0, pady=0)

		self.videolabel=tk.Label(self.leftvidframe    )
		self.videolabel.grid(row=0, column=0, padx=0, pady=0 ,  sticky='nsew')


		#right:criminals detected list
		self.criminallistframe2 = tk.Frame(self.VidFrame, width=200, height=self.height-30, bg="red")
		self.criminallistframe2.grid_propagate(0)
		self.criminallistframe2.grid(row=2, column=1, padx=0, pady=0 ,  sticky='nsew')
		
		self.criminalnameHeading2=tk.Label(self.criminallistframe2 ,text='   ' ,bg='pink',fg='red'  ,font=("Comic Sans MS", 15,'bold') )
		self.criminalnameHeading2.grid(row=0, column=0, padx=0, pady=2,   sticky='nsew' ) 
		self.cl2=[]
		self.count =1
		
 
	def open_file_dialog2(self):
		
		file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])

		if file_path:
			self.master = tk.Toplevel(self.root)
			self.master.title("VIDEO Window")
			
			width = 1000
			height = 650
			self.width = 1000
			self.height = 650

			# Calculate the screen width and height
			screen_width = self.root.winfo_screenwidth()
			screen_height = self.root.winfo_screenheight()

			# Calculate the x and y coordinates for the Tkinter window to be centered
			x = (screen_width - width) // 2
			y = (screen_height - height) // 2
	 

			# Set the geometry of the window
	 
			self.master.geometry(f"{width}x{height}+{x}+{y}")

			self.dlsit2=[]
			self.folder2=self.createVideoFolder()
			# Add widgets or content to the new window
			 
			self.video_source = file_path
			self.cap = None  # Initialize cap as None

			self.label = tk.Label(self.master,bg="black")
			self.label.grid(row=0, column=0, columnspan=2,sticky='nsew' )
			
			self.master.columnconfigure(0, weight=1)
			self.master.rowconfigure(0, weight=1)

			self.btn_start = tk.Button(self.master, text="Open Video", command=self.start_camera2)
			self.btn_start.grid(row=1, column=0, pady=10)

			self.btn_stop = tk.Button(self.master, text="Close Camera", command=self.stop_camera2, state=tk.DISABLED)
			self.btn_stop.grid(row=1, column=1, pady=10)

			self.MyFaceNet = FaceNet()
			self.database = self.load_database2()
			
			self.update_id = None  # To store the update function id

			self.master.protocol("WM_DELETE_WINDOW", self.on_close2)		

#.............................
	def load_database2(self):
		with open("datafinal3.pkl", "rb") as myfile:
			database = pickle.load(myfile)
		return database
	
	def start_camera2(self):
		self.btn_start.config(state=tk.DISABLED)
		self.btn_stop.config(state=tk.NORMAL)
		self.cap = cv2.VideoCapture(self.video_source)
		self.update2()  # Start updating the frames
		
		 
		
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
	def stop_camera2(self):
		self.btn_start.config(state=tk.NORMAL)
		self.btn_stop.config(state=tk.DISABLED)
		if self.cap is not None and self.cap.isOpened():
		    self.cap.release()
		    self.cap = None
		    if self.update_id is not None:
		        self.master.after_cancel(self.update_id)
	
	def update2(self):
		if self.cap is not None and self.cap.isOpened():
			ret, frame = self.cap.read()
			if ret:
				# Perform face recognition
				frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				faces = self.detect_faces2(frame_rgb)

				for (x1, y1, w, h) in faces:
					x1, y1 = abs(x1), abs(y1)
					x2, y2 = x1 + w, y1 + h
					face_img = frame_rgb[y1:y2, x1:x2]

					face_img = Image.fromarray(face_img)
					face_img = face_img.resize((160, 160))
					face_array = np.asarray(face_img)

					face_array = np.expand_dims(face_array, axis=0)
					signature = self.MyFaceNet.embeddings(face_array)

					min_dist = 100
					identity = ' '
					for key, value in self.database.items():
						dist = np.linalg.norm(value - signature)
						if dist < min_dist:
							min_dist = dist
							identity = key

					if identity.lower() != 'unknown'  :
						cv2.putText(frame, identity.title(), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
						cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
						if identity.lower() not in self.dlsit2:
							self.dlsit2.append(identity.lower())
							cv2.imwrite(os.path.join(self.folder2, f'criminal is {identity.title()}.jpg'), frame)

				# Update the GUI with the frame
				photo = self.convert_frame_to_photo2(frame)
				self.label.config(image=photo)
				self.label.image = photo

				self.update_id = self.master.after(10, self.update2)
			else:
				self.stop_camera2()

	def detect_faces2(self, frame):
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=4)
		return faces

	def convert_frame_to_photo2(self, frame):
		frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
		return photo

	def on_close2(self):
		self.stop_camera2()
		self.master.destroy()
		
		print(self.dlsit2)
		print(self.folder2)
	
	def updateclist2(self ):
		 
		for name in self.dlsit2 :
			if name.lower() not in self.dlsit2  and name.lower() !='unknown':
				self.criminalname2=tk.Label(self.criminallistframe2  ,bg='red',fg='black', text=name, anchor="center",font=("Georgia", 12,'bold' )  )
				self.criminalname2.grid(row=self.count, column=0, padx=0, pady=3,  sticky='nsew' )
				self.count +=1
				self.cl2.append(	name.lower())

	def sendVidEmail(self ):
	
		data = {
			"to_email": self.toMail,
			"subject": "Criminal Detection From Video File",
			"body": "",
			"dirlist":self.folder2
		}
		response = requests.post("http://localhost:5000/send_email", data=data )
		 
		if response.status_code == 200:
			result = response.json()
			if result["status"] == "success":
				messagebox.showinfo("Email Sent", "Email sent successfully!")
			else:
				messagebox.showerror("Error", "Failed to send email.")
		else:
			messagebox.showerror("Error", "Failed to connect to the server.")

		#remove email label at topframe
		 

 	
#.............................

	def update_frame(self, frame):
        # Convert the frame from BGR to RGB
		frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# Convert the frame to a PhotoImage object
		img = Image.fromarray(frame_rgb)
		imgtk = ImageTk.PhotoImage(image=img)

		# Update the label with the new frame
		self.videolabel.imgtk = imgtk
		self.videolabel.config(image=imgtk)
	 
	def play_video(self):
		if self.cap is not None and self.cap.isOpened():
			while True:
				# Read a frame from the video capture
				ret, frame = self.cap.read()

				if not ret:
				    # End of video
				    break
				frameoutput =self.model.videoprocess(frame)
				# Resize the frame to match label dimensions
				frame = cv2.resize(frameoutput[0], (self.leftvidframe.winfo_width(), self.leftvidframe.winfo_height()))
				 
				for name in frameoutput[1]:
					if name.lower() not in self.cl2 and name.lower() !='unknown':
						self.criminalname2=tk.Label(self.criminallistframe2  ,bg='red',fg='black', text=name, anchor="center",font=("Georgia", 12,'bold' )  )
						self.criminalname2.grid(row=self.count, column=0, padx=0, pady=3,  sticky='nsew' )
						self.count +=1
						self.cl2.append(	name.lower())
					
				#add criminal list
				
				# Update the label with the current frame
				self.update_frame(frame)

 

			# Release the video capture object
			self.cap.release()

			# Clear the label to show an empty space
			self.videolabel.config(image=None)

			
			#send email
			#place email label at topframe
			self.emailvidlabel.config(  text = 'Email Sending')
			# call method to send email the output photo
			response= self.model.sendVidEmail(frameoutput[2],self.toMail)
			if response.status_code == 200:
				result = response.json()
				if result["status"] == "success":
					messagebox.showinfo("Email Sent", "Email sent successfully!")
				else:
					messagebox.showerror("Error", "Failed to send email.")
			else:
				messagebox.showerror("Error", "Failed to connect to the server.")

			#remove email label at topframe
			self.emailimglabel.config(  text = '')
#.....................................................web cam methods..............................

	
	def cambtn(self):
		# Hide the existing frames
		self.topframe.grid_forget()
		self.leftframe.grid_forget()
		self.rightframe.grid_forget()
		
		# Show the new frame
		self.CamFrame.grid(row=0, column=1 )	 
		self.aftercambtnclick()

	def	aftercambtnclick(self):
		#topframe : backbtn, opencam , closecam , email label
		self.topcamframe = tk.Frame(self.CamFrame, width=self.width, height=30, bg="gray")
		self.topcamframe.grid(row=0, column=0, padx=0, pady=0,columnspan=4, sticky='nsew')
		#..........................
		
		self.dlsit2=[]
		self.folder2=self.createVideoFolder()
		# Add widgets or content to the new window
		
		self.MyFaceNet = FaceNet()
		self.database = self.load_database3()
		
		
		#..............................

		self.backimg3 = tk.PhotoImage(file="back.png")
		self.backcam = tk.Button(self.topcamframe, image=self.backimg3, command=self.backToMainWindow3 ).grid( row=0, column=0     )

		#opencam button
		 
		self.opencam = tk.Button(self.topcamframe,text="Open WebCam",    command=self.opencam ).grid( row=0, column=1 ,padx=5 ,sticky="e")

		self.closecam = tk.Button(self.topcamframe, text="Close WebCam" ,command=self.close_camera).grid( row=0, column=2  ,padx=5 ,sticky="e")

		self.sendemail = tk.Button(self.topcamframe, text="Send Email" ,command=self.sendCamEmail).grid( row=0, column=3  ,padx=15 ,sticky="e") 

		self.emailcamlabel=tk.Label(self.topcamframe  ,bg='gray')
		self.emailcamlabel.grid(row=0, column=4,padx=5 ,sticky="e" )


		#left:videoframe
		self.leftcamframe = tk.Frame(self.CamFrame, width=800, height=self.height-30 )
		self.leftcamframe.grid_propagate(0)
		self.leftcamframe.grid(row=1, column=0, padx=0, pady=0,bg='black')

		self.camfeed = tk.Label(self.leftcamframe )  # Set the background color for the label
		self.camfeed.grid(row=0, column=0, columnspan=2, padx=2, pady=2)


		#right:criminals detected list
		self.criminallistframe3 = tk.Frame(self.CamFrame, width=200, height=self.height-30)
		self.criminallistframe3.grid_propagate(0)
		self.criminallistframe3.grid(row=1, column=1, padx=0, pady=0 ,  sticky='nsew')

		self.criminalnameHeading3=tk.Label(self.criminallistframe3 , bg='black',fg='red'  ,font=("Comic Sans MS", 15,'bold') )
		self.criminalnameHeading3.grid(row=0, column=0, padx=0, pady=2,   sticky='nsew' ) 


		self.cl3=[]
		self.count3 =1


#...............................................................................................................
	def opencam(self):
		self.master2 = tk.Toplevel(self.root)
		self.master2.title("WEBCAM Window") 
		 
		self.video_source = 0
		self.cap = None  # Initialize cap as None

		self.label = tk.Label(self.master2)
		self.label.grid(row=0, column=0, columnspan=2)

		self.btn_start = tk.Button(self.master2, text="Open Camera", command=self.start_camera3)
		self.btn_start.grid(row=1, column=0, pady=10)

		self.btn_stop = tk.Button(self.master2, text="Close Camera", command=self.stop_camera3, state=tk.DISABLED)
		self.btn_stop.grid(row=1, column=1, pady=10)
		self.update_id = None  # To store the update function id

		self.master2.protocol("WM_DELETE_WINDOW", self.on_close3)
		
	def load_database3(self):
		with open("datafinal3.pkl", "rb") as myfile:
			database = pickle.load(myfile)
		return database
	
	def start_camera3(self):
		self.btn_start.config(state=tk.DISABLED)
		self.btn_stop.config(state=tk.NORMAL)
		self.cap = cv2.VideoCapture(self.video_source)
		self.update3()  # Start updating the frames
		
		 
		
	def createVideoFolder(self): 
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
	def stop_camera3(self):
		self.btn_start.config(state=tk.NORMAL)
		self.btn_stop.config(state=tk.DISABLED)
		if self.cap is not None and self.cap.isOpened():
		    self.cap.release()
		    self.cap = None
		    if self.update_id is not None:
		        self.master2.after_cancel(self.update_id)
	
	def update3(self):
		if self.cap is not None and self.cap.isOpened():
			ret, frame = self.cap.read()
			if ret:
				# Perform face recognition
				frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				faces = self.detect_faces3(frame_rgb)

				for (x1, y1, w, h) in faces:
					x1, y1 = abs(x1), abs(y1)
					x2, y2 = x1 + w, y1 + h
					face_img = frame_rgb[y1:y2, x1:x2]

					face_img = Image.fromarray(face_img)
					face_img = face_img.resize((160, 160))
					face_array = np.asarray(face_img)

					face_array = np.expand_dims(face_array, axis=0)
					signature = self.MyFaceNet.embeddings(face_array)

					min_dist = 100
					identity = ' '
					for key, value in self.database.items():
						dist = np.linalg.norm(value - signature)
						if dist < min_dist:
							min_dist = dist
							identity = key

					 
					cv2.putText(frame, identity.title(), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
					cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
					if identity.lower() not in self.dlsit2:
						self.dlsit2.append(identity.lower())
					cv2.imwrite(os.path.join(self.folder2, f'criminal is {identity.title()}.jpg'), frame)

				# Update the GUI with the frame
				photo = self.convert_frame_to_photo3(frame)
				self.label.config(image=photo)
				self.label.image = photo

				self.update_id = self.master2.after(10, self.update3)
			else:
				self.stop_camera3()

	def detect_faces3(self, frame):
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=4)
		return faces

	def convert_frame_to_photo3(self, frame):
		frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
		return photo

	def on_close3(self):
		self.stop_camera3()
		self.master2.destroy()
		
		print(self.dlsit2)
		print(self.folder2)
	
	def updateclist2(self ):
		 
		for name in self.dlsit2 :
			if name.lower() not in self.dlsit2  and name.lower() !='unknown':
				self.criminalname2=tk.Label(self.criminallistframe2  ,bg='red',fg='black', text=name, anchor="center",font=("Georgia", 12,'bold' )  )
				self.criminalname2.grid(row=self.count, column=0, padx=0, pady=3,  sticky='nsew' )
				self.count +=1
				self.cl2.append(	name.lower())

	def sendCamEmail(self ):
	
		data = {
			"to_email": self.toMail,
			"subject": "Criminal Detection From WEBCAM File",
			"body": "",
			"dirlist":self.folder2
		}
		response = requests.post("http://localhost:5000/send_email", data=data )
		 
		if response.status_code == 200:
			result = response.json()
			if result["status"] == "success":
				messagebox.showinfo("Email Sent", "Email sent successfully!")
			else:
				messagebox.showerror("Error", "Failed to send email.")
		else:
			messagebox.showerror("Error", "Failed to connect to the server.")

		#remove email label at topframe
		 

#.................................................................................................................
	def open_camera(self):
		# Disable the "Open Camera" button and enable the "Close Camera" button
		 
		try:
		# Open the webcam with the specified width and height
			self.cam = cv2.VideoCapture(0)
			if not self.cam.isOpened():
				print("Error: Could not open camera.")
				return
			self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.leftcamframe.winfo_width())
			self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.leftcamframe.winfo_height())

			# Start a thread to continuously capture frames
			self.update()
		except Exception as e:
			print(f"Error opening camera: {e}")

	def close_camera(self   ):
		# Release the camera
		dirlist=self.model.getfoldername()
		print(f'dirlist:{dirlist}')
		if self.cam is not None:
			self.cam.release()

		# Enable the "Open Camera" button and disable the "Close Camera" button
		 
		self.camfeed.configure(image=None, text="Camera Closed", compound=tk.CENTER)


		self.emailcamlabel.config(  text = ' email sending...')
		self.model.sendCamEmail( dirlist,self.toMail)
		if response.status_code == 200:
			result = response.json()
			if result["status"] == "success":
				messagebox.showinfo("Email Sent", "Email sent successfully!")
			else:
				messagebox.showerror("Error", "Failed to send email.")
		else:
			messagebox.showerror("Error", "Failed to connect to the server.")

		#remove email label at topframe
		self.emailcamlabel.config(  text = '')


	def update(self):
		print("Update method called")
		ret, frame = self.cam.read()
		self.camoutput=None
		if ret:
			
			self.camoutput=self.model.webcamprocess(frame)
			# Convert the OpenCV BGR image to RGB
			rgb_image = cv2.cvtColor(self.camoutput[0], cv2.COLOR_BGR2RGB)
			
			rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
			# Resize the image to fit the canvas dimensions
			rgb_image = cv2.resize(rgb_image, (self.leftcamframe.winfo_width(), self.leftcamframe.winfo_height()))

			# Convert the image to a PhotoImage
			img = ImageTk.PhotoImage(image=Image.fromarray(rgb_image))

			# Update the canvas with the new image
			self.camfeed.configure(image=img, text="")
			self.camfeed.img = img

			for name in self.camoutput[1]:
				if name.lower() not in self.cl3 and name.lower() !='unknown':
					self.criminalname3=tk.Label(self.criminallistframe3  ,bg='red',fg='black', text=name, anchor="center",font=("Georgia", 12,'bold' )  )
					self.criminalname3.grid(row=self.count3, column=0, padx=0, pady=3,  sticky='nsew' )
					self.count3 +=1
					self.cl3.append(	name.lower())
				

			# Call the update method again after a delay
			self.leftcamframe.after(10, self.update)
		else:
			# Release the camera if there's an issue capturing frames
			print('updatae clsoe camera')
			print(self.camoutput[2] )
			self.close_camera( )
			

		

	def backToMainWindow1(self):
		#hide imgFrame		
		self.ImgFrame.grid_forget()
		self.root.config(bg= "black") 
		#show main page
		self.topframe.grid(row=0, column=0, padx=0, pady=5,columnspan=4, sticky='nsew')
		self.leftframe.grid(row=1, column=0, padx=0, pady=0)
		self.rightframe.grid(row=1, column=1, padx=0, pady=0) 
		self.inputimage.config(image="") # its optional since imageFrame content created/overwritten   when imgage button cliked on main window.
		
	def backToMainWindow2(self):
		self.VidFrame.grid_forget()
		  
		self.root.config(bg= "black")  
		self.topframe.grid(row=0, column=0, padx=0, pady=5,columnspan=4, sticky='nsew')
		self.leftframe.grid(row=1, column=0, padx=0, pady=0)
		self.rightframe.grid(row=1, column=1, padx=0, pady=0)

	def backToMainWindow3(self):
		self.CamFrame.grid_forget()
		 
		self.topframe.grid(row=0, column=0, padx=0, pady=5,columnspan=4, sticky='nsew')
		self.leftframe.grid(row=1, column=0, padx=0, pady=0)
		self.rightframe.grid(row=1, column=1, padx=0, pady=0)

	def animation(self):
		image = self.photoimage_objects[self.current_frame]
		self.background_label.configure(image=image, padx=0)

		self.current_frame += 1
		if self.current_frame == self.frames:
			self.current_frame = 0

		# Repeat the animation after a delay (e.g., 50 milliseconds)
		self.leftframe.after(60, self.animation)

	def hello_world(self):
		self.label.config(text="Hello, World!")
		self.label.config(bg="yellow")

	def close_window(self, event):
		if event.char.lower() == 'q':
			self.root.destroy()

	 

	def run(self):
		# Start the Tkinter event loop
		self.root.mainloop()

# Create an instance of the HelloWorldApp class and run the application
#name = input("enter name for window: ")
#app = MajorProject(name)
app = MajorProject( )
app.run()

