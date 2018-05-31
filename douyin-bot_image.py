# -*- coding: utf-8 -*-
import sys
import random
import time
import os

from PIL import Image, ImageDraw, ImageFont

from common import apiutil

if sys.version_info.major != 3:
    print('Please run under Python3')
    exit(1)
try:
 pass
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

VERSION = "0.0.1"

# 我申请的 Key，随便用，嘻嘻嘻
# 申请地址 http://ai.qq.com
AppID = '1106863285'
AppKey = '5ihqtj5yQY7mhUOT'

DEBUG_SWITCH = True
FACE_PATH = 'face/'



# 审美标准
BEAUTY_THRESHOLD = 80



def main0():
    print('程序版本号：{}'.format(VERSION))
    print('激活窗口并按 CONTROL + C 组合键退出')

    for p in os.listdir(  FACE_PATH):
        if os.path.isfile( FACE_PATH + p):  # 判断是否为文件夹，如果是输出所有文件就改成： os.path.isfile(p)
            print(p)
            (filepath, tempfilename)=os.path.split( FACE_PATH + p)
            (filename, extension)=os.path.splitext(tempfilename)
            if extension=='.jpg':
                with open( FACE_PATH + p, 'rb') as bin_data:
                    image_data = bin_data.read()

                ai_obj = apiutil.AiPlat(AppID, AppKey)
                rsp = ai_obj.face_detectface(image_data, 1)

                if rsp['ret'] == 0:
                    beauty = 0
                    for face in rsp['data']['face_list']:
                        print(face)
                        face_area = (face['x'], face['y'], face['x'] + face['width'], face['y'] + face['height'])
                        print(face_area)

                        img =Image.open( FACE_PATH + p)

                        #img.show()
                        drawObject=ImageDraw.Draw(img)
                        drawObject.rectangle(face_area, outline="red")

                        drawObject.polygon(getList(face['face_shape']['face_profile']), outline="yellow")
                        drawObject.polygon(getList(face['face_shape']['left_eyebrow']), outline="white")
                        drawObject.polygon(getList(face['face_shape']['right_eyebrow']), outline="white")
                        drawObject.polygon(getList(face['face_shape']['left_eye']), outline="white")
                        drawObject.polygon(getList(face['face_shape']['right_eye']), outline="white")
                        #'left_eyebrow'
                        drawObject.polygon(getList(face['face_shape']['mouth']), outline="green")
                        drawObject.polygon(getList(face['face_shape']['nose']), outline="#ffcc00")
                        BASE_PATH='.' + os.sep

                        hwls_path=os.path.join(BASE_PATH, "font", "STKAITI.ttf")
                        hwls_font=ImageFont.truetype(hwls_path, 14)
                        gender__format=u'魅力={},性别={}'.format(face['beauty'], face['gender'])
                        drawObject.text( (50,img.size[1]-50),
                                        gender__format, "#ccFFcc",hwls_font)
                        #
                        #drawObject.rectangle(face_area, fill=128)
                        img.save(FACE_PATH + face['face_id'] + 'box.png')
                        cropped_img = img.crop(face_area).convert('RGB')
                        cropped_img.save(FACE_PATH + face['face_id'] + 'crop.png')
                        # 性别判断
                        if face['beauty'] > beauty and face['gender'] < 50:
                            beauty = face['beauty']

                    # 是个美人儿~关注点赞走一波
                    if beauty > BEAUTY_THRESHOLD:
                        print('发现漂亮妹子！！！')


                else:
                    print(rsp)
                    continue


def getList(face_shape):

    tuple_shape=list(map(dict2tuple, face_shape))
    return tuple_shape


def dict2tuple(r):
    rx=r['x']
    ry=r['y']
    return   (rx,ry)


if __name__ == '__main__':
    try:
        # yes_or_no()
        main0()
    except KeyboardInterrupt:
        # adb.run('kill-server')
        print('\n谢谢使用', end='')
        exit(0)
