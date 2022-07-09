# computer_vision_End_of_period-
实验方案与分析：
任务大体上分为四个部分，一个是检测出运动目标的轮廓，二是将轮廓用链码表达，三是对目标进行跟踪，四是检测物体的运动轨迹。
编程语言：python
编程IDE：pycharm
录屏视频：做抛物运动的橡皮。
整体上，我们使用opencv的cv2库，我们使用了opencv-python==3.4.18.65的版本，之所以没有使用最新的版本是因为4.0+的版本的imshow有一些问题，不便于编程。
我们的任务是视频分析，所以我们都要使用cv.VideoCapture('****.mp4')来读取视频，在这里先进行一下说明。
Part1：检测出运动目标的轮廓
我们的目标是使用cv.findContours()获得物体的轮廓。它要求使用二值图，通过观察我们自己用手机录制的视频，发现物体和背景较好的区分，因此我们直接使用了阈值分割。
ret, thresh = cv.threshold(gray_frame, 127, 255, cv.THRESH_BINARY)
效果很好,见下图。

然后就是进行轮廓的绘制，在有二值图的前提下相对简单：
img,contours,hierarchy=cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(gray_frame, contours, -1, (0,255,0), 3)
效果如下：

Part2:链码的生成
我们链码的生成依赖，cv.findContours()的返回值在他的返回值的基础上，我们进行链码的生成。
cv.findContours()会返回轮廓的像素坐标，根据这些像素坐标，不难得到对应的链码。

代码如下：
"""得到链码"""
for c in contours:
    cnt = np.squeeze(c)
    cnt = np.insert(cnt, 0, cnt[-1], axis=0)  # 循环填补
    #print(len(cnt))
    if(len(cnt)>20):
        freeman_code = chain_code(cnt)
        print("链码的长度为{}".format(len(freeman_code)))
        print(freeman_code)
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
Part3:运动目标的追踪：
尝试了多种的方案，最终选用了基于帧间差异的目标跟踪方法。
效果也还不错：


我们还尝试过，连续自适应 Meanshift 算法，效果不太好：

会发现，跟踪框不随物体运动变化，推测可能是因为物体运动速度过快。
Part4：检测出运动轨迹：
这个需求在运动目标跟踪的基础上不难完成，我们只要定义一个track_path = []数组，然后之后将所有矩阵框的中心点左边传进去，然后随着每一次的变化打印即可。
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
效果如下：

因为物体做的是抛物运动，所以观测轨迹曲线，不难发现轨迹的合理性。

实验的最终效果如下：
