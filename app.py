import os
import shutil
import re
import subprocess
from sys import argv
import json

import requests
from tqdm import tqdm

from git import Repo
from git import RemoteProgress

try:
    url = argv[1]  # получаем первую переменную, поданную на вход. Нужно сделать без рестарта контейнера
except(IndexError):
    print("Введите ссылку гитхаб/докерхаб")
dir = './project/'


class CloneProgress(RemoteProgress):
    # Прогресс для клонирования репозитория
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


def python_scan(folders_):
    bandit = subprocess.run(['bandit', '-r', folders_], capture_output=True, text=True)
    print(bandit.stdout)


def go_scan(folders_):
    pass


''' os.environ["PATH"] = "$PATH:/usr/local/bin/go/bin"
    os.environ["PATH"] = "$PATH:/usr/local/bin/"
    thisdir = os.getcwd()
    os.chdir(folders_)


    gosec = subprocess.run(['gosec', '-r', './...'], capture_output=True, text=True)
    print(gosec.stdout)
    os.chdir(thisdir)
    print(os.getcwd())
'''


def java_scan(folders_):
    subprocess.run(['/home/toor/dependency-check/bin/dependency-check.sh',
                    '--scan', folders_, '-f', 'JSON'], capture_output=True)

    with open('dependency-check-report.json') as report:
        x = json.loads(report.readline())
        print(json.dumps(x, indent=4))


def github_scan():
    # сканирование гитхаба
    name = url[re.search(r'.com/', url).end():]
    folders = dir + name
    try:
        # Удалаем папку если есть
        shutil.rmtree(folders)
        pass
    except(FileNotFoundError):
        pass
    Repo.clone_from(url, folders, CloneProgress())
    # Клонируем репо в папку
    api_git = 'https://api.github.com/repos/' + name + '/languages'
    req = requests.get(api_git)
    lang_repo = ''
    try:
        lang_repo = req.text[2:-1]
        lang_repo = lang_repo.split(',')[0]  # Режем строку на языки и берем самый частый
    except():
        pass

    if 'Python' in lang_repo:
        python_scan(folders)
    if 'Go' in lang_repo:
        go_scan(folders)
    if 'Java' in lang_repo:
        java_scan(folders)


#TODO понять как запустить сонар
#TODO выбираем инстурменты под язык СИ
#TODO сделать так, чтобы контейнер не установаливал все подряд
#TODO пофиксить докерфайл
#TODO доделать го
#TODO нужно ли юзать триви с гита?
#TODO найти больше инструментов


def docker_scan():
    name = url[re.search(r'.com/', url).end():]  # грепаем нормально имя контейнера
    if '_/' or 'r/' == name[:1] in name:
        if '/' == name[-1]: name = name[:-1]
        name = name[2:]
    print("__________________Trivy_____________________ ")
    trivy = subprocess.run(['trivy', 'image', name], capture_output=True, text=True)
    print(trivy.stdout)

    print("__________________Grype_____________________ ")
    grype = subprocess.run(['grype', '-vv', name], capture_output=True, text=True)
    print(grype.stdout)
    # стащить ридми


if 'github' in url:
    github_scan()

if 'docker' in url:
    docker_scan()
    print()
