# ColorInfo

## 介绍

ColorInfo 是一个使用Python3编写的简单的彩色日志工具,主要特性:

* 使用简单
* 彩色输出
* 中文注释
* 支持全部Python3版本(>=3.0)

## 更新内容

### `1.0.0`

* 增加覆盖功能选项: `cover`, 默认关闭此功能
* 修改包名为: `ColorInfo`
* 重构信息生成逻辑，简化重复代码

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

logger = ColorLogger()
logger.info("1", "2")
logger.debug("3", "4")
logger.warning("5")
logger.error("6", "7", "yes")
```

# 效果

请在`gitee`项目主页点击下下面的按钮

![logg.png](./logg.png)

# 项目主页

[https://pypi.org/project/colorloggers](https://pypi.org/project/colorloggers/)

[https://gitee.com/liumou_site/pypicolorloggers.git](https://gitee.com/liumou_site/pypicolorloggers.git)