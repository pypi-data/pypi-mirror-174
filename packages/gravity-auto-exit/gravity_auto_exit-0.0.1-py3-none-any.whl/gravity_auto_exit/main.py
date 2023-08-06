import datetime
import logging
import threading
import time
from cad.main import CAD
from whikoperator.main import Wpicoperator
import requests
import io
from PIL import Image


class AutoExit:
    def __init__(self, cam_host, cam_login, cam_password,
                 auth_method='Digest', engine_callback=None):
        self.cad = CAD(host=cam_host, login=cam_login, password=cam_password,
                       callback_func=self.cad_callback_func, delay_time=0)
        cam_ip = cam_host.replace('http://', '')
        self.cam = Wpicoperator(cam_ip=cam_ip,
                                cam_login=cam_login,
                                cam_pass=cam_password,
                                auth_method=auth_method)
        self.count = 0
        self.last_take = datetime.datetime.now()
        threading.Thread(target=self.counter_checker).start()
        self.engine_callback = engine_callback
        logging.info('AUTO_EXIT has started successfully')

    def cut_photo(self, photo):
        img = Image.open(io.BytesIO(photo))
        # left, upper, right, lower
        im_r = img.crop((930, 900, 1500, 1100))
        im_r.show()
        img_byte_arr = io.BytesIO()
        im_r.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

    def cad_callback_func(self, data):
        self.count += 1
        logging.debug(f'self.count: {self.count}')
        if self.count >= 5 and datetime.datetime.now() - self.last_take > datetime.timedelta(
                seconds=15):
            result = self.try_recognise_plate()
            if result:
                if self.engine_callback:
                    self.engine_callback(result)
                self.last_take = datetime.datetime.now()
                self.count = 0
                return result

    def try_recognise_plate(self):
        photo = self.cam.take_shot()
        photo = self.cut_photo(photo)
        # Отправляю запрос
        response = self.get_state_number(
            url='https://dispatcher.ml.neuro-vision.tech/1.4/predict/'
                'car_plate_gpu',
            photo=photo,
            login='admin',
            password='admin'
        )
        number = self.parse_recognition_result(response.json())
        return number

    def get_state_number(self, url, photo, login, password):
        files = {'images': ('image.jpg', photo, 'image/jpeg')}
        response = requests.post(url, files=files,
                                 auth=(login, password))
        return response

    def parse_recognition_result(self, response):
        if response['results'][0]['status'] == 'Success':
            return response['results'][0]['plate']

    def counter_checker(self):
        count_time = datetime.datetime.now()
        count_now = self.count
        while True:
            if self.count != count_now:
                count_now = self.count
                count_time = datetime.datetime.now()
            if count_now != 0 and self.count == count_now and (
                    datetime.datetime.now() - count_time > datetime.timedelta(
                seconds=6)):
                self.count = 0
            time.sleep(1)


if __name__ == '__main__':
    inst = AutoExit('http://127.0.0.1',
                    'admin',
                    'Assa+123')
    inst.cad.mainloop()