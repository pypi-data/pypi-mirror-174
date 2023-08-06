# -*- coding: utf-8 -*-
"""
    * vcf-tools
    * Created by liuxiaodong on 2022/10/16.
    * Change Activity:
    *     liuxiaodong   2022/10/16.
"""

import uuid
# import wmi


class Hardware:
    @staticmethod
    def get_cpu_sn():
        """
        获取CPU序列号
        :return: CPU序列号
        """
        c = wmi.WMI()
        for cpu in c.Win32_Processor():
            # print(cpu.ProcessorId.strip())
            return cpu.ProcessorId.strip()

    @staticmethod
    def get_baseboard_sn():
        """
        获取主板序列号
        :return: 主板序列号
        """
        c = wmi.WMI()
        for board_id in c.Win32_BaseBoard():
            # print(board_id.SerialNumber)
            return board_id.SerialNumber

    @staticmethod
    def get_bios_sn():
        """
        获取BIOS序列号
        :return: BIOS序列号
        """
        c = wmi.WMI()
        for bios_id in c.Win32_BIOS():
            # print(bios_id.SerialNumber.strip)
            return bios_id.SerialNumber.strip()

    @staticmethod
    def get_disk_sn():
        """
        获取硬盘序列号
        :return: 硬盘序列号列表
        """
        c = wmi.WMI()

        disk_sn_list = []
        for physical_disk in c.Win32_DiskDrive():
            # print(physical_disk.SerialNumber)
            # print(physical_disk.SerialNumber.replace(" ", ""))
            disk_sn_list.append(physical_disk.SerialNumber.replace(" ", ""))
        return disk_sn_list

    @staticmethod
    def get_mac():
        """
        获取mac地址
        """
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0,11,2)])

    @staticmethod
    def get_info():
        # cpu_sn = Hardware.get_cpu_sn()
        # baseboard_sn = Hardware.get_baseboard_sn()
        # bios_sn = Hardware.get_bios_sn()
        # disk_sn = Hardware.get_disk_sn()
        mac = Hardware.get_mac()
        return {
            # 'cpu_sn': cpu_sn,
            # 'baseboard_sn': baseboard_sn,
            # 'bios_sn': bios_sn,
            # 'disk_sn': disk_sn,
            'mac': mac
        }
