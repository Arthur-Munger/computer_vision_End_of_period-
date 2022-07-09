# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import numpy as np
import cv2 as cv
cap = cv.VideoCapture('eraser3.mp4')
i=5
# 生成椭圆结构元素
es = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 4))
# 设置背景帧
background = None
track_path = []
def chain_code(cnt):
    diff_cnt=np.diff(cnt,axis=0)
    a = diff_cnt.tolist()
    for i in a:
        for j in range(0,2):
            if(i[j]>0):
                i[j]=1
            elif(i[j]<0):
                i[j]=-1
    dic={(1,0):0,(1,1):1,(0,1):2,(-1,1):3,(-1,0):4,(-1,-1):5,(0,-1):6,(1,-1):7}
    direction=[tuple(x) for x in a]#tuple([-607, 0])转换为元组(-607, 0)
    code=list(map(dic.get,direction))
    code=np.array(code)
    return code
while(True):
    # 一帧一帧捕捉
    ret, frame = cap.read()
    # 我们对帧的操作在这里\
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray_frame, 127, 255, cv.THRESH_BINARY)
    img,contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #cv.drawContours(gray_frame, contours, -1, (0,255,0), 3)
    """得到链码"""
    for c in contours:
        cnt = np.squeeze(c)
        cnt = np.insert(cnt, 0, cnt[-1], axis=0)  # 循环填补
        #print(len(cnt))
        if(len(cnt)>20):
            freeman_code = chain_code(cnt)
            print("链码的长度为{}".format(len(freeman_code)))
            print(freeman_code)
    """运动跟踪和轨迹部分"""
    #获取背景帧
    if background is None:
        # 将视频的第一帧图像转为灰度图
        background = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # 对灰度图进行高斯模糊,平滑图像
        background = cv.GaussianBlur(background, (21, 21), 0)
        continue

    # 将视频的每一帧图像转为灰度图
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # 对灰度图进行高斯模糊,平滑图像
    gray_frame = cv.GaussianBlur(gray_frame, (21, 21), 0)

    # 获取当前帧与背景帧之间的图像差异,得到差分图
    diff = cv.absdiff(background, gray_frame)

    # 利用像素点值进行阈值分割,得到一副黑白图像
    diff = cv.threshold(diff, 25, 255, cv.THRESH_BINARY)[1]

    # 膨胀图像,减少错误
    diff = cv.dilate(diff, es, iterations=2)

    # 得到图像中的目标轮廓
    image, cnts, hierarchy = cv.findContours(diff.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if (cv.contourArea(c) > 10000): # and cv.contourArea(c) < 65000):
        # 绘制目标矩形框
         # print(cv.contourArea(c))
          (x, y, w, h) = cv.boundingRect(c)
          cv.rectangle(frame, (x+2, y+2), (x+w, y+h), (54, 54, 54), 2)
          #绘制运动轨迹
          x1 = int(x+w/2)
          y1 = int(y+h/2)
          mid = np.array([x1,y1])
          track_path.append(mid)
     #   print(mid)
    for i in range(1,len(track_path)):
        cv.line(frame,(track_path[i-1][0],track_path[i-1][1]),
                (track_path[i][0],track_path[i][1]),
                (130,130,130), 2, 6, 0)
    # 显示检测视频
    # cv.namedWindow('contours', 0)
    # cv.resizeWindow('contours', 600, 400)
    # cv.imshow('contours', frame)
    cv.drawContours(frame, contours, -1, (28, 28, 28), 3)
    # 显示返回的每帧
    cv.imshow('frame',frame)

    # if (i == 1):
    #     print(len(freeman_code))
    #     print(freeman_code)
        #print(hierarchy)
        #cv.imwrite('frame',gray)
    i = i - 1
    #cv.imshow('frame',frame)
    if cv.waitKey(500) & 0xFF == ord('q'):
        break
# 当所有事完成，释放 VideoCapture 对象
cap.release()
cv.destroyAllWindows()



