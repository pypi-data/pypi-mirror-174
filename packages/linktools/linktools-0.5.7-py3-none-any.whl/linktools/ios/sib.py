#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author  : Hu Ji
@file    : sib.py 
@time    : 2022/10/29
@site    :  
@software: PyCharm 

              ,----------------,              ,---------,
         ,-----------------------,          ,"        ,"|
       ,"                      ,"|        ,"        ,"  |
      +-----------------------+  |      ,"        ,"    |
      |  .-----------------.  |  |     +---------+      |
      |  |                 |  |  |     | -==----'|      |
      |  | $ sudo rm -rf / |  |  |     |         |      |
      |  |                 |  |  |/----|`---=    |      |
      |  |                 |  |  |   ,/|==== ooo |      ;
      |  |                 |  |  |  // |(((( [33]|    ,"
      |  `-----------------'  |," .;'| |((((     |  ,"
      +-----------------------+  ;;  | |         |,"
         /_)______________(_/  //'   | +---------+
    ___________________________/___  `,
   /  oooooooooooooooo  .o.  oooo /,   \,"-----------
  / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
 /_==__==========__==_ooo__ooo=_/'   /___________,"
"""
import json
import subprocess
import warnings
from typing import Any

from linktools import get_logger, tools, utils
from linktools.decorator import cached_property

logger = get_logger("ios.sib")


class SibError(Exception):

    def __init__(self, message: str):
        super().__init__(message.rstrip("\r\n"))


class Sib(object):
    _alive_status = ["online"]

    @classmethod
    def devices(cls, alive: bool = None) -> [str]:
        """
        获取所有设备列表
        :param alive: 只显示在线的设备
        :return: 设备号数组
        """
        devices = []
        result = cls.exec("devices", "--format")
        result_json = json.loads(result)
        if not result_json or "deviceList" not in result_json:
            raise SibError(result)
        for device in utils.get_list_item(result_json, "deviceList") or []:
            if alive is None:
                devices.append(device.get("serialNumber"))
            elif alive == (device.get("status") in cls._alive_status):
                devices.append(device.get("serialNumber"))
        return devices

    @classmethod
    def popen(cls, *args: [str], **kwargs) -> subprocess.Popen:
        return tools["sib"].popen(*args, **kwargs)

    @classmethod
    def exec(cls, *args: [str], ignore_error: bool = False, **kwargs) -> str:
        """
        执行命令
        :param args: 命令
        :param ignore_error: 忽略错误，报错不会抛异常
        :return: 如果是不是守护进程，返回输出结果；如果是守护进程，则返回Popen对象
        """
        process, out, err = tools["sib"].exec(*args, **kwargs)
        if not ignore_error and process.returncode != 0 and not utils.is_empty(err):
            err = err.decode(errors='ignore')
            if not utils.is_empty(err):
                raise SibError(err)
        return out.decode(errors='ignore') if out is not None else ""


class Device(object):

    def __init__(self, device_id: str = None):
        """
        :param device_id: 设备号
        """
        if device_id is None:
            devices = Sib.devices(alive=True)
            if len(devices) == 0:
                raise SibError("no devices/emulators found")
            elif len(devices) > 1:
                raise SibError("more than one device/emulator")
            self._device_id = next(iter(devices))
        else:
            self._device_id = device_id

    @cached_property
    def id(self) -> str:
        """
        获取设备号
        :return: 设备号
        """
        return self._device_id

    def exec(self, *args: [str], explicit_id: bool = False, **kwargs) -> str:
        """
        执行命令
        :param args: 命令行参数
        :param explicit_id: 显式指定udid参数
        :return: sib输出结果
        """
        args = ["-s", self.id, *args]
        if explicit_id:
            args.extend(["--udid", self.id])
        return Sib.exec(*args, **kwargs)

    def install(self, file_path: str, **kwargs) -> str:
        """
        安装ipa
        :param file_path: ipa文件路径
        :return: sib输出结果
        """
        kwargs["explicit_id"] = True
        return self.exec("app", "install", file_path, **kwargs)

    def uninstall(self, bundle_id: str, **kwargs) -> str:
        """
        卸载ipa
        :param bundle_id: 包名
        :return: sib输出结果
        """
        kwargs["explicit_id"] = True
        return self.exec("app", "uninstall", bundle_id, **kwargs)

    def kill(self, bundle_id: str, **kwargs) -> str:
        """
        卸载ipa
        :param bundle_id: 包名
        :return: sib输出结果
        """
        kwargs["explicit_id"] = True
        return self.exec("app", "kill", bundle_id, **kwargs)

    @classmethod
    def _ignore_invalid_argument(cls, kwargs: dict, key: str, value: Any):
        if key in kwargs:
            if kwargs[key] == value:
                kwargs.pop(key)
                warnings.warn(f"invalid argument {key}={value}, ignored!", stacklevel=2)

    def __repr__(self):
        return f"SibDevice<{self.id}>"


if __name__ == '__main__':
    for d in Sib().devices(alive=True):
        print(d)
