#!/usr/bin/python3.8

import os, sys
import shutil
import glob
import yaml
import subprocess
import requests
from multiprocessing import Process
from tqdm import tqdm

from pathlib import Path
from halo import Halo

from domain import __version__


USERNAME = os.environ.get("USERNAME", 'root')
ASSISTANT_PATH = f"/home/{USERNAME}/.assistant" if USERNAME != "root" else "/usr/share/assistant"

I18N, L10N = (x for x in os.environ.get('LANG', "en_EN.UTF-8").split(".")[0].split("_"))

REPO_PROTOCOL = "https"
REPO_HOST = "gitlab.com"
REPO_BASE_GROUP = "waser-technologies"
REPO_BASE_URL = f"{REPO_PROTOCOL}://{REPO_HOST}/{REPO_BASE_GROUP}"
REPO_DOMAINS = f"{REPO_BASE_URL}/data/nlu" # Where are the domains located
REPO_BASE_DOMAIN_NAME = "smalltalk" # Single base domain name across languages
REPO_MODELS = f"{REPO_BASE_URL}/models" # Where are pre-trained models located
REPO_BASE_MODELS_NAME = "nlu" # Single base models name across languages
REPO_COOKIECUTTERS = "https://gitlab.com/waser-technologies/cookiecutters" # Where are cookiecutter templates located
REPO_BASE_COOKIECUTTER_NAME = "nlu-domain-template" # Single base template name across languages
REPO_BASE_COOKIECUTTER_URL = f"{REPO_COOKIECUTTERS}/{REPO_BASE_COOKIECUTTER_NAME}"

def _pp(text: str) -> str:
    _s = f"\t[\t{text}\t]\t"
    print(_s)
    return _s

def read_yaml(yaml_filepath):
    with open(yaml_filepath, 'r') as yf:
        yml = yaml.load(yf, Loader=yaml.SafeLoader)
        yf.close()
        return yml
    return None

def get_domain_metadata(domain):
    return domain.get('metadata')

def get_list_installed_domains(domains_path: str):
    domain_files = glob.glob(domains_path + "/*.yml")
    list_installed_domains = []
    for d in domain_files:
        domain = read_yaml(d)
        domain_metadata = get_domain_metadata(domain)
        list_installed_domains.append(domain_metadata)
    return list_installed_domains

def mktemp(name: str):
    tmp_path = "/tmp"
    tmp_dir_path = f"{tmp_path}/{name}"
    Path(tmp_dir_path).mkdir(parents=True, exist_ok=True)
    return tmp_dir_path

def git_clone(repository_url, working_dir):
    clone = f"git clone '{repository_url}' '{working_dir}'"
    os.system(clone)
    return

def rmdir(remove_path):
    shutil.rmtree(remove_path)

def copy_actions(tmp_domain, domain_path, domain_slug, domain_lang):
    try:
        shutil.copytree(f"{tmp_domain}/actions", f"{domain_path}/actions/{domain_lang}/{domain_slug}", dirs_exist_ok=True)
        if not Path(f"{domain_path}/actions/{domain_lang}/__init__.py").exists():
            os.mknod(f"{domain_path}/actions/{domain_lang}/__init__.py")
        return 1
    except FileNotFoundError:
        return 0

def copy_forms(tmp_domain, domain_path, domain_slug, domain_lang):
    try:
        shutil.copytree(f"{tmp_domain}/data/forms", f"{domain_path}/data/{domain_lang}/NLU/forms/{domain_slug}", dirs_exist_ok=True)
        return 1
    except FileNotFoundError:
        return 0
    
def copy_stories(tmp_domain, domain_path, domain_slug, domain_lang):
    try:
        shutil.copytree(f"{tmp_domain}/data/stories", f"{domain_path}/data/{domain_lang}/NLU/stories/{domain_slug}", dirs_exist_ok=True)
        return 1
    except FileNotFoundError:
        return 0
 
def copy_nlu(tmp_domain, domain_path, domain_slug, domain_lang):
    try:
        shutil.copytree(f"{tmp_domain}/data/nlu", f"{domain_path}/data/{domain_lang}/NLU/nlu/{domain_slug}", dirs_exist_ok=True)
        return 1
    except FileNotFoundError:
        return 0
 
def copy_rules(tmp_domain, domain_path, domain_slug, domain_lang):
    try:
        shutil.copytree(f"{tmp_domain}/data/rules", f"{domain_path}/data/{domain_lang}/NLU/rules/{domain_slug}", dirs_exist_ok=True)
        return 1
    except FileNotFoundError:
        return 0
 
def copy_responses(tmp_domain, domain_path, domain_slug, domain_lang):
    try:
        shutil.copytree(f"{tmp_domain}/data/responses", f"{domain_path}/data/{domain_lang}/NLU/responses/{domain_slug}", dirs_exist_ok=True)
        return 1
    except FileNotFoundError:
        return 0
 
def copy_tests(tmp_domain, domain_path, domain_slug, domain_lang):
    try:
        shutil.copytree(f"{tmp_domain}/tests", f"{domain_path}/tests/{domain_lang}/{domain_slug}", dirs_exist_ok=True)
        return 1
    except FileNotFoundError:
        return 0
 
def copy_domain(tmp_domain, domain_path, domain_slug, domain_lang):
    Path(f'{domain_path}/domains/{domain_lang}').mkdir(parents=True, exist_ok=True)
    try:
        shutil.copyfile(f"{tmp_domain}/domain.yml", f"{domain_path}/domains/{domain_lang}/{domain_slug}.yml")
        return 1
    except FileNotFoundError:
        return 0

def copy_models(tmp_models, models_path, models_lang):
    try:
        shutil.copytree(f"{tmp_models}/models", f"{models_path}/{models_lang}/NLU")
        return 1
    except FileExistsError:
        shutil.copyfile(f"{tmp_models}/models/*.tar.gz", f"{models_path}/{models_lang}/NLU")
    except FileNotFoundError:
        return 0

def copy_config(tmp_config, config_path, config_lang):
    config_dest = f"{config_path}/configs/{config_lang}/config.yml"
    if not Path(config_dest).exists():
        print(f"No config found @{config_dest}. Trying to create it.")
        Path(f"{config_path}/configs/{config_lang}").mkdir(parents=True, exist_ok=True)
        try:
            shutil.copyfile(f"{tmp_config}/config.yml", config_dest)
            return 1
        except FileNotFoundError:
            print(f"Couldn't find {tmp_config}/config.yml")
            raise FileNotFoundError(f"{tmp_config}/config.yml")
            return 0
    else:
        print(f"Found config @{config_dest}.")
        return 1

def mk_models_dir(models_path):
    Path(models_path).mkdir(parents=True, exist_ok=True)

def mk_assistant_dir(assistant_path):
    domains_path = f"{ASSISTANT_PATH}/domains/{I18N}"
    actions_path = f"{ASSISTANT_PATH}/actions/{I18N}"
    actions_init_modules = [
        f"{ASSISTANT_PATH}/actions/__init__.py",
        f"{ASSISTANT_PATH}/actions/{I18N}/__init__.py"
    ]
    #configs_path = f"{ASSISTANT_PATH}/configs/{I18N}"
    data_path = f"{ASSISTANT_PATH}/data/{I18N}/NLU"
    forms_path = f"{data_path}/forms"
    stories_path = f"{data_path}/stories"
    nlu_path = f"{data_path}/nlu"
    responses_path = f"{data_path}/responses"
    rules_path = f"{data_path}/rules"
    tests_path = f"{ASSISTANT_PATH}/tests/{I18N}"
    Path(actions_path).mkdir(parents=True, exist_ok=True)
    for module in actions_init_modules:
        if not Path(module).exists():
            os.mknod(module)
    #Path(configs_path).mkdir(parents=True, exist_ok=True)
    Path(data_path).mkdir(parents=True, exist_ok=True)
    #Path(forms_path).mkdir(parents=True, exist_ok=True)
    Path(stories_path).mkdir(parents=True, exist_ok=True)
    Path(nlu_path).mkdir(parents=True, exist_ok=True)
    Path(responses_path).mkdir(parents=True, exist_ok=True)
    Path(rules_path).mkdir(parents=True, exist_ok=True)
    Path(tests_path).mkdir(parents=True, exist_ok=True)
    Path(domains_path).mkdir(parents=True, exist_ok=True)

def install_domain(tmp_domain, domain_path):
    mk_assistant_dir(domain_path)
    domain = read_yaml(f"{tmp_domain}/domain.yml")
    domain_metadata = get_domain_metadata(domain)
    domain_name = domain_metadata.get('name', 'Unamed domain')
    domain_lang = domain_metadata.get('lang', 'en')
    _pp(f"Installing {domain_name} for {domain_lang.upper()}")
    copy_actions(tmp_domain, domain_path, domain_name, domain_lang)
    #copy_forms(tmp_domain, domain_path, domain_name)
    copy_stories(tmp_domain, domain_path, domain_name, domain_lang)
    copy_nlu(tmp_domain, domain_path, domain_name, domain_lang)
    copy_rules(tmp_domain, domain_path, domain_name, domain_lang)
    copy_responses(tmp_domain, domain_path, domain_name, domain_lang)
    copy_tests(tmp_domain, domain_path, domain_name, domain_lang)
    copy_config(tmp_domain, domain_path, domain_lang)
    dc = copy_domain(tmp_domain, domain_path, domain_name, domain_lang)
    if dc < 1:
        raise Exception("Unable to copy domain file.")
    rmdir(tmp_domain)
    return domain_metadata

def install_pretrained_models(tmp_models, models_path, models_lang):
    #mk_models_dir(models_path)
    _pp(f"Installing model from {tmp_models} to {models_path}.")
    copy_models(tmp_models, f"{models_path}/models", models_lang)
    copy_config(tmp_models, models_path, models_lang)
    rmdir(tmp_models)
    print("If this model contains custom actions responses, you need to serve them manually.")
    return models_path

def validate_data(data_path, data=None, domains=None, config=None):
    rasa = shutil.which('rasa')
    if rasa:
        stdout_path = f"{data_path}/validation.stdout.txt"
        stdOut = open(stdout_path, 'w+')
        
        cmd = [
            "rasa",
            "data",
            "validate",
            "--data" if data else "",
            f"{data}" if data else "",
            "-d" if domains else "",
            f"{domains}" if domains else "",
            "-c" if config else "",
            f"{config}" if config else "",
            "--quiet"
        ]
        p = subprocess.Popen(cmd, stdin=stdOut, stdout=stdOut, cwd=data_path, universal_newlines=True)
        output, errors = p.communicate()
        stdOut.close()
        print(f"See logs @{data_path}/validation.*.txt")
    else:
        print("Cannot validate the data without RASA installed inside the $PATH.")
        print("$\tpip install -U rasa")
    return

def train_lm(data_path, data=None, domains=None, config=None, models=None):
    rasa = shutil.which('rasa')
    if rasa:
        stdout_path = f"{data_path}/training.stdout.txt"
        stdOut = open(stdout_path, 'w+')
        cmd = [
            "rasa",
            "train",
            "--data" if data else "",
            f"{data}" if data else "",
            "-d" if domains else "",
            f"{domains}" if domains else "",
            "-c" if config else "",
            f"{config}" if config else "",
            "--out" if models else "",
            f"{models}" if models else "",
            "--quiet"
        ]
        p = subprocess.Popen(cmd, stdin=stdOut, stdout=stdOut, cwd=data_path, universal_newlines=True)
        output, errors = p.communicate()
        stdOut.close()
        print(f"See logs @{data_path}/training.*.txt")
    else:
        print("Cannot train the language model without RASA installed inside the $PATH.")
        print("$\tpip install -U rasa")
    return

def add_evaluate_domain_and_train_models(domain_repo):
    tmp_domain = mktemp(f"dmt") + "/add_domain"
    _pp("Cloning Domain")
    git_clone(domain_repo, tmp_domain)
    # Install domain
    _pp("Installing Domain")
    domain = install_domain(tmp_domain, ASSISTANT_PATH)
    domain_lang = domain.get('lang', 'en')
    rmdir(tmp_domain)
    validate_data(ASSISTANT_PATH, domains=f"domains/{domain_lang}", data=f"data/{domain_lang}", config=f"configs/{domain_lang}/config.yml")
    train_lm(ASSISTANT_PATH, domains=f"domains/{domain_lang}", data=f"data/{domain_lang}", config=f"configs/{domain_lang}/config.yml", models=f"models/{domain_lang}/NLU")
    print(f"Use `dmt -S -L {domain_lang}` to serve this model.")
    return f"models/{domain_lang}/NLU"

def serve_lm(data_path, models, endpoints, credentials):
    rasa = shutil.which('rasa')
    if rasa:
        cmd = [
            rasa,
            "run",
            "-m",
            f"{models}",
            "--enable-api",
            "--endpoints",
            f"{endpoints}",
            "--credentials",
            f"{credentials}"
        ]
        p = subprocess.Popen(cmd, cwd=data_path, universal_newlines=True)
        output, errors = p.communicate()
    else:
        print("Cannot serve language model without RASA installed inside the $PATH.")
        print("$\tpip install -U rasa")
    return

def serve_actions(data_path, module_name):
    rasa = shutil.which('rasa')
    if rasa:
        cmd = [
            "rasa",
            "run",
            f"{module_name}"
        ]
        p = subprocess.Popen(cmd, cwd=data_path, universal_newlines=True)
        output, errors = p.communicate()
    else:
        print("Cannot serve action without the RASA Action Server installed inside the $PATH.")
        print("$\tpip install -U rasa rasa-sdk")
    return

def ping(link):
	try:
		#Get Url
		get = requests.get(link)
		# if the request succeeds 
		if get.status_code == 200:
			return True
		else:
			return False
	except requests.exceptions.RequestException:
		return False

def models_as_service(data_path=ASSISTANT_PATH, models=f"models/{I18N}/NLU", endpoints="endpoints.yml", credentials="credentials.yml", module_name="actions", lang=I18N):
    """
    Loads the NLP models and sets up actions.
    """
    # Check models exists

    try:
        assert models == f"models/{lang}/NLU"
    except Exception:
        raise RuntimeError(f"`{models}` is not `models/{lang}/NLU`")

    if not Path(f"{data_path}/{models}").exists() or not glob.glob(f"{data_path}/{models}/*.tar.gz"):
    ##  if not:
    ##  Check if any model is installed
        gm = glob.glob(f"models/{lang}/NLU/*.tar.gz")
        if not gm:
    ###     if not:
    ###     Checks if lang has pre-trained model
            if not ping(f"{REPO_MODELS}/{lang}/{REPO_BASE_MODELS_NAME}"):
    ####        if not:
    ####        Checks if smalltalk domain is avalible for lang
                if not ping(f"{REPO_DOMAINS}/{lang}/{REPO_BASE_DOMAIN_NAME}"):
    #####           if not:
    #####           Sets lang to english
                    models="models/en/NLU"
                    lang="en"
    #####           Checks if english has pre-trained models
                    if not ping(f"{REPO_MODELS}/en/{REPO_BASE_MODELS_NAME}"):
    ######              if not:
    ######              Check if smalltalk is avalible in english
                        if not ping(f"{REPO_DOMAINS}/en/{REPO_BASE_DOMAIN_NAME}"):
    #######                 if not:
    #######                 Raises NotImplementedError
                            raise NotImplementedError(f"Languages: [{lang}, en]; not found")
                        else:
                            print("No english models found but SmallTalk exists.")
                            print("Using domain SmallTalk to build a model for EN.")
                            # Add and evaluate SmallTalk and train a new model for english
                            add_evaluate_domain_and_train_models(f"{REPO_DOMAINS}/en/{REPO_BASE_DOMAIN_NAME}.git")
                    else:
                        print(f"No domain for {lang} found.")
                        print("Using english as backup language.")
                        print("Found pre-trained models for EN.")
                        # download and install pre-trained models for english
                        # Clone models
                        tmp_models = mktemp(f"dmt") + "/add_models"
                        _pp("Cloning Models")
                        git_clone(f"{REPO_MODELS}/en/{REPO_BASE_MODELS_NAME}.git", tmp_models)
                        # Install models
                        _pp("Installing Models")
                        install_pretrained_models(tmp_models, ASSISTANT_PATH, "en")
                else:
                    print(f"No models for {lang} but SmallTalk exists.")
                    print(f"Using domain SmallTalk to build a model for {lang.upper()}.")
                    # Add and evaluate SmallTalk and train a new model for {I18N}
                    add_evaluate_domain_and_train_models(f"{REPO_DOMAINS}/{lang}/{REPO_BASE_DOMAIN_NAME}.git")
            else:
                print(f"Found pre-trained models for {lang.upper()}.")
                # download and install pre-trained models for {I18N}
                # Clone models
                tmp_models = mktemp(f"dmt") + "/add_models"
                _pp("Cloning Models")
                git_clone(f"{REPO_MODELS}/{lang}/{REPO_BASE_MODELS_NAME}.git", tmp_models)
                # Install models
                _pp("Installing Models")
                install_pretrained_models(tmp_models, ASSISTANT_PATH, lang)
        else:
            m = gm[0] # Take the first model here but we'll let rasa choose the best (inside the same dir)
            models = Path(m).parent # Take the parent dir
            print(f"Found models at {models}.")
    else:
        print(f"Found local models at {models}.")
    
    nlp_server_proc = Process(target=serve_lm, args=(data_path, models, endpoints, credentials))
    actions_server_proc = Process(target=serve_actions, args=(data_path, module_name))
    nlp_server_proc.start()
    actions_server_proc.start()
    return nlp_server_proc.join(), actions_server_proc.join()

def check_cookiecutter():
    fp = shutil.which('cookiecutter')
    if not fp:
        print("You must install `cookiecutter` somewhere inside your $PATH.")
        print("$\tpip install -U cookiecutter")
    return fp

def bake_cookie_domain(recipe_url=REPO_BASE_COOKIECUTTER_URL):
    cc = check_cookiecutter()
    if not cc:
        return 1
    else:
        bake_recipe = [
            f"{cc}",
            f"{recipe_url}"
        ]
        p = subprocess.Popen(bake_recipe, universal_newlines=True)
        output, errors = p.communicate()
        if errors:
            print(errors)
            return 1
        else:
            print("Your domain was successfully created here.")
            print("Use `git init` inside the domain to initialize the repository")
            print("and `git push` to upload it.")
            return 0

def print_paths(domains_path=None, data_path=None, config_path=None, models_path=None):
    results = ()
    if domains_path:
        results += (domains_path,)
        print(f"Domains Path: {domains_path}")
    if data_path:
        results += (data_path,)
        print(f"Data Path: {data_path}")
    if config_path:
        results += (config_path,)
        print(f"Config Path: {config_path}")
    if models_path:
        results += (models_path,)
        print(f"Models Path: {models_path}")
    if len(results) == 1:
        return results[0]
    return results

def main(ARGS):

    if not ARGS.version and not ARGS.list and not ARGS.create and not ARGS.add and not ARGS.sync and not ARGS.validate and not ARGS.train and not ARGS.serve:
        _pp("Domain Management Tool")
        print(f"Version: {str(__version__)}")
        print()
        print("[Tip]: Type dmt --help for help")
    
    if ARGS.version:
        _pp("Domain Management Tool")
        print(f"Version: {str(__version__)}")
        return

    if ARGS.list and ARGS.lang:
        spinner = Halo(text="Fetching Installed Domains", spinner='dots')
        spinner.start()
        # Checking domains directory exists
        mk_assistant_dir(ASSISTANT_PATH)
        domains_path = print_paths(domains_path=f"{ASSISTANT_PATH}/domains/{ARGS.lang}")
        # for each domain
        list_installed_domains = get_list_installed_domains(domains_path)
        ## get metadata.name
        ## get metadata.url
        spinner.stop()
        _pp(f"{ARGS.lang.upper()}: List of installed domains")
        for domain in list_installed_domains:
            print(f"\t- {domain.get('name')}:\t{domain.get('url')}")
        return
    
    if ARGS.create:
        # Create new domain from cookiecutter template repo
        _pp("Creating new domain")
        _pp("Looking for template...")
        sys.exit(bake_cookie_domain())
    
    if ARGS.add:
        #spinner = Halo(text="Cloning Domain", spinner='dots')
        _pp("Adding new domain")
        #spinner.start()
        print(f"GitURL: {ARGS.add}")
        # Clone domain
        tmp_domain = mktemp(f"dmt") + "/add_domain"
        _pp("Cloning Domain")
        git_clone(ARGS.add, tmp_domain)
        # Install domain
        _pp("Installing Domain")
        install_domain(tmp_domain, ASSISTANT_PATH)

        if not ARGS.validate or not ARGS.train:
            _pp("Warning")
            print("You need to validate this domain and train a new model to install this domain properly.")
            print("\t$\tdmt -V -T")
        #spinner.stop()
    
    if ARGS.sync and ARGS.lang:
        #spinner = Halo(text="Summoning Domains", spinner='dots')
        # Sync domains
        _pp(f"Syncho-summoning Domains for {ARGS.lang.upper()}")
        #spinner.start()
        # Checking domains directory exists
        domains_path = print_paths(domains_path=f"{ASSISTANT_PATH}/domains/{ARGS.lang}")
        Path(domains_path).mkdir(parents=True, exist_ok=True)
        # for each domain
        list_installed_domains = get_list_installed_domains(domains_path)
        for domain in tqdm(list_installed_domains):
        ##  Clone domain
            domain_name = domain.get('name')
            domain_url = domain.get('url')
            if domain_url:
                work_dir = mktemp(f"dmt/{domain_name if domain_name else 'unamed_domain'}")
                _pp(f"Cloning Domain {domain_name}")
                git_clone(domain_url, work_dir)
        ## Install domain
                _pp(f"Installing Domain {domain_name}")
                install_domain(work_dir, ASSISTANT_PATH)
        #spinner.stop()

    if ARGS.validate and ARGS.lang:
        # Validate data
        #spinner = Halo(text=f"Validating {ARGS.lang.upper()}", spinner='dots')
        _pp(f"Validating Data for {ARGS.lang.upper()}")
        domains_path, data_path, config_path = print_paths(domains_path=f"domains/{ARGS.lang}", data_path=f"data/{ARGS.lang}", config_path=f"configs/{ARGS.lang}/config.yml")
        #spinner.start()
        validate_data(ASSISTANT_PATH, domains=domains_path, data=data_path, config=config_path)
        #spinner.stop()

    if ARGS.train and ARGS.lang:
        # Train
        #spinner = Halo(text="Training", spinner='dots')
        _pp("Training Models")
        domains_path, data_path, config_path, models_path = print_paths(domains_path=f"domains/{ARGS.lang}", data_path=f"data/{ARGS.lang}", config_path=f"configs/{ARGS.lang}/config.yml", models_path=f"models/{ARGS.lang}/NLU")
        #spinner.start()
        train_lm(ASSISTANT_PATH, domains=domains_path, data=data_path, config=config_path, models=models_path)
        #spinner.stop()
    
    if ARGS.serve and ARGS.lang:
        # Train
        #spinner = Halo(text="Serving", spinner='dots')
        _pp("Serving Models")
        models_path = print_paths(models_path=f"models/{ARGS.lang}/NLU")
        #spinner.start()
        models_as_service(models=models_path, lang=ARGS.lang)
        #spinner.stop()
    
    return 0
