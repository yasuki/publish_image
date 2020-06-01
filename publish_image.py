# -*- coding: utf-8 -*-
#
# Usage: python publish_image.py <IMAGE FILE> <TITLE>
#
#
import sys

# ライブラリ読み込み
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS

def get_exif_rotation(orientation_num):
    """
    ExifのRotationの数値から、回転する数値と、ミラー反転するかどうかを取得する
    return 回転度数,反転するか(0 1)
    # 参考: https://qiita.com/minodisk/items/b7bab1b3f351f72d534b
    """
    if orientation_num == 1:
        return 0, 0
    if orientation_num == 2:
        return 0, 1
    if orientation_num == 3:
        return 180, 0
    if orientation_num == 4:
        return 180, 1
    if orientation_num == 5:
        return 270, 1
    if orientation_num == 6:
        return 270, 0
    if orientation_num == 7:
        return 90, 1
    if orientation_num == 8:
        return 90, 0
    else:
        return 0, 0

# 画像の向きを取得
def get_exif_orientation(img):
    exif=img._getexif()

    exif_table={}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = str(value)

    try:
        ret = exif_table['Orientation']
    except:
        ret = 0

    return ret

# 画像を回転
def get_rotation_image(img):
    print ('Orientation: '+str(get_exif_orientation(img)))
    rotate,reverse = get_exif_rotation( int(get_exif_orientation(img)) )

    if reverse == 1:
        img = ImageOps.mirror(img)
    if rotate != 0:
        img = img.rotate(rotate, expand=True)
    return img

# 画像の短辺のサイズを取得
def get_resize_y(x, y, resize_x):
    if x >= y:
        resize_y = resize_x * y /x
    if x < y:
        resize_y = resize_x * x / y
    return int(resize_y)

# 指定したピクセルの色を取得
def get_text_color(img,x,y):
    pixel=img.getpixel( (x,y) )
    if (pixel[0]+pixel[1]+pixel[2])/3 > 128 :
        return (0,0,0)
    else:
        return (255,255,255)

# タイトルを出力
def draw_title(img,title):
    font_file="/home/user/publish_image/TakaoPGothic.ttf"
    font_size=45
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_file, font_size)
    text_color=get_text_color(img,100,100)
    draw.text((10, 10), title, fill=text_color, font=font)
    return img

# シグニチャを出力
def draw_signiture(img,sig):
    font_file="/home/user/publish_image/TakaoPGothic.ttf"
    font_size=10
    width,height=img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_file, font_size)
    text_color=get_text_color(img,width-150,height-30)
    draw.text((width-150, height-30), sig, fill=text_color, font=font)
    return img

###############################################
# main
###############################################
# リサイズする長辺のサイズ(オリジナルは6000)
resize_x = 1200
# 出力するファイルにつけるサフィックス
suffix = '_text'
# Signitureの文字列
signiture = u'どっとBlogrc\nhttp://dotblogrc.blogspot.com/'

# 引数を取得
args=sys.argv
if len(args) < 2:
    print('Usage: python '+args[0]+' <Image File> <Title>')
    exit()
filename=args[1]

# 画像をオープン
img = Image.open(filename)

# 画像の回転
img = get_rotation_image(img)

# 画像のリサイズ
width,height = img.size
print('Original size: '+ str(width) + ' ' + str(height) )

if width >= height :
    img = img.resize( (resize_x, get_resize_y(width,height,resize_x)) )
else:
    img = img.resize( (get_resize_y(width,height,resize_x), resize_x) )

width,height = img.size
print('Resized size: '+ str(width) + ' ' + str(height) )

# タイトルとシグニチャの描画
if len(args)>2:
    img = draw_title( img, args[2] )
img = draw_signiture( img, signiture )

# 画像の保存
f=filename.split(".")
output_filename=f[0]+suffix+'.'+f[1]

img.save(output_filename)
print ('Saved: '+output_filename)
