from crypt import crypt
from fabric.api import local, settings, abort, run, env, sudo, put, get, prefix
# from fabric import Connection, Config, task
# import getpass

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from config import PI_PASSWORD

# env.hosts = ["%s:%s" % ("raspberrypi.local", 22)]
env.hosts = ["%s:%s" % ("10.0.0.4", 22)]
env.user = "lush"
env.password = PI_PASSWORD

# HOST = "192.168.1.101"
# PORT = 22
# USER = "pi"

# sudo_pass = getpass.getpass("What's your sudo password?")
# configuration = Config(overrides={'sudo': {'password': sudo_pass}})
# c = Connection(host=HOST, user=USER, port=PORT, config=configuration)
# c = Connection(host=HOST, user=USER, port=PORT)

# BOOTSTRAP_VERSION = "0.0.1"
# PYTHON_VERSION = "0.0.2"
# TEST_VERSION = "0.0.1"
# DESKCONTROL_VERSION = "0.0.6"
# BRICKD_VERSION = "0.0.1"
# COMMAND_VERSION = "0.0.4"

# Raspbian supporting KeDei touch screen
# http://www.kedei.net/raspberry/v6_1/rpi_35_v6_3_stretch_kernel_4_15_18.rar
RASPBIAN_VERSION = "KeDei Raspbian rpi_v6_3_stretch_kernel_4_15_18"

############################################################################
##              Preparing the base disc image from JESSIE_VERSION
############################################################################

"""
    On local machine install fabric3
    pip3 install fabric3
    Steps to set up the Raspberry Pi:
    Login to Raspberry Pi
    "sudo su"
    'wpa_passphrase "WiFiSSID" "WiFiPassword" >> /etc/wpa_supplicant/wpa_supplicant.conf'
    "wpa_cli reconfigure"
    "raspi-config"
    Interfacing Options > SSH > Yes
    reboot
"""

def prepare_card():
    uninstall_packages()
    apt_autoremove()
    apt_update()
    apt_upgrade()
    apt_autoremove()
    apt_clean()
    # install_openhab()
    # change_password()
    # _change_graphics_memory()
    # install_docker()
    # docker_login(password)
    # add_bootstrap()
    # _reduce_logging()
    # reduced_writes()
    # add_resize()
    # sudo("reboot")

def apt_update():
    sudo('apt update')

def apt_upgrade():
    sudo('apt upgrade')

def apt_autoremove():
    sudo('apt autoremove')

def apt_clean():
    sudo('df -h')
    sudo('apt clean')
    sudo('df -h')

def uninstall_packages():
    sudo('df -h')
    sudo('apt remove wolfram*')
    sudo('apt remove scratch*')
    sudo('apt remove libreoffice*')
    sudo('apt remove minecraft*')
    sudo('df -h')

def reboot():
    print('System reboot')
    sudo('reboot')

def halt():
    print('System halt')
    sudo('halt')

def kedei_install_SPI_touchscreen_drivers():
    pass
    # kedei_download_touchscreen_drivers()
    # kedei_untar_touchscreen_drivers()
    # kedei_backup_old_kernel()
    # kedei_install_new_kernel()
    # reboot()

def kedei_download_touchscreen_drivers():
    print('Downloading KeDei touchscreen drivers. This operation may take a very long time')
    # sudo('mkdir /opt/kedei')
    sudo('[ ! -d "/opt/kedei" ] && mkdir /opt/kedei')
    sudo('cd /opt/kedei ; wget http://www.kedei.net/raspberry/v6_1/LCD_show_v6_1_3.tar.gz')
    sudo('pwd')

def kedei_untar_touchscreen_drivers():
    sudo('[ ! -d "/opt/kedei" ] && mkdir /opt/kedei')
    sudo('cd /opt/kedei ; tar zxvf LCD_show_v6_1_3.tar.gz')

def kedei_backup_old_kernel():
    print('Backing up old kernel')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v /boot/kernel.img  ./backup/kernel.img')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v /boot/kernel7.img ./backup/kernel7.img')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v /boot/*.dtb ./backup/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v /boot/overlays/*.dtb* ./backup/overlays/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v -rf  /lib/firmware    ./backup/lib/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v -rf  /lib/modules    ./backup/lib')
    print('Backing up old kernel completed')

def kedei_install_new_kernel():
    print('Installing new kernel for Kedei touchscreen driver')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./lcd_35_v/kernel.img /boot/kernel.img')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./lcd_35_v/kernel7.img /boot/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./lcd_35_v/*.dtb /boot/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./lcd_35_v/overlays/*.dtb* /boot/overlays/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v -rf ./lcd_35_v/lib/* /lib/')
    sudo('apt-mark hold raspberrypi-kernel')
    print('Installing new kernel for Kedei touchscreen driver completed')

def kedei_restore_old_kernel():
    print('Restoring old kernel')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./backup/kernel.img /boot/kernel.img')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./backup/kernel7.img /boot/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./backup/*.dtb /boot/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./backup/overlays/*.dtb* /boot/overlays/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v -rf ./backup/lib/* /lib/')
    print('Restoring old kernel completed')

def kedei_restore_hdmi_kernel():
    print('Restoring kernel with HDMI output')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./hdmi/kernel.img /boot/kernel.img')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./hdmi/kernel7.img /boot/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./hdmi/*.dtb /boot/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v ./hdmi/overlays/*.dtb* /boot/overlays/')
    sudo('cd /opt/kedei/LCD_show_v6_1_3 ; cp -v -rf ./hdmi/lib/* /lib/')
    print('Restoring kernel with HDMI output completed')

def install_software_apt_prerequisites():
    print('Installing software APT prerequisites')
    sudo('apt-get -y remove python-pip python3-pip ; apt-get -y install python-pip python3-pip')
    sudo('apt-get -y install python-requests python-pygame')
    sudo('apt-get -y install ntp ifmetric p7zip-full man apt-utils expect wget git libfreetype6 dbus dbus-*dev ')
    sudo('apt-get -y install libsmbclient libssh-4 libpcre3 fonts-freefont-ttf espeak alsa-tools alsa-utils')
    sudo('apt-get -y install python3-gpiozero python-rpi.gpio python-pigpio python-gpiozero')
    sudo('apt-get -y install pigpio python3-pigpio python3-rpi.gpio raspi-gpio wiringpi')
    sudo('apt-get -y install fbset fbi')
    sudo('apt-get -y install omxplayer ola ola-python')
    sudo('apt-get -y install build-essential python3-dev')
    print('Installing software APT prerequisites completed')

def install_software_pip_prerequisites():
    print('Installing software PIP prerequisites')
    # sudo('apt-get -y remove python-pip python3-pip ; apt-get -y install python-pip python3-pip')
    # sudo('pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pygameui') # not working
    sudo('pip install evdev')
    sudo('pip install tinkerforge')
    sudo('pip install numpy')
    sudo('pip install pysrt')
    sudo('pip install phue')
    # sudo('pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org  pygameui') # not working
    sudo('pip3 install evdev')
    sudo('pip3 install tinkerforge')
    sudo('pip3 install numpy')
    sudo('pip3 install pysrt')
    sudo('pip3 install phue')
    sudo('pip3 install dbus-python')
    sudo('pip3 install flask')
    sudo('pip3 install -U flask-cors')
    sudo('pip3 install Flask-RESTful')
    sudo('pip3 install Flask-Jsonpify')
    sudo('pip3 install flask-inputs')
    sudo('pip3 install omxplayer-wrapper')
    print('Installing software PIP prerequisites completed')

def install_pygameui():
    print('Installing pygameui')
    # sudo('rm -rf /opt/pygameui')
    # sudo('mkdir /opt/pygameui')
    sudo('[ ! -d "/opt/pygameui" ] && mkdir /opt/pygameui')
    sudo('cd /opt/pygameui ; git clone https://github.com/fictorial/pygameui.git /opt/pygameui')
    sudo('cd /opt/pygameui ; python setup.py install')
    print('Installing pygameui completed')

def install_rclone():
    print('Installing rclone')
    # sudo('rm -rf /opt/rclone')
    # sudo('mkdir /opt/rclone')
    sudo('[ ! -d "/opt/rclone" ] && mkdir /opt/rclone')
    sudo('cd /opt/rclone ; wget https://raw.github.com/pageauc/rclone4pi/master/rclone-install.sh')
    sudo('cd /opt/rclone ; ./rclone-install.sh')
    sudo('rclone --version')
    print('Installing rclone clompleted')


def create_lushroom_dev():
    print('Creating LushRoom development environment')
    sudo('mkdir /opt/lushroom')
    sudo('mkdir /opt/lushroom/lrpi_base')
    sudo('mkdir /opt/lushroom/lrpi_bootstrap')
    sudo('mkdir /opt/lushroom/lrpi_commands')
    sudo('mkdir /opt/lushroom/lrpi_rclone')
    sudo('mkdir /opt/lushroom/lrpi_player')
    # sudo('mkdir /opt/lushroom/lrpi_recorder')
    sudo('mkdir /opt/lushroom/lrpi_tablet_ui')
    sudo('git clone --single-branch -b develop https://github.com/LUSHDigital/lrpi_base.git /opt/lushroom/lrpi_base')
    sudo('git clone --single-branch -b develop https://github.com/LUSHDigital/lrpi_bootstrap.git /opt/lushroom/lrpi_bootstrap')
    sudo('git clone --single-branch -b develop https://github.com/LUSHDigital/lrpi_commands.git /opt/lushroom/lrpi_commands')
    sudo('git clone --single-branch -b develop https://github.com/LUSHDigital/lrpi_rclone.git /opt/lushroom/lrpi_rclone')
    sudo('git clone --single-branch -b develop https://github.com/LUSHDigital/lrpi_player.git /opt/lushroom/lrpi_player')
    # sudo('git clone --single-branch -b develop https://github.com/LUSHDigital/lrpi_recorder.git /opt/lushroom/lrpi_recorder')
    sudo('git clone --single-branch -b develop https://github.com/LUSHDigital/lrpi_tablet_ui.git /opt/lushroom/lrpi_tablet_ui')
    print('Creating LushRoom development environment completed')


def install_openhab():
    sudo('apt install screen mc vim git htop')
    sudo('wget -qO - "https://bintray.com/user/downloadSubjectPublicKey?username=openhab" | apt-key add')
    sudo('apt-get install apt-transport-https')
    sudo('echo "deb https://dl.bintray.com/openhab/apt-repo2 stable main" | tee /etc/apt/sources.list.d/openhab2.list')
    sudo('apt-get update')
    sudo('apt-get install openhab2')
    sudo('apt-get install openhab2-addons')
    sudo('systemctl start openhab2.service')
    sudo('systemctl status openhab2.service')
    sudo('systemctl daemon-reload')
    sudo('systemctl enable openhab2.service')

def reduced_writes():

    # a set of optimisations from
    # http://www.zdnet.com/article/raspberry-pi-extending-the-life-of-the-sd-card/
    # and
    # https://narcisocerezo.wordpress.com/2014/06/25/create-a-robust-raspberry-pi-setup-for-24x7-operation/

    # minimise writes
    use_ram_partitions()
    _stop_fsck_running()
    _redirect_logrotate_state()
    _dont_update_fake_hwclock()
    _dont_do_man_indexing()
    # _remove_swap()

def use_ram_partitions():
    sudo('echo "tmpfs    /tmp    tmpfs    defaults,noatime,nosuid,size=100m    0 0" >> /etc/fstab')
    sudo('echo "tmpfs    /var/tmp    tmpfs    defaults,noatime,nosuid,size=30m    0 0" >> /etc/fstab')
    sudo('echo "tmpfs    /var/log    tmpfs    defaults,noatime,nosuid,mode=0755,size=100m    0" >> /etc/fstab')

def _redirect_logrotate_state():
    sudo("rm /etc/cron.daily/logrotate")
    put("logrotate", "/etc/cron.daily/logrotate", use_sudo=True)
    sudo("chmod 755 /etc/cron.daily/logrotate")
    sudo("chown root /etc/cron.daily/logrotate")
    sudo("chgrp root /etc/cron.daily/logrotate")

def _stop_fsck_running():
    sudo("tune2fs -c -1 -i 0 /dev/mmcblk0p2")

def _dont_update_fake_hwclock():
    sudo("rm /etc/cron.hourly/fake-hwclock")

def _dont_do_man_indexing():
    sudo("rm  /etc/cron.weekly/man-db")
    sudo("rm  /etc/cron.daily/man-db")

def _remove_swap():
    # not needed on Hypriot OS
    sudo("update-rc.d -f dphys-swapfile remove")
    sudo("swapoff /var/swap")
    sudo("rm /var/swap")

def _reduce_logging():
    ## add our own rsyslog.conf
    sudo("rm /etc/rsyslog.conf")
    put("rsyslog.conf", "/etc/rsyslog.conf", use_sudo=True)
    sudo("chmod 755 /etc/rsyslog.conf")
    sudo("chown root /etc/rsyslog.conf")
    sudo("chgrp root /etc/rsyslog.conf")

"""
def change_password():
    env.password = "raspberry"
    crypted_password = crypt(PI_PASSWORD, 'salt')
    sudo('usermod --password %s %s' % (crypted_password, env.user), pty=False)

def _change_graphics_memory():
    sudo('echo "gpu_mem=16" >> /boot/config.txt')

def add_bootstrap():
    # # build_bootstrap()
    # sudo("mkdir -p /opt/augment00")
    # put("start.sh", "/opt/augment00/start.sh", use_sudo=True)
    # sudo("chmod 755 /opt/augment00/start.sh")

    put("wifi.py", "/opt/augment00/wifi.py", use_sudo=True)
    sudo("chmod 755 /opt/augment00/wifi.py")

    # ## add our own rc.local
    # sudo("rm /etc/rc.local")
    # put("rc.local", "/etc/rc.local", use_sudo=True)
    # sudo("chmod 755 /etc/rc.local")
    # sudo("chown root /etc/rc.local")
    # sudo("chgrp root /etc/rc.local")


def add_resize():
    sudo('printf " quiet init=/usr/lib/raspi-config/init_resize.sh" >> /boot/cmdline.txt')
    put("resize2fs_once", "/etc/init.d/resize2fs_once", use_sudo=True)
    sudo("chmod +x /etc/init.d/resize2fs_once")
    sudo("chown root /etc/init.d/resize2fs_once")
    sudo("chgrp root /etc/init.d/resize2fs_once")
    sudo("systemctl enable resize2fs_once")

def build_bootstrap():
    tag = BOOTSTRAP_VERSION
    put("docker", "~")
    sudo('docker build --no-cache=true -t="augment00/augment00-bootstrap:%s" '
         'docker/augment00-bootstrap' % tag)
    sudo('docker tag augment00/augment00-bootstrap:%s augment00/'
         'augment00-bootstrap:latest' % tag)
    sudo('docker push augment00/augment00-bootstrap:latest')

def install_docker():
    # install docker
    run("curl -sSL get.docker.com | sh")
    # sets up service
    run("sudo systemctl enable docker")
    # allows pi use to use docker
    run("sudo usermod -aG docker pi")
    # installs cocker compose
    sudo("curl --silent --show-error --retry 5 https://bootstrap.pypa.io/"
         "get-pip.py | sudo python2.7")
    sudo("pip install docker-compose")


############################################################################
##              Docker commands for building other images                       ##
############################################################################


def docker_login(password):
    sudo('docker login -u augment00 -p "%s"' % password)


def push_bootstrap():
    sudo('docker push augment00/augment00-bootstrap:latest')


def build_python():
    tag = PYTHON_VERSION
    put("docker", "~")
    sudo('docker build --no-cache=true -t="augment00/augment00-python:%s" docker/augment00-python' % tag)
    sudo('docker push augment00/augment00-python:%s' % tag)
    sudo('docker tag augment00/augment00-python:%s augment00/augment00-python:latest' % tag)
    sudo('docker push augment00/augment00-python:latest')


def build_deskcontrol():
    tag = DESKCONTROL_VERSION
    put("docker", "~")
    sudo('docker build --no-cache=true -t="augment00/augment00-deskcontrol:%s" docker/augment00-deskcontrol' % tag)
    sudo('docker push augment00/augment00-deskcontrol:%s' % tag)
    sudo('docker tag augment00/augment00-deskcontrol:%s augment00/augment00-deskcontrol:latest' % tag)
    sudo('docker push augment00/augment00-deskcontrol:latest')


def build_command():
    tag = COMMAND_VERSION
    put("docker", "~")
    sudo('docker build --no-cache=true -t="augment00/augment00-command:%s" docker/augment00-command2' % tag)
    sudo('docker push augment00/augment00-command:%s' % tag)
    sudo('docker tag augment00/augment00-command:%s augment00/augment00-command:latest' % tag)
    sudo('docker push augment00/augment00-command:latest')


def build_brickd():
    tag = BRICKD_VERSION
    put("docker", "~")
    sudo('docker build --no-cache=true -t="augment00/augment00-brickd:%s" docker/augment00-brickd' % tag)
    sudo('docker push augment00/augment00-brickd:%s' % tag)
    sudo('docker tag augment00/augment00-brickd:%s augment00/augment00-brickd:latest' % tag)
    sudo('docker push augment00/augment00-brickd:latest')

def test():
    put("test.txt", "~")

def get_file():
    get("/etc/cron.daily/logrotate")
"""
