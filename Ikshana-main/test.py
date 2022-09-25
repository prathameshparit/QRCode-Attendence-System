# import qrcode
# import cv2
# from pyzbar.pyzbar import decode
# from pyzbar.pyzbar import ZBarSymbol
#
#
# img = cv2.imread("51_Daniel.jpg")
# decrypt = decode(img, symbols=[ZBarSymbol.QRCODE])
# # print(decrypt[0].rect)
# print(decrypt[0].polygon[1])
#
# def point_locator(decrypt):
#     top_left = (decrypt[0].rect.left, decrypt[0].rect.top)
#     top_right = (decrypt[0].rect.left + decrypt[0].rect.width, decrypt[0].rect.top)
#     bottom_left = (decrypt[0].rect.left, decrypt[0].rect.top + decrypt[0].rect.height)
#     bottom_right = (decrypt[0].rect.left + decrypt[0].rect.width, decrypt[0].rect.left + decrypt[0].rect.height)
#
#     return top_left, top_right, bottom_left, bottom_right
#
# def plot(img, r=5, len=34, th=4, clr = (0, 255, 0)):
#     top_left, top_right, bottom_left, bottom_right = point_locator(decrypt)
#
#     cv2.circle(img, top_left, radius=r, color=clr, thickness=-1)
#     img = cv2.line(img, top_left, (top_left[0], top_left[1] + len), color=clr, thickness=th)
#     img = cv2.line(img, top_left, (top_left[0] + len, top_left[1]), color=clr, thickness=th)
#
#     cv2.circle(img, top_right, radius=r, color=clr, thickness=-1)
#     img = cv2.line(img, top_right, (top_right[0], top_right[1] + len), color=clr, thickness=th)
#     img = cv2.line(img, top_right, (top_right[0] - len, top_right[1]), color=clr, thickness=th)
#
#     cv2.circle(img, bottom_left, radius=r, color=clr, thickness=-1)
#     img = cv2.line(img, bottom_left, (bottom_left[0], bottom_left[1] - len), color=clr, thickness=th)
#     img = cv2.line(img, bottom_left, (bottom_left[0] + len, bottom_left[1]), color=clr, thickness=th)
#
#     cv2.circle(img, bottom_right, radius=r, color=clr, thickness=-1)
#     img = cv2.line(img, bottom_right, (bottom_right[0], bottom_right[1] - len), color=clr, thickness=th)
#     img = cv2.line(img, bottom_right, (bottom_right[0] - len, bottom_right[1]), color=clr, thickness=th)
#
#     return img
#
# polygon_cords = decrypt[0].polygon
# def plot_polygon(img, polygon_cords, r=5, len=34, th=4, clr = (0, 255, 0)):
#     top_left, top_right, bottom_left, bottom_right = polygon_cords[0], polygon_cords[1], polygon_cords[2], polygon_cords[3]
#
#     cv2.circle(img, top_left, radius=r, color=clr, thickness=-1)
#     img = cv2.line(img, top_left, (top_left[0], top_left[1] + len), color=clr, thickness=th)
#     img = cv2.line(img, top_left, (top_left[0] + len, top_left[1]), color=clr, thickness=th)
#
#     cv2.circle(img, top_right, radius=r, color=clr, thickness=-1)
#     img = cv2.line(img, top_right, (top_right[0], top_right[1] - len), color=clr, thickness=th)
#     img = cv2.line(img, top_right, (top_right[0] + len, top_right[1]), color=clr, thickness=th)
#
#     cv2.circle(img, bottom_left, radius=r, color=clr, thickness=-1)
#     img = cv2.line(img, bottom_left, (bottom_left[0], bottom_left[1] - len), color=clr, thickness=th)
#     img = cv2.line(img, bottom_left, (bottom_left[0] - len, bottom_left[1]), color=clr, thickness=th)
#
#     cv2.circle(img, bottom_right, radius=r, color=clr, thickness=-1)
#     img = cv2.line(img, bottom_right, (bottom_right[0], bottom_right[1] + len), color=clr, thickness=th)
#     img = cv2.line(img, bottom_right, (bottom_right[0] - len, bottom_right[1]), color=clr, thickness=th)
#
#     return img
#
#
# while True:
#     img = plot_polygon(img, polygon_cords)
#
#     cv2.imshow("Window", img)
#
#     if cv2.waitKey(0) & 0xFF == ord("q"):
#         break
#

import cv2
from library import LIB
# gen = LIB('bookrecord.csv')

cap = cv2.VideoCapture(0)

while True:
    res, img = cap.read()

    cv2.imshow("Win", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
