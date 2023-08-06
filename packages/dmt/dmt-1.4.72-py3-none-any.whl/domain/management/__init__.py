import os

def enable_service_now():
    if not os.path.isfile("/usr/lib/systemd/system/dmt.service"):
        os.system("sudo wget https://gitlab.com/waser-technologies/technologies/dmt/-/raw/main/dmt.service.example && sudo mv dmt.service.example /usr/lib/systemd/system/dmt.service")
    os.system("sudo systemctl enable --now dmt.service")