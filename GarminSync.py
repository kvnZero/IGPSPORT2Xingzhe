import base64
import os.path
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from garth.http import Client
import zipfile

def encrpt(password, public_key):
    rsa = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(rsa)
    return base64.b64encode(cipher.encrypt(password.encode())).decode()

def syncData(garmin_email, garmin_password):
    if garmin_password is None or garmin_password == '':
        print("未设置账号密码，跳过脚本")
        return

    global_garth = Client()
    garth = Client()

    garth.configure(domain="garmin.cn")

    try:
        garth.login(garmin_email, garmin_password)
        global_garth.login(garmin_email, garmin_password)
    except Exception as e:
        print("登录态失败")
        print(e)
        return False

    global_activities = global_garth.connectapi(
        f"/activitylist-service/activities/search/activities",
        params={"activityType": "running", "limit": 5, "start": 0, 'excludeChildren': False}, #这里是跑步数据 骑行数据可修改成cycling
    )
    activities = garth.connectapi(
        f"/activitylist-service/activities/search/activities",
        params={"activityType": "running", "limit": 5, "start": 0, 'excludeChildren': False},
    )

    add_list = []
    has_exist = []
    for item2 in global_activities:
        has_exist.append(item2['startTimeGMT'])

    for item in activities:
        if item['startTimeGMT'] not in has_exist:
            rid = item['activityId']
            rid = str(rid)

            add_list.append(rid)
            if not os.path.isfile(rid+".zip"):
                res = garth.download(
                    f"/download-service/files/activity/{rid}",
                )
                with open(rid+".zip", "wb") as f:
                    f.write(res)
                with zipfile.ZipFile(rid + ".zip", 'r') as zip_ref:
                    zip_ref.extractall(rid)
        else:
            print("%s:已同步" % item['activityId'])

    print(add_list)
    print("本次同步数量：%s" % len(add_list))
    for u in add_list:
        with open(u + "/" + u + "_ACTIVITY.fit", 'rb') as fd:
            uploaded = requests.post('https://connectapi.garmin.com/upload-service/upload',
                          files={'file': fd},
                          headers={'authorization': global_garth.oauth2_token.__str__()})
            # uploaded = global_garth.upload(fd)
            print(uploaded.content)

    return True

activity = syncData(os.getenv("GARMIN_RUN_EMAIL"), os.getenv("GARMIN_RUN_PASSWORD"))
