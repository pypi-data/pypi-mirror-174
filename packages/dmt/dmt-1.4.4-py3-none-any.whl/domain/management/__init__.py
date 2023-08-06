import os

def enable_service_now():
    if not os.path.isfile("/usr/lib/systemd/user/dmt.service"):
        os.system("sudo wget https://gitlab.com/waser-technologies/technologies/dmt/-/raw/main/dmt.service.example && sudo mv dmt.service.example /usr/lib/systemd/user/dmt.service")
    os.system("systemctl --user enable --now dmt.service")