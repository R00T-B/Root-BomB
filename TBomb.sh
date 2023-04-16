#!/bin/bash

detect_distro() {
    if [[ "$OSTYPE" == linux-android* ]]; then
            distro="termux"
    fi

    if [ -z "$distro" ]; then
        distro=$(ls /etc | awk 'match($0, "(.+?)[-_](?:release|version)", groups) {if(groups[1] != "os") {print groups[1]}}')
    fi

    if [ -z "$distro" ]; then
        if [ -f "/etc/os-release" ]; then
            distro="$(source /etc/os-release && echo $ID)"
        elif [ "$OSTYPE" == "darwin" ]; then
            distro="darwin"
        else 
            distro="invalid"
        fi
    fi
}

pause() {
    read -n1 -r -p "Devam etmek için herhangi bir tuşa basın..."
}
banner() {
    clear
    echo -e "\e[1;31m"
    if ! [ -x "$(command -v figlet)" ]; then
        echo 'Introducing TBomb'
    else
        figlet TBomb
    fi
    if ! [ -x "$(command -v toilet)" ]; then
        echo -e "\e[4;34m Bu Bombacı Tarafından Oluşturuldu \e[1;32mRoot-B \e[0m"
    else
        echo -e "\e[1;34mTarafından yaratıldı \e[1;34m"
        toilet -f mono12 -F border Root-B
    fi
    echo -e "\e[1;34m Sorularınız İçin Bana Katılın!!!\e[0m"
    echo -e "\e[1;32m           Telegram: https://t.me/TBombChat \e[0m"
    echo -e "\e[4;32m   YouTube: https://www.youtube.com/c/SpeedXTech \e[0m"
    echo " "
    echo "NOTE: Daha fazla kararlılık için lütfen TBomb'un PIP sürümüne geçin."
    echo " "
}

init_environ(){
    declare -A backends; backends=(
        ["arch"]="pacman -S --noconfirm"
        ["debian"]="apt-get -y install"
        ["ubuntu"]="apt -y install"
        ["termux"]="apt -y install"
        ["fedora"]="yum -y install"
        ["redhat"]="yum -y install"
        ["SuSE"]="zypper -n install"
        ["sles"]="zypper -n install"
        ["darwin"]="brew install"
        ["alpine"]="apk add"
    )

    INSTALL="${backends[$distro]}"

    if [ "$distro" == "termux" ]; then
        PYTHON="python"
        SUDO=""
    else
        PYTHON="python3"
        SUDO="sudo"
    fi
    PIP="$PYTHON -m pip"
}

install_deps(){
    
    packages=(openssl git $PYTHON $PYTHON-pip figlet toilet)
    if [ -n "$INSTALL" ];then
        for package in ${packages[@]}; do
            $SUDO $INSTALL $package
        done
        $PIP install -r requirements.txt
    else
        echo "Bağımlılıkları yükleyemedik."
        echo "Lütfen git, python3, pip3 ve gereksinimlerin yüklü olduğundan emin olun."
        echo "Ardından bomber.py dosyasını çalıştırabilirsiniz."
        exit
    fi
}

banner
pause
detect_distro
init_environ
if [ -f .update ];then
    echo "Tüm Gereksinimler Bulundu...."
else
    echo 'Yükleme Gereksinimleri...'
    echo .
    echo .
    install_deps
    echo Bu Komut Dosyası Root-B Tarafından Yapılmıştır > .update
    echo 'Gereksinimler Yüklendi....'
    pause
fi
while :
do
    banner
    echo -e "\e[4;31m Lütfen Talimatı Dikkatlice Okuyun !!! \e[0m"
    echo " "
    echo "Başlamak için 1'e basın SMS  Bomber "
    echo "Başlamak için 2'e basın CALL Bomber "
    echo "Başlamak için 3'e basın MAIL Bomber (Henüz uygun değil)"
    echo "için 4'e basın  Güncelleme (Linux ve Linux Emülatörlerinde Çalışır) "
    echo "için 5'e basın  Cıkıs "
    read ch
    clear
    if [ $ch -eq 1 ];then
        $PYTHON bomber.py --sms
        exit
    elif [ $ch -eq 2 ];then
        $PYTHON bomber.py --call
        exit
    elif [ $ch -eq 3 ];then
        $PYTHON bomber.py --mail
        exit
    elif [ $ch -eq 4 ];then
        echo -e "\e[1;34m Son Dosyalar İndiriliyor..."
        rm -f .update
        $PYTHON bomber.py --update
        echo -e "\e[1;34m RUN TBomb Again..."
        pause
        exit
    elif [ $ch -eq 5 ];then
        banner
        exit
    else
        echo -e "\e[4;32m Geçersiz Giriş !!! \e[0m"
        pause
    fi
done
