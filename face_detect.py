# coding=utf-8 
import os
import cv2
from PIL import Image,ImageDraw

#detectFaces()����ͼ�������������ľ������꣨�������ϡ����¶��㣩
#ʹ��haar�����ļ���������haarcascade_frontalface_default.xml����haarcascadesĿ¼�»���������ѵ���õ�xml�ļ��ɹ�ѡ��
#ע��haarcascadesĿ¼��ѵ���õķ����������ԻҶ�ͼ��Ϊ���롣
def detectFaces(image_name):
    img = cv2.imread(image_name)
    face_cascade = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml")
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img #if��䣺���imgά��Ϊ3��˵�����ǻҶ�ͼ����ת��Ϊ�Ҷ�ͼgray�������Ϊ3��Ҳ����2��ԭͼ���ǻҶ�ͼ

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)#1.3��5����������С������ⴰ�ڣ����ı�����Ҳ��ı�
    result = []
    for (x,y,width,height) in faces:
        result.append((x,y,x+width,y+height))
    return result


#��������ͼ
def saveFaces(image_name):
    faces = detectFaces(image_name)
    if faces:
        #������������save_dirĿ¼�¡�
        #Imageģ�飺Image.open��ȡͼ������crop����ͼ��(���е��������detectFaces���ص�����)��save���档
        save_dir = image_name.split('.')[0]+"_faces"
        os.mkdir(save_dir)
        count = 0
        for (x1,y1,x2,y2) in faces:
            file_name = os.path.join(save_dir,str(count)+".jpg")
            Image.open(image_name).crop((x1,y1,x2,y2)).save(file_name)
            count+=1


#��ԭͼ���ϻ����Σ��������������
#����Imageģ���draw������Image.open��ȡͼ������ImageDraw.Draw��ȡ��ͼ���drawʵ����Ȼ����ø�drawʵ����rectangle����������(���ε����꼴
#detectFaces���ص�����)��outline�Ǿ���������ɫ(B,G,R)��
#ע��ԭʼͼ������ǻҶ�ͼ����ȥ��outline����Ϊ�Ҷ�ͼû��RGB���ԡ�drawEyes��detectSmilesҲһ����
def drawFaces(image_name):
    faces = detectFaces(image_name)
    if faces:
        img = Image.open(image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1,y1,x2,y2) in faces:
            draw_instance.rectangle((x1,y1,x2,y2), outline=(255, 0,0))
        img.save('drawfaces_'+image_name)




#����۾�����������
#�����۾��������ϣ������������ȼ�����������ϸ��ؼ���۾�����detectEyes����detectFaces�����������У���������Ҫע�⡰������ꡱ��
#��ȻҲ����������ͼƬ��ֱ��ʹ�÷�����,���ַ��������detectFacesһ�������ﲻ��˵��
def detectEyes(image_name):
    eye_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')
    faces = detectFaces(image_name)

    img = cv2.imread(image_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = []
    for (x1,y1,x2,y2) in faces:
        roi_gray = gray[y1:y2, x1:x2]
        eyes = eye_cascade.detectMultiScale(roi_gray,1.3,2)
        for (ex,ey,ew,eh) in eyes:
            result.append((x1+ex,y1+ey,x1+ex+ew,y1+ey+eh))
    return result


#��ԭͼ���Ͽ���۾�.
def drawEyes(image_name):
    eyes = detectEyes(image_name)
    if eyes:
        img = Image.open(image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1,y1,x2,y2) in eyes:
            draw_instance.rectangle((x1,y1,x2,y2), outline=(0, 0,255))
        img.save('draweyes_'+image_name)


#���Ц��
def detectSmiles(image_name):
    img = cv2.imread(image_name)
    smiles_cascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_smile.xml")
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img #if��䣺���imgά��Ϊ3��˵�����ǻҶ�ͼ����ת��Ϊ�Ҷ�ͼgray�������Ϊ3��Ҳ����2��ԭͼ���ǻҶ�ͼ

    smiles = smiles_cascade.detectMultiScale(gray,4,5)
    result = []
    for (x,y,width,height) in smiles:
        result.append((x,y,x+width,y+height))
    return result


#��ԭͼ���Ͽ��Ц��
def drawSmiles(image_name):
    smiles = detectSmiles(image_name)
    if smiles:
        img = Image.open(image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1,y1,x2,y2) in smiles:
            draw_instance.rectangle((x1,y1,x2,y2), outline=(100, 100,0))
        img.save('drawsmiles_'+image_name)


if __name__ == '__main__':
	"""
	����Ĵ��뽫�۾���������Ц���ڲ�ͬ��ͼ���Ͽ���������Ҫ��ͬһ��ͼ���Ͽ������һ�´���Ϳ����ˡ�
	��֮������opencv��ѵ���õ�haar������xml�ļ�����ͼƬ�ϼ������������꣬����������꣬���ǿ��Խ�����������б��棬Ҳ������ԭͼ�Ͻ�������������б��������Լ��þ��ι��߿��������������ʹ�õ���PIL���Image��ImageDrawģ�顣
	���⣬opencv����Ҳ�л����ε�ģ�飬ͬ�������������������
	"""
    drawFaces('obama.jpg')
    #drawEyes('obama.jpg')
    #drawSmiles('obama.jpg')
    saveFaces('obama1.jpg')

