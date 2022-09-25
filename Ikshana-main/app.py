import cv2
import csv
import time
import numpy as np
import pandas as pd
from QR_Generator import QR_GEN, ZBarSymbol
from flask import Flask, render_template, Response, request
import datetime
import pyzbar as pyzbar
from pyzbar.pyzbar import decode


app = Flask(__name__)

def FPS(img, fps, latency):
	cv2.putText(img, f"FPS: {str(int(fps))}", org=(7, 25), fontFace=cv2.FONT_HERSHEY_PLAIN,
				fontScale=1, color=(0, 0, 0), thickness=1)

	cv2.putText(img, f"Latency: {str(latency)}s", org=(97, 25), fontFace=cv2.FONT_HERSHEY_PLAIN,
				fontScale=1, color=(0, 0, 0), thickness=1)

	return img

def gen_frames_attendance():
	pTime, pTimeL = 0, 0
	previous = time.time()
	delta = 0
	message = ""
	a = 0

	gen = QR_GEN("names.csv")
	url = "http://192.168.0.110:8080/video"

	cap = cv2.VideoCapture(0)
	cap.set(10, 150)

	while True:
		_, img = cap.read()
		# img = cv2.flip(img, 1)

		img = cv2.resize(img, (640, 480))
		gen.qr_check_attendance(img)

		decrypt = decode(img, symbols=[ZBarSymbol.QRCODE])
		if decrypt:
			polygon_cords = decrypt[0].polygon
			img = gen.plot_polygon(img, polygon_cords)

		# # FPS
		cTimeL = time.time()

		cTime = time.time()
		if (cTime - pTime) != 0:
			fps = 1 / (cTime - pTime)
			latency = np.round((cTimeL - pTimeL), 4)
			pTime, pTimeL = cTime, cTimeL
			a += 1

			img = FPS(img, fps, latency)

		# Video stream
		ret, buffer = cv2.imencode('.jpg', img)
		img = buffer.tobytes()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

def gen_frames_mid_day_meal():
	pTime, pTimeL = 0, 0
	previous = time.time()
	delta = 0
	message = ""
	a = 0

	gen = QR_GEN("names.csv")
	url = "http://192.168.0.110:8080/video"

	cap = cv2.VideoCapture(0)
	cap.set(10, 150)

	while True:
		_, img = cap.read()
		# img = cv2.flip(img, 1)

		img = cv2.resize(img, (640, 480))
		gen.qr_check_mid_day_meal(img)

		decrypt = decode(img, symbols=[ZBarSymbol.QRCODE])
		if decrypt:
			polygon_cords = decrypt[0].polygon
			img = gen.plot_polygon(img, polygon_cords)

		# # FPS
		cTimeL = time.time()

		cTime = time.time()
		if (cTime - pTime) != 0:
			fps = 1 / (cTime - pTime)
			latency = np.round((cTimeL - pTimeL), 4)
			pTime, pTimeL = cTime, cTimeL
			a += 1

			img = FPS(img, fps, latency)

		# Video stream
		ret, buffer = cv2.imencode('.jpg', img)
		img = buffer.tobytes()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')


def change_type(sub):
	"""
	Makes each element of list or array change to string
	:param sub: list or any array
	:return: string type of all elements
	"""

	if isinstance(sub, list):
		return [change_type(ele) for ele in sub]
	elif isinstance(sub, tuple):
		return tuple(change_type(ele) for ele in sub)
	else:
		return str(sub)




def gen_frames_library():
	df = pd.read_csv('bookrecord.csv')

	# Constants:
	record = df["ISBN"].to_list()
	stored = []
	count = 0
	realtimeuser = []
	flag = 0
	flag2 = 0

	pTime, pTimeL = 0, 0
	previous = time.time()
	delta = 0
	message = ""
	a = 0

	url = "http://192.168.0.110:8080/video"

	cap = cv2.VideoCapture(0)
	cap.set(10, 150)

	while True:
		_, img = cap.read()
		# img = cv2.flip(img, 1)

		img = cv2.resize(img, (640, 480))

		# Scanning data in continous loop and Frame by Frame it scans the code
		decodedObjects = pyzbar.pyzbar.decode(img)

		# Processing the decoded image
		for obj in decodedObjects:

			print('Type : ', obj.type)
			mydata = obj.data.decode('utf-8')

			# Using QRcode for the user's name and roll no.
			if obj.type == "QRCODE":
				qr = obj.data.decode('utf-8')
				print('Data : ', qr, '\n')

				scanned_name, scanned_roll = qr.split(" ")

				# Checking who the realtimeuser is!... even if new user has logged in.... the existing session terminates
				if flag == 1:
					realtimeuser = []

				if qr not in realtimeuser:
					realtimeuser.append(qr)

				if obj.type == "QRCODE" and realtimeuser[0] == qr:
					flag = 0
					print(f"{scanned_name} please provide the ISBN of the book")
				print(realtimeuser[0])

				if obj.type == "QRCODE" and realtimeuser[0] != qr:
					flag = 1
					count = 0
					print(f"New Session Started hello {scanned_name}")


			# Using barcode for storing, extracting, processing book info
			elif obj.type == "EAN13":
				barcode = obj.data.decode('utf-8')
				barcode = int(barcode)
				print('Data : ', barcode, '\n')

			df = pd.read_csv('bookrecord.csv')

			if obj.type == "EAN13":
				# Adding the book name by entering the name as input if ISBN code not found in "bookrecord.csv"
				if barcode not in record:
					name = input("Enter Book Name: ")
					df = pd.DataFrame({'ISBN': [barcode],
									   'Book': [name]})
					record.append(barcode)
					df.to_csv('bookrecord.csv', mode='a', index=False, header=False)
					print("Done")

				# If ISBN record found then book is been borrow or returned on user's data
				else:
					df = pd.read_csv('librec.csv')

					# List1 is the list of all values of librec.csv in a list
					list1 = df.values.tolist()
					list1 = change_type(list1)

					df = pd.read_csv('bookrecord.csv')

					issue_date = datetime.datetime.now()
					issue_date = issue_date.strftime("%d-%m-%Y")

					new_date = datetime.datetime.now()
					issue_time = new_date.strftime("%H:%M")

					# Finding book name by check the ISBN code and searching code through "bookrecord.csv"
					index = record.index(barcode)
					book_name = df["Book"].iloc[index]

					# Making a dataframe of Realtimeuser detail's to then append it to library record
					rt_df = pd.DataFrame({'Name': [scanned_name],  # rt_df = realtime dataframe
										  'Roll': [scanned_roll],
										  'Book': [book_name],
										  'ISBN': [barcode],
										  'Idate': [issue_date],
										  'Itime': [issue_time],
										  'Rdate': "Null",
										  'Rtime': "Null"})

					# To check if the user has changed and brought another book to borrow
					realtimecode = [barcode]
					stored.append(barcode)
					count += 1
					if realtimecode[0] != stored[0]:
						count = 1
						stored[0] = realtimecode[0]

					# List2 is the list of all values of current user detail (i.e rt_df) in a list
					list2 = rt_df.values.tolist()
					list2 = change_type(list2)

					df = pd.read_csv('librec.csv')

					# Checking if user is returning the book
					for i in range(len(list1)):
						flag2 = 0
						if list1[i][0] == list2[0][0] and list1[i][1] == list2[0][1] and list1[i][2] == list2[0][2] and \
								list1[i][3] == list2[0][3]:
							if list1[i][5] != issue_time:
								if list1[i][6] == "Null" and list1[i][7] == "Null":
									print("Returned")
									df.iloc[i, df.columns.get_loc('Rdate')] = issue_date
									df.iloc[i, df.columns.get_loc('Rtime')] = issue_time
									df.to_csv('librec.csv', index=False)
									flag2 = 1
									break

					# If not returning append the data to library record
					if count == 1 and flag2 == 0:
						rt_df.to_csv('librec.csv', mode='a', header=False, index=False)

					print("DONE Donea done")



		# # FPS
		cTimeL = time.time()

		cTime = time.time()
		if (cTime - pTime) != 0:
			fps = 1 / (cTime - pTime)
			latency = np.round((cTimeL - pTimeL), 4)
			pTime, pTimeL = cTime, cTimeL
			a += 1

			img = FPS(img, fps, latency)

		# Video stream
		ret, buffer = cv2.imencode('.jpg', img)
		img = buffer.tobytes()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/attendance')
def attendance():
	return render_template('attendance.html')

@app.route('/mid-day-meal')
def midDayMeal():
	return render_template('mid-day-meal.html')

@app.route('/library')
def library():
	return render_template('library.html')



@app.route('/data_attendance', methods=['GET', 'POST'])
def data_attendance():
	f = "attendance.csv"
	data = []
	with open(f) as file:
		csvfile = csv.reader(file)
		for row in csvfile:
			data.append(row)

	data = pd.DataFrame(data)
	return render_template('data.html', data=data.to_html(classes='mystyle', header=False, index=False))

@app.route('/data_mid_day_meal', methods=['GET', 'POST'])
def data_mid_day_meal():
	f = "mid-day-meal.csv"
	data = []
	with open(f) as file:
		csvfile = csv.reader(file)
		for row in csvfile:
			data.append(row)

	data = pd.DataFrame(data)
	return render_template('data.html', data=data.to_html(classes='mystyle', header=False, index=False))

@app.route('/data_library', methods=['GET', 'POST'])
def data_library():
	f = "librec.csv"
	data = []
	with open(f) as file:
		csvfile = csv.reader(file)
		for row in csvfile:
			data.append(row)

	data = pd.DataFrame(data)
	return render_template('data.html', data=data.to_html(classes='mystyle', header=False, index=False))




@app.route('/video_feed_attendance')
def video_feed():
	return Response(gen_frames_attendance(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_mid_day_meal')
def video_feed_mid_day_meal():
	return Response(gen_frames_mid_day_meal(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_library')
def video_feed_library():
	return Response(gen_frames_library(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	app.run(debug=True)