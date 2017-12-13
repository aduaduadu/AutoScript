# -*- coding:utf-8 -*-
"""ScreenCapture."""


import win32gui
import win32ui
import win32con
import win32api
import numpy as np
import imutils
import cv2


def allScreenCapture():
    # 截屏并持续缩放显示。有点慢，估计不做缩放，会快上一点点。。
    wDC = win32gui.GetWindowDC(0)
    scrDC = win32ui.CreateDCFromHandle(wDC)
    scrList = []
    moniters = win32api.EnumDisplayMonitors(None, None)
    for m in moniters:
        cDC = scrDC.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        x, y, w, h = m[2][0], m[2][1], m[2][2] - m[2][0], m[2][3] - m[2][1]
        dataBitMap.CreateCompatibleBitmap(scrDC, w, h)
        cDC.SelectObject(dataBitMap)
        scrList.append((m, cDC, dataBitMap))
    while True:
        for m, cDC, dataBitMap in scrList:
            x, y, w, h = m[2][0], m[2][1], m[2][2] - m[2][0], m[2][3] - m[2][1]
            cDC.BitBlt((0, 0), (w, h), scrDC, (x, y), win32con.SRCCOPY)
            im = dataBitMap.GetBitmapBits(False)
            frame = np.array(im).astype(dtype="uint8")
            frame.shape = (h, w, 4)
            img = imutils.resize(frame, width=800)
            cv2.imshow("Screen-%d" % m[0].handle, img)
        key = cv2.waitKey(1)
        # 如果按下q键，跳出循环
        if key == ord("q"): break
    for m, cDC, dataBitMap in scrList:
        cDC.DeleteDC()
        win32gui.DeleteObject(dataBitMap.GetHandle())
    scrDC.DeleteDC()
    win32gui.ReleaseDC(0, wDC)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    allScreenCapture()
