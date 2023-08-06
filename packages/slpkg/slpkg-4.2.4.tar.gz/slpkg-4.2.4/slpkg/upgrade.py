#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass
from distutils.version import LooseVersion

from slpkg.configs import Configs
from slpkg.queries import SBoQueries


@dataclass
class Upgrade:
    log_packages: str = Configs.log_packages
    sbo_repo_tag: str = Configs.sbo_repo_tag

    def packages(self):
        ''' Compares version of packages and returns the maximum. '''
        print("Do not forget to run 'slpkg update' before.")

        repo_packages = SBoQueries('').names()

        for pkg in os.listdir(self.log_packages):
            if pkg.endswith(self.sbo_repo_tag):
                inst_pkg_name = '-'.join(pkg.split('-')[:-3])

                if inst_pkg_name in repo_packages:
                    installed_ver = pkg.replace(
                        inst_pkg_name + '-', '').split('-')[0]
                    repo_ver = SBoQueries(inst_pkg_name).version()

                    if LooseVersion(repo_ver) > LooseVersion(installed_ver):
                        yield inst_pkg_name
