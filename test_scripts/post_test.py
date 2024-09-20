from requests import post

URL = "https://script.google.com/macros/s/AKfycbx6wPNqYTieuuD5W6441Im1kWIoejl3Oze2mHHC07Wy18FoQr_Y1vQ4vJ_qXpdOeL0jYw/exec"
data_points_key = "p"
parallelism_value_key = "parallelismValue"

data = {
    "0": 0.000,
    "1": 0.001,
    "2": 0.002,
    "3": 0.003,
    "4": 0.004,
    "5": 0.005,
    "6": 0.006,
    "7": 0.007,
    "8": 0.008
}
parallelism_value = 29

post_url = \
    f"{URL}?" \
    f"{data_points_key}=" \
    f"{str(data['0'])}," \
    f"{str(data['1'])}," \
    f"{str(data['2'])}," \
    f"{str(data['3'])}," \
    f"{str(data['4'])}," \
    f"{str(data['5'])}," \
    f"{str(data['6'])}," \
    f"{str(data['7'])}," \
    f"{str(data['8'])}&" \
    f"{parallelism_value_key}=" \
    f"{str(parallelism_value)}"

print(post_url)

ret = post(post_url)

print(ret)