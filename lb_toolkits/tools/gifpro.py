# -*- coding:utf-8 -*-
'''
@Project  : lb_toolkits
@File     : gifpro.py
@Modify Time      @Author    @Version
--------------    -------    --------
2022/8/6 16:42      Lee       1.0
@Description
------------------------------------

'''
import imageio
import os
from PIL import Image, ImageDraw


def creategif(outname, filels, duration=0.1):
    '''
    使用 imageio 生成 GIF
    :param outname: 输出GIF文件名
    :param filels: 输入需要创建GIF的图片列表
    :param duration: 时间间隔，控制GIF播放速度
    :return:
    '''

    frames = []
    # inpath = os.path.dirname(outname)
    # if not os.path.isdir(inpath):
    #     print("%s is not exist, will be create!!" % inpath)
    #     os.makedirs(inpath)

    if not outname.endswith(".gif") and not outname.endswith(".GIF"):
        outname  += ".gif"

    num = len(filels)
    for item in filels:
        num -= 1
        if not item.lower().endswith(".jpg") and not item.lower().endswith(".png"):
            print('文件后缀不是PNG或JPG格式文件，将跳过该文件【%s】' %(os.path.basename(item)))
            continue

        if not os.path.isfile(item):
            print("%s not exist, will be continue !!!!" % item)
            continue

        print("【%d】%s" % (num,item))
        frames.append(imageio.imread(item))

    imageio.mimsave(outname, frames, "GIF", duration = duration)
    # print("outname:",outname)

def creategif1(outname, filels, duration=0.1):
    '''
    使用 Image 生成 GIF
    :param files: 输入需要创建GIF的图片列表
    :param outname: 输出GIF文件名
    :param t: 时间间隔，控制GIF播放速度
    :return:
    '''
    imgs = []
    for item in filels:
        print(item)
        if not item.lower().endswith(".jpg") and not item.lower().endswith(".png"):
            print(not item.lower().endswith(".jpg") , not item.lower().endswith(".png"))
            continue

        if not os.path.isfile(item):
            print("%s not exist, will be continue !!!!" % item)
            continue

        temp = Image.open(item)
        imgs.append(temp)

    imgs[0].save(outname, save_all=True, append_images=imgs, duration=duration)
    print("outname:",outname)
    return outname

def splitgif(outdir, gifname):
    '''
    拆解GIF文件，还原成单幅图像
    Iterate the GIF, extracting each frame.
    '''
    img = Image.open(gifname)

    try:
        for i in range(img.n_frames) :
            img.seek(i)
            new_frame = Image.new('RGBA', img.size)

            new_frame.paste(img)

            outname = os.path.join(outdir, os.path.basename(gifname)+'_%d.png' %(i))
            new_frame.save(outname, 'PNG')
            print('[%d]成功创建：%s' %(i, outname))
    except EOFError:
        pass

def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results








