import os

def enable_service_now():
    if not os.path.isfile("/etc/systemd/system/dmt.service"):
        os.system("sudo wget https://gitlab.com/waser-technologies/technologies/dmt/-/raw/main/dmt.service.example && sudo mv dmt.service.example /etc/systemd/system/dmt.service")
    os.system("systemctl enable --now dmt.service")