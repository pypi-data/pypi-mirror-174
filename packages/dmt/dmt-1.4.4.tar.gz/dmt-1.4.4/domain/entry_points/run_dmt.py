import os, sys
from domain.management.tools import main

I18N, L10N = (x for x in os.environ.get('LANG', "en_EN.UTF-8").split(".")[0].split("_"))

def run():
    import argparse
    parser = argparse.ArgumentParser(description="Domain Management Tool")

    parser.add_argument('-v', '--version', action='store_true', help="output version information and exit")
    parser.add_argument('-l', '--list', action="store_true", help="list installed domains")
    parser.add_argument('-c', '--create', action="store_true", help="Create a new domain from template")
    parser.add_argument('-a', '--add', type=str, help="git repository hosting a domain to add", required=False)
    parser.add_argument('-s', '--sync', action="store_true", help="Synchronize all installed domains")
    parser.add_argument('-V', '--validate', action="store_true", help="Validate all installed domains")
    parser.add_argument('-T', '--train', action="store_true", help="Train new model from all installed domains")
    parser.add_argument('-S', '--serve', action="store_true", help="Serve the lastest model")
    parser.add_argument('-L', '--lang', type=str, help=f"language to work with (defaults to your system preference: {I18N})", default=I18N)

    ARGS = parser.parse_args()
    try:
        sys.exit(main(ARGS))
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == '__main__':
    run()