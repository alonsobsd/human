import argparse
import os
import random
from importlib import import_module
from time import sleep

from app.utility.webdriver_helper import WebDriverHelper


TASK_CLUSTER_COUNT = 5
TASK_INTERVAL_SECONDS = 10
GROUPING_INTERVAL_SECONDS = 500


def emulation_loop(workflows, clustersize, taskinterval, taskgroupinterval):
    while True:
        for c in range(clustersize):
            sleep(random.randrange(taskinterval))
            workflows[random.randrange(len(workflows))].action()
        sleep(random.randrange(taskgroupinterval))


def import_workflows(webdriver_helper):
    extensions = []
    for root, dirs, files in os.walk(os.path.join('app', 'workflows')):
        files = [f for f in files if not f[0] == '.' and not f[0] == "_"]
        dirs[:] = [d for d in dirs if not d[0] == '.' and not d[0] == "_"]
        for file in files:
            extensions.append(load_module(root, file, webdriver_helper))
    return extensions


def load_module(root, file, webdriver_helper):
    module = os.path.join(root, file.split('.')[0]).replace(os.path.sep, '.')
    try:
        return getattr(import_module(module), 'load')(driver=webdriver_helper)
    except Exception as e:
        print('Error could not load workflow. {}'.format(e))


def run(clustersize, taskinterval, taskgroupinterval):
    random.seed()
    webdriver_helper = WebDriverHelper()
    if webdriver_helper.browser != '':
        workflows = import_workflows(webdriver_helper=webdriver_helper)
        emulation_loop(workflows=workflows, clustersize=clustersize, taskinterval=taskinterval,
                       taskgroupinterval=taskgroupinterval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Emulate human behavior on a system')
    parser.add_argument('--clustersize', type=int, default=TASK_CLUSTER_COUNT)
    parser.add_argument('--taskinterval', type=int, default=TASK_INTERVAL_SECONDS)
    parser.add_argument('--taskgroupinterval', type=int, default=GROUPING_INTERVAL_SECONDS)
    args = parser.parse_args()
    run(clustersize=args.clustersize, taskinterval=args.taskinterval, taskgroupinterval=args.taskgroupinterval)