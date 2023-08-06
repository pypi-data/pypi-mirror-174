# ColorInfo

## 介绍

ColorInfo 是一个使用Python3编写的简单的彩色日志工具,主要特性:

* 使用简单
* 彩色输出
* 中文注释
* 支持全部Python3版本(>=3.0)

## 更新内容

### `1.1.4`

* 增加`set_format`函数,可按需显示相关信息

```python
def set_format(self, date_on=True, time_on=True, filename_on=True, class_on=True, fun_on=True, line_on=True):
    """
    设置格式开关,默认全开
    :param line_on: 是否显示行号(默认: True)-line: 230
    :param fun_on: 是否显示函数(默认: True)
    :param class_on: 是否显示类(默认: True)
    :param date_on: 是否显示日期(默认: True)-2022-11-03
    :param time_on: 是否显示时间(默认: True)-20:42:24
    :param filename_on: 是否显示文件名(源码文件)(默认: True)-ColorInfo.py
    :return:
    """
```

## 安装教程

执行下面的命令即可

```shell
pip3 install ColorInfo
```

## Demo

```
# -*- encoding: utf-8 -*-
"""
@File    :   demo.py
@Time    :   2022-10-26 23:51
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   演示
"""
from ColorInfo import ColorLogger

log = ColorLogger(txt=True, fileinfo=True, basename=False)
log.info(msg='1', x="23")
log.error('2', '22', '222')
log.debug('3', '21')
log.warning('4', '20', 22)
```

# 效果

请在`gitee`项目主页查看图片

![logg.png](./Demo.png)

# 项目主页

[https://pypi.org/project/colorloggers](https://pypi.org/project/colorloggers/)

[https://gitee.com/liumou_site/ColorInfo.git](https://gitee.com/liumou_site/ColorInfo.git)
