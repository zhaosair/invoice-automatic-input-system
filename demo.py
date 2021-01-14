# -*- coding:utf-8 -*-
import os
import ocr
import time
import shutil
import cv2
import numpy as np
from PIL import Image
from glob import glob
image_files = glob('./test_images/*.*')
import pdfkit
import sys
from vector import Vector
from table import *
from math import *
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

AllLine = []


def getLine(img, x, y, vector, Line):
    if img[x][y] == 255:
        img[x][y] = 0
        prev_x = Line[-1][0]
        prev_y = Line[-1][1]
        LastPoint = Vector((prev_x, prev_y))
        v = Vector((x, y)).minus(LastPoint)
        if v.parallelism(vector):
            Line[-1] = (x, y)
        else:
            if (abs(x - prev_x) <= 1) & (abs(y - prev_y) <= 1):
                Line.append((x, y))
            else:
                Line = [(x, y)]
        if not (getLine(img, x, y+1, v, Line) & getLine(img, x+1, y, v, Line)): # & getLine(img, x+1, y+1, v, Line)):
            if AllLine.count(Line) == 0:
                AllLine.append(Line)
        return True
    else:
        return False
    # if node.count(Point):
    #     print("nodePoint:", Point)
    #     return Point
    # elif img[startPoint[0]][startPoint[1]] == 255:
    #     img[startPoint[0]][startPoint[1]] = 200
    #     return getLine(img, (Point[0], Point[1] + 1)) + getLine(img, (Point[0] + 1, Point[1]))  \
    #         + getLine(img, (Point[0] + 1, Point[1] + 1))
    # else:
    #     return ()


if __name__ == '__main__':
    result_dir = './test_result'
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)

    for image_file in sorted(image_files):
        AllLine = []
        image = np.array(Image.open(image_file).convert('RGB'))
        t = time.time()
        result, image_framed, boxes, scale = ocr.model(image)
        output_file = os.path.join(result_dir, image_file.split('/')[-1])
        Image.fromarray(image_framed).save(output_file)
        img = cv2.resize(image, None, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Mission complete, it took {:.3f}s".format(time.time() - t))
        print("\nRecognition Result:\n")

        for box in boxes:
            for i in range(box[1], box[5]):
                for j in range(box[0], box[2]):
                    img[i][j] = 255
        img = cv2.resize(img, None, None, fx=1.0 / scale, fy=1.0 / scale, interpolation=cv2.INTER_LINEAR)
        img = cv2.resize(img, None, None, fx=1.0 / 2, fy=1.0 / 2, interpolation=cv2.INTER_LINEAR)
        img = cv2.resize(img, None, None, fx=1.0 / 2, fy=1.0 / 2, interpolation=cv2.INTER_LINEAR)
        Image.fromarray(img).save('image1.tif')
        minPoint = [1500, 1500]
        maxPoint = [0, 0]
        Point = []
        count = 0
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                if img[i][j] < 230:
                    img[i][j] = 255
                    Point.append((i, j))
                    if count == 0:
                        minPoint[0] = i
                        minPoint[1] = j
                        count = 1
                    maxPoint[0] = i
                    maxPoint[1] = j
                else:
                    img[i][j] = 0
        # node = []
        # horizontal = []
        # vertical = []
        # for i in range(0, len(Point)):
        #     if Point.count((Point[i][0], Point[i][1] - 1)) | Point.count((Point[i][0], Point[i][1] + 1)):
        #         horizontal.append(Point[i])
        #     if Point.count((Point[i][0] - 1, Point[i][1])) | Point.count((Point[i][0] + 1, Point[i][1])):
        #         vertical.append(Point[i])
        # for i in range(0, len(horizontal)):
        #     if vertical.count(horizontal[i]):
        #         node.append(horizontal[i])

        # for i in range(0, img.shape[0]):
        #     for j in range(0, img.shape[1]):
        #         if node.count((i, j)) == 0:
        #             img[i][j] = 0
        Image.fromarray(img).save('image.tif')
        #  获取直线
        startPoint = minPoint
        vector = Vector((startPoint[0], startPoint[1]))
        Line = [(startPoint[0], startPoint[1])]
        getLine(img, startPoint[0], startPoint[1] + 1, vector, Line)
        getLine(img, startPoint[0] + 1, startPoint[1], vector, Line)
        # getLine(img, startPoint[0] + 1, startPoint[1] + 1, vector, Line)

        row = []
        col = []
        for L in AllLine:
            if row.count(ceil(L[1][0]*4*scale)) == 0:
                row.append(ceil(L[1][0]*4*scale))
            if col.count(ceil(L[1][1]*4*scale)) == 0:
                col.append(ceil(L[1][1]*4*scale))
        row = sorted(row)
        col = sorted(col)
        data = []
        for i in range(len(row) - 1):
            a = []
            for j in range(len(col) - 1):
                a.append(' ')
            data.append(a)
        print("文本识别结果")
        for key in result:
            x = 0
            y = 0
            for i in range(len(row)):
                if boxes[key][1] < row[i]:
                    if (row[i] - boxes[key][1]) >= (boxes[key][5] - row[i]):
                        x = i - 1
                        break
                    else:
                        x = i
                        break
            for j in range(len(col)):
                if boxes[key][0] < col[j]:
                    if (col[j] - boxes[key][0]) >= (boxes[key][2] - col[j]):
                        y = j - 1
                        break
                    else:
                        y = j
                        break
            data[x][y] = result[key][1]
            print(result[key][1])
        Style = getSampleStyleSheet()
        n = Style['Normal']
        z = table_model(data)
        save_file = image_file.split('/')[-1].split('.')[0] + '.pdf'
        pdf = SimpleDocTemplate(save_file)
        pdf.multiBuild([Paragraph(' ', n), z])
        print("文本检测框位置信息")
        for box in boxes:
            print(box)
        print("表格直线信息")
        print(AllLine)
        print("表格行信息")
        print(row)
        print("表格列信息")
        print(col)
        # 形成pdf文档
        # content = ''
        # # content += '<table border="1" cellspacing="0px" style="border-collapse:collapse">'
        # for key in result:
        #     # print(result[key][1])
        #     if boxes[key][0] - left > 20:
        #         #     if key % count == 0:
        #         #         content += '<tr>'
        #         #     tr = '<td>%s</td>' % result[key][1]
        #         #     content += tr
        #         #     if (key+1) % count == 0:
        #         #         content += '</tr>'
        #         # content += '</table>'
        #         content = content + '&emsp;&emsp;'
        #         if result[key][1][0] in {',', '.', '!', '{'}:
        #             content = content + result[key][1][1:] + '<br>'
        #         else:
        #             content = content + result[key][1] + '<br>'
        #     else:
        #         content = content + result[key][1] + '<br>'
        # html = '<html><head><meta charset="UTF-8"></head>' \
        #        '<body><div align="left"><p>%s</p></div></body></html>' % content
        # save_file = image_file.split('/')[-1].split('.')[0] + '.pdf'
        # pdfkit.from_string(html, save_file)
