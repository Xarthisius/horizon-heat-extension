
import glob
from os.path import basename
from django.conf import settings
from yaml import load, dump


HEAT_ROOT = getattr(settings, "HEAT_ROOT", "/srv/heat/env")

TEMPLATE_PATH = "template"
ENV_PATH ="env"

HOT = ".hot"
ENV = ".env"

HOT_MASK = "*%s" % HOT
ENV_MASK = "*%s" % ENV


def filename(path):
    """helper
    return filename without extension
    """
    return basename(path).split(".")[0]


def get_templates(choices=True):
    """if choices is False return array of full path
    """

    path = "/".join([HEAT_ROOT, TEMPLATE_PATH])
    
    templates = []

    for path in glob.glob("/".join([path, HOT_MASK])):
        name = filename(path)
        templates.append((name, name.replace("_", " ").capitalize()))

    return sorted(templates)


def get_environments(template_name=None):
    """return environments choices
    """
    path = "/".join([HEAT_ROOT, ENV_PATH])

    environments = []

    if template_name:
        join = [path, template_name, ENV_MASK]
    else:
        join = [path, ENV_MASK]

    for path in glob.glob("/".join(join)):
        name = filename(path)        
        environments.append((name, name.replace("_", " ").capitalize()))

    return sorted(environments)


def get_template_data(name):
    """load and return template data
    """

    path = "/".join([
        HEAT_ROOT,
        TEMPLATE_PATH,
        "".join([name, HOT])
        ])

    try:
        f = open(path, 'r')
        data = load(f)
    except Exception, e:
        raise e

    return data


def get_environment_data(template_name, name):
    """load and return parameters data
    """

    path = "/".join([
        HEAT_ROOT,
        ENV_PATH,
        template_name,
        "".join([name, ENV])
        ])

    try:
        f = open(path, 'r')
        data = load(f)
    except Exception, e:
        raise e

    return data