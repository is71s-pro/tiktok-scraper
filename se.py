from hashlib import md5
from time import time
import random
import asyncio
import aiohttp
import os
import binascii
import uuid
import urllib.parse
import pycountry
import sys
from hsopyt import Gorgon, Argus, Ladon
from colorama import Fore, Style, init
init()




class Scraping:
    def __init__(self):
        self.region = input("Enter country Example : [ SA ] ").upper()
        self.max_following = 100
        self.add = []
        self.users = set()
        self.lock = asyncio.Lock()
        self.a = 0
        self.following_list = []
        try:
            self.a1 = int(input("Enter Start Followers Example : [ 1000 ] "))
            self.a2 = int(input("Enter End Followers Example : [ 9999 ] "))
        except:
            print("[ Error ] Please enter a number only!")
            exit()
        self.geting_new_ids = 0
        self.start_get_id_followings = 0
        self.start_get_users_followings = 0

    def see(self):
        text = f"""\r
{Fore.CYAN}═══════════════════════════════════
{Fore.YELLOW} COUNTRY        : {Fore.WHITE}{self.get_country()}
{Fore.GREEN} NEW IDS        : {Fore.WHITE}{self.geting_new_ids}
{Fore.BLUE} FOLLOWING IDS  : {Fore.WHITE}{self.start_get_id_followings}
{Fore.MAGENTA} SAVED          : {Fore.WHITE}{self.start_get_users_followings}
{Fore.RED} RANGE          : {Fore.WHITE}{self.a1} - {self.a2}
{Fore.CYAN}═══════════════════════════════════{Style.RESET_ALL}
"""
        sys.stdout.write('\033[H\033[J')
        sys.stdout.write(text)

    def get_country(self):
        country = pycountry.countries.get(alpha_2=self.region.upper()) if self.region else None
        return getattr(country, "name", "")

    def sign(self, params, payload: str = None, sec_device_id: str = "", cookie=None,
             aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "2.3.1.i18n",
             sdk_version: int = 2, platform: int = 19, unix: int = None):
        x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload is not None else None
        if not unix:
            unix = int(time())
        return Gorgon(params, unix, payload, cookie).get_value() | {
            "x-ladon": Ladon.encrypt(unix, license_id, aid),
            "x-argus": Argus.get_sign(params, x_ss_stub, unix, platform=platform, aid=aid,
                                      license_id=license_id, sec_device_id=sec_device_id,
                                      sdk_version=sdk_version_str, sdk_version_int=sdk_version)
        }

    def Vals(self):
        return {
            "manifest_version_code": "330802",
            "_rticket": str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632",
            "app_language": "ar",
            "app_type": "normal",
            "iid": str(random.randint(1, 10 ** 19)),
            "channel": "googleplay",
            "device_type": "RMX3511",
            "language": "ar",
            "host_abi": "arm64-v8a",
            "locale": "ar",
            "resolution": "1080*2236",
            "openudid": str(binascii.hexlify(os.urandom(8)).decode()),
            "update_version_code": "330802",
            "ac2": "lte",
            "cdid": str(uuid.uuid4()),
            "sys_region": "IQ",
            "os_api": "33",
            "timezone_name": "Asia/Baghdad",
            "dpi": "360",
            "carrier_region": "IQ",
            "ac": "4g",
            "device_id": str(random.randint(1, 10 ** 19)),
            "os_version": "13",
            "timezone_offset": "10800",
            "version_code": "330802",
            "app_name": "musically_go",
            "ab_version": "33.8.2",
            "app_version": "33.8.2",
            "version_name": "33.8.2",
            "device_brand": "realme",
            "op_region": "IQ",
            "ssmix": "a",
            "device_platform": "android",
            "build_number": "33.8.2",
            "region": "IQ",
            "aid": "1340",
            "ts": str(round(random.uniform(1.2, 1.6) * 100000000) * -1)
        }, {
            'User-Agent': 'com.zhiliaoapp.musically/2023001020 (Linux; U; Android 13; ar; RMX3511; Build/TP1A.220624.014; Cronet/TTNetVersion:06d6a583 2023-04-17 QuicVersion:d298137e 2023-02-13)'
        }

    async def get_following_and_save(self, session, user_id):
        token = None
        while True:
            try:
                p, h = self.Vals()
                signed = self.sign(params=urllib.parse.urlencode(p), payload="", cookie="")
                h.update({
                    'x-ss-req-ticket': signed['x-ss-req-ticket'],
                    'x-argus': signed["x-argus"],
                    'x-gorgon': signed["x-gorgon"],
                    'x-khronos': signed["x-khronos"],
                    'x-ladon': signed["x-ladon"]
                })

                base_url = f'https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/following/list/?user_id={user_id}&count=50&source_type=1&request_tag_from=h5&{urllib.parse.urlencode(p)}'
                if token:
                    base_url += f"&page_token={urllib.parse.quote(token)}"

                async with session.get(base_url, headers=h) as response:
                    data = await response.json()

                for user in data.get("followings", []):
                    uname = user.get("unique_id")
                    uid = user.get("uid")
                    reg = user.get("region")
                    fol = user.get("follower_count")

                    async with self.lock:
                        if uname and uname not in self.users:
                            if reg == self.region:
                                if self.a1 <= int(fol) <= self.a2:
                                    self.start_get_users_followings += 1
                                    self.users.add(uname)
                                    self.see()
                                    with open(f"{self.get_country()}.txt", "a", encoding="utf-8") as f:
                                        f.write(uname + "\n")
                                if uid not in self.following_list:
                                    self.following_list.append(uid)
                                    self.start_get_id_followings += 1

                if not data.get("has_more"):
                    break
                token = data.get("next_page_token")
                if not token:
                    break
            except:
                break

    def gen_keyword(self):
        chars = random.choice([
            'azertyuiopmlkjhgfdsqwxcvbn',
            'abcdefghijklmnopqrstuvwxyz',
            'abcdefghijklmnopqrstuvwxyzñ',
            '的一是不了人我在有他这为之大来以个中上们到说时国和地要就出会可也你对生能而子那得于着下自之',
            'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん',
            'αβγδεζηθικλμνξοπρστυφχψω',
        ])
        return ''.join(random.choice(chars) for _ in range(random.randint(3, 6)))

    async def search_worker(self, session):
        while True:
            try:
                keyword = self.gen_keyword()
                params = {
                    'aid': '1340',
                    'device_id': str(random.randint(10**18, 10**19 - 1)),
                    'keyword': keyword,
                    'ts': str(int(time() * 1000)),
                    'count': '30',
                    'cursor': '0',
                    'type': '1'
                }
                url = "https://search19-normal-alisg.tiktokv.com/aweme/v1/discover/search/"
                async with session.get(url, params=params) as data:
                    r = await data.json()
                    user_list = r.get('user_list', [])

                    for user in user_list:
                        info = user.get('user_info', {})
                        following = info.get('following_count', 0)
                        region = info.get('region', 'NA')
                        uid = info.get('uid')

                        if region == self.region and following > self.max_following:
                            self.geting_new_ids += 1
                            self.see()
                            if uid not in self.add:
                                self.add.append(uid)
                                asyncio.create_task(self.get_following_and_save(session, uid))
            except:
                continue

    async def process_following_list(self, session):
        while True:
            await asyncio.sleep(5)
            async with self.lock:
                if self.following_list:
                    batch = self.following_list[:50]
                    self.following_list = self.following_list[50:]
                else:
                    batch = []
            for uid in batch:
                asyncio.create_task(self.get_following_and_save(session, uid))

    async def run(self):
        async with aiohttp.ClientSession() as session:
            workers = [asyncio.create_task(self.search_worker(session)) for _ in range(200)]
            workers.append(asyncio.create_task(self.process_following_list(session)))
            await asyncio.gather(*workers)


asyncio.run(Scraping().run())