import os

def enable_service_now():
    if not os.path.isfile("/usr/lib/systemd/user/listen.service"):
        os.system("sudo wget https://gitlab.com/waser-technologies/technologies/listen/-/raw/main/listen.service.example && sudo mv listen.service.example /usr/lib/systemd/user/listen.service")
    os.system("systemctl --user enable --now listen.service")