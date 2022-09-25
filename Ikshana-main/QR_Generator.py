# Importing dependancies
import cv2
import qrcode
import datetime
import pandas as pd
from records import records
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

class QR_GEN():
    def __init__(self, names_csv):
        self.record = []
        self.qr_list = []
        self.names_csv = names_csv
        self.df = pd.read_csv(self.names_csv)

    def createQrCode(self, save=False):
        df = pd.read_csv(self.names_csv)

        for index, values in df.iterrows():
            name = values["Name"]
            roll = values["Roll"]

            data = f"{name} {roll}"
            self.record.append(data)

            image = qrcode.make(data)

            self.qr_list.append(f"{roll}_{name}.jpg")

            # Saving the codes to <QRs> directory
            if save:
                image.save(f"QRs/{roll}_{name}.jpg")
        return self.record

    def name_col_check(self):
        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y")

        self.df = pd.read_csv(self.names_csv)
        if date not in self.df.columns:
            self.df.insert(2, column=date, value="A")
            self.df.to_csv('output.csv', index=False)

        return date

    def qr_check_attendance(self, img):
        # date = self.name_col_check()
        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y")
        if date not in self.df.columns:
            self.df.insert(2, column=date, value="A")
            self.df.to_csv('attendance.csv', index=False)
        if decode(img, symbols=[ZBarSymbol.QRCODE]):
            for qr in decode(img, symbols=[ZBarSymbol.QRCODE]):
                myData = qr.data.decode('utf-8')

                scanedname, scanedroll = myData.split(" ")

                if myData in records:  # Check if the student is actually listed in records
                    print(f"Good morning, Your attendance has been marked {scanedname}")
                    # df = pd.read_csv('output.csv')

                    self.df = pd.read_csv('attendance.csv')

                    pos = self.df[self.df['Name'] == scanedname].index.values
                    self.df.loc[pos[0], date] = "P"
                    # print(self.df.loc[pos[0], date])

                    self.df.to_csv('attendance.csv', index=False)

    def qr_check_mid_day_meal(self, img):
        # date = self.name_col_check()
        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y")
        if date not in self.df.columns:
            self.df.insert(2, column=date, value="NA")
            self.df.to_csv('mid-day-meal.csv', index=False)
        if decode(img, symbols=[ZBarSymbol.QRCODE]):
            for qr in decode(img, symbols=[ZBarSymbol.QRCODE]):
                myData = qr.data.decode('utf-8')

                scanedname, scanedroll = myData.split(" ")

                if myData in records:  # Check if the student is actually listed in records
                    print(f"Hello, Your meal will been served {scanedname}")
                    # df = pd.read_csv('output.csv')

                    self.df = pd.read_csv('mid-day-meal.csv')

                    pos = self.df[self.df['Name'] == scanedname].index.values
                    self.df.loc[pos[0], date] = "Recieved"
                    # print(self.df.loc[pos[0], date])

                    self.df.to_csv('mid-day-meal.csv', index=False)


    def point_locator(self, decrypt):
        top_left = (decrypt[0].rect.left, decrypt[0].rect.top)
        top_right = (decrypt[0].rect.left + decrypt[0].rect.width, decrypt[0].rect.top)
        bottom_left = (decrypt[0].rect.left, decrypt[0].rect.top + decrypt[0].rect.height)
        bottom_right = (decrypt[0].rect.left + decrypt[0].rect.width, decrypt[0].rect.left + decrypt[0].rect.height)

        return top_left, top_right, bottom_left, bottom_right

    def plot(self, img, decrypt, r=5, len=34, th=4, clr=(0, 255, 0)):
        top_left, top_right, bottom_left, bottom_right = self.point_locator(decrypt)

        cv2.circle(img, top_left, radius=r, color=clr, thickness=-1)
        img = cv2.line(img, top_left, (top_left[0], top_left[1] + len), color=clr, thickness=th)
        img = cv2.line(img, top_left, (top_left[0] + len, top_left[1]), color=clr, thickness=th)

        cv2.circle(img, top_right, radius=r, color=clr, thickness=-1)
        img = cv2.line(img, top_right, (top_right[0], top_right[1] + len), color=clr, thickness=th)
        img = cv2.line(img, top_right, (top_right[0] - len, top_right[1]), color=clr, thickness=th)

        cv2.circle(img, bottom_left, radius=r, color=clr, thickness=-1)
        img = cv2.line(img, bottom_left, (bottom_left[0], bottom_left[1] - len), color=clr, thickness=th)
        img = cv2.line(img, bottom_left, (bottom_left[0] + len, bottom_left[1]), color=clr, thickness=th)

        cv2.circle(img, bottom_right, radius=r, color=clr, thickness=-1)
        img = cv2.line(img, bottom_right, (bottom_right[0], bottom_right[1] - len), color=clr, thickness=th)
        img = cv2.line(img, bottom_right, (bottom_right[0] - len, bottom_right[1]), color=clr, thickness=th)

        return img

    def plot_polygon(self, img, polygon_cords, r=5, len=34, th=4, clr=(0, 255, 0)):
        top_left, top_right, bottom_left, bottom_right = polygon_cords[0], polygon_cords[1], polygon_cords[2], \
                                                         polygon_cords[3]

        cv2.circle(img, top_left, radius=r, color=clr, thickness=-1)
        img = cv2.line(img, top_left, (top_left[0], top_left[1] + len), color=clr, thickness=th)
        img = cv2.line(img, top_left, (top_left[0] + len, top_left[1]), color=clr, thickness=th)

        cv2.circle(img, top_right, radius=r, color=clr, thickness=-1)
        img = cv2.line(img, top_right, (top_right[0], top_right[1] - len), color=clr, thickness=th)
        img = cv2.line(img, top_right, (top_right[0] + len, top_right[1]), color=clr, thickness=th)

        cv2.circle(img, bottom_left, radius=r, color=clr, thickness=-1)
        img = cv2.line(img, bottom_left, (bottom_left[0], bottom_left[1] - len), color=clr, thickness=th)
        img = cv2.line(img, bottom_left, (bottom_left[0] - len, bottom_left[1]), color=clr, thickness=th)

        cv2.circle(img, bottom_right, radius=r, color=clr, thickness=-1)
        img = cv2.line(img, bottom_right, (bottom_right[0], bottom_right[1] + len), color=clr, thickness=th)
        img = cv2.line(img, bottom_right, (bottom_right[0] - len, bottom_right[1]), color=clr, thickness=th)

        return img

def main():
    gen = QR_GEN("names.csv")
    url = "http://192.168.0.110:8080/video"
    # url = "http://192.168.43.22:8080/video"
    # url = "http://192.168.125.199:8080/video"

    cap = cv2.VideoCapture(url)
    while True:
        res, img = cap.read()
        img = cv2.resize(img, (640, 480))
        gen.qr_check_mid_day_meal(img)

        decrypt = decode(img, symbols=[ZBarSymbol.QRCODE])
        if decrypt:
            polygon_cords = decrypt[0].polygon
            img = gen.plot_polygon(img, polygon_cords)

        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

if __name__ == "__main__":
    main()
