import RPi.GPIO as GPIO
import picamera
import dataset
from pyzbar.pyzbar import decode
from PIL import Image
import time, json, settings
import fourletterphat as flp
from decimal import Decimal
from modules import nano
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

GPIO.setmode(GPIO.BOARD)
channel1 = 11
GPIO.setup(channel1, GPIO.IN)
channel2 = 13
GPIO.setup(channel2, GPIO.IN)
channel3 = 15
GPIO.setup(channel3, GPIO.IN)
channel4 = 16
GPIO.setup(channel4, GPIO.IN)
channel5 = 18
GPIO.setup(channel5, GPIO.IN)
channel6 = 22
GPIO.setup(channel6, GPIO.IN)

coins = [ 0, 0 ]
timeout = 10

def my_callback_one(channel1):
    print('1p')
    coins[0] = coins[0] + 1
    coins[1] = time.time() + timeout

def my_callback_two(channel2):
    print('2p')
    coins[0] = coins[0] + 2
    coins[1] = time.time() + timeout

def my_callback_thr(channel3):
    print('5p')
    coins[0] = coins[0] + 5
    coins[1] = time.time() + timeout

def my_callback_fou(channel4):
    print('10p')
    coins[0] = coins[0] + 10
    coins[1] = time.time() + timeout

def my_callback_fiv(channel5):
    print('20p')
    coins[0] = coins[0] + 20
    coins[1] = time.time() + timeout

def my_callback_six(channel6):
    print('50p')
    coins[0] = coins[0] + 50
    coins[1] = time.time() + timeout


db = dataset.connect('sqlite:///users.db')
user_table = db['user']

camera = picamera.PiCamera()
camera.resolution = (1024, 768)
#camera.color_effects = (128, 128)

camera.start_preview()
# Camera warm-up time
time.sleep(2)

#text.write("Nano Hardware Faucet    Waiting for QR Code")

loop_count = 0

while 1:

  coins[0] = 0
  coins[1] = 0

  flp.print_str('SCAN')
  flp.show()

  camera.capture('image.jpg')

  print("Picture taken")

  result = decode(Image.open('image.jpg'))

  if len(result) > 0:
    print("Found QR Code")

    qr_code = result[0].data.decode("utf-8")
    print(qr_code)
    flp.scroll_print(qr_code.upper(), tempo=0.11)

    if len(qr_code) > 0:
        if qr_code[3] == ":":
           qr_code = qr_code[4:]

    #send_xrb(qr_code)

    print("Insert Coins")

    flp.print_str('GO!')
    flp.show()

    #Here we can count coins
    start_time = time.time() + timeout
    GPIO.add_event_detect(channel1, GPIO.RISING)
    GPIO.add_event_callback(channel1, my_callback_one)

    GPIO.add_event_detect(channel2, GPIO.RISING)
    GPIO.add_event_callback(channel2, my_callback_two)

    GPIO.add_event_detect(channel3, GPIO.RISING)
    GPIO.add_event_callback(channel3, my_callback_thr)

    GPIO.add_event_detect(channel4, GPIO.RISING)
    GPIO.add_event_callback(channel4, my_callback_fou)

    GPIO.add_event_detect(channel5, GPIO.RISING)
    GPIO.add_event_callback(channel5, my_callback_fiv)

    GPIO.add_event_detect(channel6, GPIO.RISING)
    GPIO.add_event_callback(channel6, my_callback_six)

    coins[1] = time.time() + timeout

    while time.time() < coins[1]:
        print("Waiting {}, {}".format(coins[0], coins[1]))
        flp.print_str('{}'.format(coins[0]))
        flp.show()

        time.sleep(1)

    GPIO.remove_event_detect(channel1)
    GPIO.remove_event_detect(channel2)
    GPIO.remove_event_detect(channel3)
    GPIO.remove_event_detect(channel4)
    GPIO.remove_event_detect(channel5)
    GPIO.remove_event_detect(channel6)

    flp.print_str('PROC')
    flp.show()
    count_loop = 0
    nano_sent = 1
    while nano_sent == 1:
        try:
            price = cg.get_price(ids='nano', vs_currencies='gbp')
            gbp_price = price['nano']['gbp']
            print("GBP Price: {}".format(gbp_price))

            nano_to_send = Decimal(gbp_price) * (Decimal(coins[0]) / Decimal(100))
            print("Nano to send: {}".format(nano_to_send))

            raw_to_send = Decimal(nano_to_send) * Decimal(1000000000000000000000000000000)
            print("Raw to send: {}".format(raw_to_send))

            if qr_code[:4] == 'nano':
                dest_account = 'xrb' + qr_code[4:]

            print("{} {} {} {} {}".format(dest_account, int(raw_to_send), settings.address, int(0), settings.wallet_seed))

            return_block = nano.send_xrb(dest_account, int(raw_to_send), settings.address, int(0), settings.wallet_seed)
            print(return_block)
            nano_sent = 0
        except Exception as e:
            print(e)
            time.sleep(1)
            count_loop = count_loop + 1
            if count_loop > 5:
               flp.print_str('ERR')
               flp.show()

    flp.print_str('SENT')
    flp.show()

    user_table.insert(dict(address=qr_code, requests=0, time=int(time.time()), loop=loop_count, claim=1))

    time.sleep(5)

    print("Nano Hardware Faucet    Waiting for QR Code")


