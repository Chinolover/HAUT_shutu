from PIL import Image,ImageDraw

base_image = Image.open("./blurred.jpg")
width,height = base_image.size 
#生成一张尺寸和底图尺寸一样，背景为白色的模板
bg = Image.new('RGB',(width,height),color=(255,255,0,0))
#bg.paste(base_image,(0,0))

#头像尺寸
avatar_size =(256,256)
avatar = Image.open("./Circle.png")
avatar = avatar.resize(avatar_size)

#新建模板图
mask = Image.new('RGBA',(256,256),color=(0,0,0,0))
#mask.paste(avatar,(0,0))

#画圆
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse((0,0,avatar_size[0],avatar_size[1]),fill=(159,159,159))

bg.paste(base_image,(0,0))  #底片粘贴
bg.paste(avatar,(128,128),mask)     #圆形粘贴

bg.save("./LLLast.png","PNG")