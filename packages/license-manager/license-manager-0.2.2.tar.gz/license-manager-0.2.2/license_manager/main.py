# -*- coding: utf-8 -*-
"""
    * vcf-tools
    * Created by liuxiaodong on 2022/10/16.
    * Change Activity:
    *     liuxiaodong   2022/10/16.
"""

import fire
from license_manager.command import create, verify, hardware


def main():
    fire.Fire({
        'create': create,
        'verify': verify,
        'hardware': hardware
    })


if __name__ == '__main__':
    main()