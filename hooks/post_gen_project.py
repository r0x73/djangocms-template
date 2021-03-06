#!/usr/bin/env python

import os
import subprocess


def install_drifter():
    os.system('git init .')
    os.system('curl -sS https://raw.githubusercontent.com/liip/drifter/master/install.sh | /bin/bash')


def set_parameter(path, key, value):
    patched_lines = []
    parameter_exists = False

    with open(path) as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith('{}:'.format(key)):
            line = '{key}: "{value}"\n'.format(key=key, value=value)
            parameter_exists = True
        patched_lines.append(line)

    if not parameter_exists:
        patched_lines.append('{key}: "{value}"\n'.format(key=key, value=value))

    with open(path, 'w') as f:
        f.write(''.join(patched_lines))


def patch_parameters(path):
    set_parameter(path, 'django_pip_requirements', 'requirements/dev.txt')
    set_parameter(path, 'project_name', '{{ cookiecutter.project_slug }}')
    set_parameter(path, 'database_name', '{{ cookiecutter.project_slug }}')
    set_parameter(path, 'hostname', "{{ cookiecutter.project_slug.replace('_', '-') }}.lo")
    set_parameter(path, 'python_version', '3')


def patch_playbook(path):
    patched_lines = []

    with open(path) as f:
        lines = f.readlines()

    wanted_roles = ['django', 'postgresql', 'gulp']

    for line in lines:
        for role in wanted_roles:
            if 'role: %s' % role in line:
                line = line.replace('# -', '-')

        patched_lines.append(line)

    with open(path, 'w') as f:
        f.write(''.join(patched_lines))


def pip_compile(path):
    with open('/dev/null', 'wb') as f:
        subprocess.call(['pip-compile', path], stdout=f)


if __name__ == '__main__':
    if '{{ cookiecutter.use_drifter }}' == 'y':
        install_drifter()
        patch_parameters('virtualization/parameters.yml')
        patch_playbook('virtualization/playbook.yml')

    pip_compile('requirements/dev.in')
    pip_compile('requirements/base.in')
    pip_compile('requirements/deploy.in')
