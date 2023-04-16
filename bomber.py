#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import sys
import subprocess
import string
import random
import json
import re
import time
import argparse
import zipfile
from io import BytesIO

from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.decorators import MessageDecorator
from utils.provider import APIProvider

try:
    import requests
    from colorama import Fore, Style
except ImportError:
    print("\tBazı bağımlılıklar içe aktarılamadı (yüklü olmayabilir)")
    print(
        "Type `pip3 install -r requirements.txt` to "
        " gerekli tüm paketleri kurun")
    sys.exit(1)


def readisdc():
    with open("isdcodes.json") as file:
        isdcodes = json.load(file)
    return isdcodes


def get_version():
    try:
        return open(".version", "r").read().strip()
    except Exception:
        return '1.0'


def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def bann_text():
    clr()
    logo = """
 $$$$$$$\                       $$\           $$$$$$$\                          $$$$$$$\  
$$  __$$\                      $$ |          $$  __$$\                         $$  __$$\ 
$$ |  $$ | $$$$$$\   $$$$$$\ $$$$$$\         $$ |  $$ | $$$$$$\  $$$$$$\$$$$\  $$ |  $$ |
$$$$$$$  |$$  __$$\ $$  __$$\\_$$  _|$$$$$$\ $$$$$$$\ |$$  __$$\ $$  _$$  _$$\ $$$$$$$\ |
$$  __$$< $$ /  $$ |$$ /  $$ | $$ |  \______|$$  __$$\ $$ /  $$ |$$ / $$ / $$ |$$  __$$\ 
$$ |  $$ |$$ |  $$ |$$ |  $$ | $$ |$$\       $$ |  $$ |$$ |  $$ |$$ | $$ | $$ |$$ |  $$ |
$$ |  $$ |\$$$$$$  |\$$$$$$  | \$$$$  |      $$$$$$$  |\$$$$$$  |$$ | $$ | $$ |$$$$$$$  |
\__|  \__| \______/  \______/   \____/       \_______/  \______/ \__| \__| \__|\_______/ 
                                                                                         
                                                                                         
                                                                                          """
    if ASCII_MODE:
        logo = ""
    version = "Version: "+__VERSION__
    contributors = "Contributors: "+" ".join(__CONTRIBUTORS__)
    print(random.choice(ALL_COLORS) + logo + RESET_ALL)
    mesgdcrt.SuccessMessage(version)
    mesgdcrt.SectionMessage(contributors)
    print()


def check_intr():
    try:
        requests.get("https://motherfuckingwebsite.com")
    except Exception:
        bann_text()
        mesgdcrt.FailureMessage("Zayıf internet bağlantısı algılandı")
        sys.exit(2)


def format_phone(num):
    num = [n for n in num if n in string.digits]
    return ''.join(num).strip()


def do_zip_update():
    success = False
    if DEBUG_MODE:
        zip_url = "https://github.com/TheRoot-B/Root-BomB/archive/dev.zip"
        dir_name = "Root-BomB-dev"
    else:
        zip_url = "https://github.com/TheRoot-B/Root-BomB/archive/master.zip"
        dir_name = "Root-BomB-master"
    print(ALL_COLORS[0]+"Downloading ZIP ... "+RESET_ALL)
    response = requests.get(zip_url)
    if response.status_code == 200:
        zip_content = response.content
        try:
            with zipfile.ZipFile(BytesIO(zip_content)) as zip_file:
                for member in zip_file.namelist():
                    filename = os.path.split(member)
                    if not filename[1]:
                        continue
                    new_filename = os.path.join(
                        filename[0].replace(dir_name, "."),
                        filename[1])
                    source = zip_file.open(member)
                    target = open(new_filename, "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
            success = True
        except Exception:
            mesgdcrt.FailureMessage("Ayıklanırken hata oluştu !!")
    if success:
        mesgdcrt.SuccessMessage("Root-BomB en son sürüme güncellendi")
        mesgdcrt.GeneralMessage(
            "En son sürümü yüklemek için lütfen betiği tekrar çalıştırın")
    else:
        mesgdcrt.FailureMessage("Root-BomB güncellenemiyor.")
        mesgdcrt.WarningMessage(
            "En Sonuncuyu Alın https://github.com/TheRoot-B/Root-BomB.git")

    sys.exit()


def do_git_update():
    success = False
    try:
        print(ALL_COLORS[0]+"UPDATING "+RESET_ALL, end='')
        process = subprocess.Popen("git checkout . && git pull ",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        while process:
            print(ALL_COLORS[0]+'.'+RESET_ALL, end='')
            time.sleep(1)
            returncode = process.poll()
            if returncode is not None:
                break
        success = not process.returncode
    except Exception:
        success = False
    print("\n")

    if success:
        mesgdcrt.SuccessMessage("Root-BomB en son sürüme güncellendi")
        mesgdcrt.GeneralMessage(
            "En son sürümü yüklemek için lütfen betiği tekrar çalıştırın")
    else:
        mesgdcrt.FailureMessage("Root-BomB güncellenemiyor.")
        mesgdcrt.WarningMessage("Yüklediğinizden emin olun 'git' ")
        mesgdcrt.GeneralMessage("Ardından komutu çalıştırın:")
        print(
            "git checkout . && "
            "git pull https://github.com/TheRoot-B/Root-BomB.git HEAD")
    sys.exit()


def update():
    if shutil.which('git'):
        do_git_update()
    else:
        do_zip_update()


def check_for_updates():
    if DEBUG_MODE:
        mesgdcrt.WarningMessage(
            "HATA AYIKLAMA MODU Etkin! Otomatik Güncelleme kontrolü devre dışı bırakıldı.")
        return
    mesgdcrt.SectionMessage("Güncellemeler kontrol ediliyor")
    fver = requests.get(
        "https://raw.githubusercontent.com/TheRoot-B/Root-BomB/master/.version"
    ).text.strip()
    if fver != __VERSION__:
        mesgdcrt.WarningMessage("Bir güncelleme mevcut")
        mesgdcrt.GeneralMessage("Güncelleme başlatılıyor...")
        update()
    else:
        mesgdcrt.SuccessMessage("Root-BomB güncele")
        mesgdcrt.GeneralMessage("Root-BomB Başlatılıyor")


def notifyen():
    try:
        if DEBUG_MODE:
            url = "https://github.com/TheRoot-B/Root-BomB/raw/dev/.notify"
        else:
            url = "https://github.com/TheRoot-B/Root-BomB/raw/master/.notify"
        noti = requests.get(url).text.upper()
        if len(noti) > 10:
            mesgdcrt.SectionMessage("NOTIFICATION: " + noti)
            print()
    except Exception:
        pass


def get_phone_info():
    while True:
        target = ""
        cc = input(mesgdcrt.CommandMessage(
            "ülke kodunuzu girin (Olmadan +): "))
        cc = format_phone(cc)
        if not country_codes.get(cc, False):
            mesgdcrt.WarningMessage(
                "ülke kodu ({cc}) girmiş olduğun"
                " geçersiz veya desteklenmiyor".format(cc=cc))
            continue
        target = input(mesgdcrt.CommandMessage(
            "hedef numarayı girin: +" + cc + " "))
        target = format_phone(target)
        if ((len(target) <= 6) or (len(target) >= 12)):
            mesgdcrt.WarningMessage(
                "Telefon numarası ({target})".format(target=target) +
                "girmiş olduğunuz geçersiz")
            continue
        return (cc, target)


def get_mail_info():
    mail_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while True:
        target = input(mesgdcrt.CommandMessage("Hedef postayı girin: "))
        if not re.search(mail_regex, target, re.IGNORECASE):
            mesgdcrt.WarningMessage(
                "Posta ({target})".format(target=target) +
                " girmiş olduğunuz geçersiz")
            continue
        return target


def pretty_print(cc, target, success, failed):
    requested = success+failed
    mesgdcrt.SectionMessage("Bombalama sürüyor - Lütfen sabırlı olun")
    mesgdcrt.GeneralMessage(
        "Bombalama sırasında lütfen internete bağlı kalın")
    mesgdcrt.GeneralMessage("Target       : " + cc + " " + target)
    mesgdcrt.GeneralMessage("Sent         : " + str(requested))
    mesgdcrt.GeneralMessage("Successful   : " + str(success))
    mesgdcrt.GeneralMessage("Failed       : " + str(failed))
    mesgdcrt.WarningMessage(
        "Bu araç yalnızca eğlence ve araştırma amaçlı yapılmıştır")
    mesgdcrt.SuccessMessage("Root-BomB, Root-B tarafından oluşturuldu")


def workernode(mode, cc, target, count, delay, max_threads):

    api = APIProvider(cc, target, mode, delay=delay)
    clr()
    mesgdcrt.SectionMessage("Bombacıyı donatıldı - Lütfen sabırlı olun")
    mesgdcrt.GeneralMessage(
        "Bombalama sırasında lütfen internete bağlı kalın")
    mesgdcrt.GeneralMessage("API Version   : " + api.api_version)
    mesgdcrt.GeneralMessage("Target        : " + cc + target)
    mesgdcrt.GeneralMessage("Amount        : " + str(count))
    mesgdcrt.GeneralMessage("Threads       : " + str(max_threads) + " threads")
    mesgdcrt.GeneralMessage("Delay         : " + str(delay) +
                            " seconds")
    mesgdcrt.WarningMessage(
        "Bu araç yalnızca eğlence ve araştırma amaçlı yapılmıştır")
    print()
    input(mesgdcrt.CommandMessage(
        "Bombacıyı askıya almak için [CTRL+Z]'ye veya devam ettirmek için [ENTER]'a basın."))

    if len(APIProvider.api_providers) == 0:
        mesgdcrt.FailureMessage("Ülkeniz/hedefiniz henüz desteklenmiyor")
        mesgdcrt.GeneralMessage("Bize ulaşmaktan çekinmeyin")
        input(mesgdcrt.CommandMessage("Çıkmak için [ENTER]'a basın"))
        bann_text()
        sys.exit()

    success, failed = 0, 0
    while success < count:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            jobs = []
            for i in range(count-success):
                jobs.append(executor.submit(api.hit))

            for job in as_completed(jobs):
                result = job.result()
                if result is None:
                    mesgdcrt.FailureMessage(
                        "Hedefiniz için bombalama sınırına ulaşıldı")
                    mesgdcrt.GeneralMessage("Daha sonra tekrar deneyin !!")
                    input(mesgdcrt.CommandMessage("Çıkmak için [ENTER]'a basın"))
                    bann_text()
                    sys.exit()
                if result:
                    success += 1
                else:
                    failed += 1
                clr()
                pretty_print(cc, target, success, failed)
    print("\n")
    mesgdcrt.SuccessMessage("Bombalama tamamlandı!")
    time.sleep(1.5)
    bann_text()
    sys.exit()


def selectnode(mode="sms"):
    mode = mode.lower().strip()
    try:
        clr()
        bann_text()
        check_intr()
        check_for_updates()
        notifyen()

        max_limit = {"sms": 500, "call": 15, "mail": 200}
        cc, target = "", ""
        if mode in ["sms", "call"]:
            cc, target = get_phone_info()
            if cc != "91":
                max_limit.update({"sms": 100})
        elif mode == "mail":
            target = get_mail_info()
        else:
            raise KeyboardInterrupt

        limit = max_limit[mode]
        while True:
            try:
                message = ("Sayısını girin {type}".format(type=mode.upper()) +
                           " Gönder (Max {limit}): ".format(limit=limit))
                count = int(input(mesgdcrt.CommandMessage(message)).strip())
                if count > limit or count == 0:
                    mesgdcrt.WarningMessage("Talepte bulundunuz " + str(count)
                                            + " {type}".format(
                                                type=mode.upper()))
                    mesgdcrt.GeneralMessage(
                        "Değeri otomatik olarak sınırlama"
                        " ile {limit}".format(limit=limit))
                    count = limit
                delay = float(input(
                    mesgdcrt.CommandMessage("Gecikme süresini girin (saniye cinsinden): "))
                    .strip())
                # delay = 0
                max_thread_limit = (count//10) if (count//10) > 0 else 1
                max_threads = int(input(
                    mesgdcrt.CommandMessage(
                        "Sayısını girin Konu (Önerilen): {max_limit}): "
                        .format(max_limit=max_thread_limit)))
                    .strip())
                max_threads = max_threads if (
                    max_threads > 0) else max_thread_limit
                if (count < 0 or delay < 0):
                    raise Exception
                break
            except KeyboardInterrupt as ki:
                raise ki
            except Exception:
                mesgdcrt.FailureMessage("Read Instructions Carefully !!!")
                print()

        workernode(mode, cc, target, count, delay, max_threads)
    except KeyboardInterrupt:
        mesgdcrt.WarningMessage("INTR araması alındı - Çıkılıyor...")
        sys.exit()


mesgdcrt = MessageDecorator("icon")
if sys.version_info[0] != 3:
    mesgdcrt.FailureMessage("Root-BomB yalnızca Python v3'te çalışacak")
    sys.exit()

try:
    country_codes = readisdc()["isdcodes"]
except FileNotFoundError:
    update()


__VERSION__ = get_version()
__CONTRIBUTORS__ = ['Root-B', 't0xic0der', 'scpketer', 'Stefan']

ALL_COLORS = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE,
              Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
RESET_ALL = Style.RESET_ALL

ASCII_MODE = False
DEBUG_MODE = False

description = """Root-BomB - Dostça Spam Yapan Uygulamanız

Root-BomB, aşağıdakileri içeren birçok amaç için kullanılabilir: -
\t Güvenlik açığı bulunan API'leri İnternet üzerinden açığa çıkarma
\t Dostane Spam
\t İstenmeyen Posta Dedektörünüzü ve daha fazlasını test etme ....

Root-BomB kötü amaçlı kullanımlar için tasarlanmamıştır.
"""

parser = argparse.ArgumentParser(description=description,
                                 epilog='Kodlayan Root-B !!!')
parser.add_argument("-sms", "--sms", action="store_true",
                    help="Root-BomB'u SMS Bomb moduyla başlat")
parser.add_argument("-call", "--call", action="store_true",
                    help="CALL Bomb moduyla Root-BomB'yi başlat")
parser.add_argument("-mail", "--mail", action="store_true",
                    help="MAIL Bomb moduyla Root-BomB'yi başlat")
parser.add_argument("-ascii", "--ascii", action="store_true",
                    help="sadece standart ASCII setinin karakterlerini göster")
parser.add_argument("-u", "--update", action="store_true",
                    help="Root-BomB'yi güncelle")
parser.add_argument("-c", "--contributors", action="store_true",
                    help="mevcut Root-BomB katkıda bulunanları göster")
parser.add_argument("-v", "--version", action="store_true",
                    help="geçerli Root-BomB sürümünü göster")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.ascii:
        ASCII_MODE = True
        mesgdcrt = MessageDecorator("stat")
    if args.version:
        print("Version: ", __VERSION__)
    elif args.contributors:
        print("Contributors: ", " ".join(__CONTRIBUTORS__))
    elif args.update:
        update()
    elif args.mail:
        selectnode(mode="mail")
    elif args.call:
        selectnode(mode="call")
    elif args.sms:
        selectnode(mode="sms")
    else:
        choice = ""
        avail_choice = {
            "1": "SMS",
            "2": "CALL",
            "3": "MAIL"
        }
        try:
            while (choice not in avail_choice):
                clr()
                bann_text()
                print("Available Options:\n")
                for key, value in avail_choice.items():
                    print("[ {key} ] {value} BOMB".format(key=key,
                                                          value=value))
                print()
                choice = input(mesgdcrt.CommandMessage("Seçimi Gir : "))
            selectnode(mode=avail_choice[choice].lower())
        except KeyboardInterrupt:
            mesgdcrt.WarningMessage("INTR araması alındı - Çıkılıyor...")
            sys.exit()
    sys.exit()
