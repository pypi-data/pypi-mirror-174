# ColorInfo

## 介绍

ColorInfo 是一个使用Python3编写的简单的彩色日志工具,主要特性:

* 使用简单
* 彩色输出
* 中文注释
* 支持全部Python3版本(>=3.0)

## 更新内容

### `1.1.7`

* 等级设置增加验证及默认等级

```python
	def set_level(self, console="DEBUG", text="DEBUG"):
		"""
		设置显示等级,当实际等级低于设置等级的时候将不会显示/写入
		:param console: 设置控制台显示最低等级
		:param text: 设置文本记录最低等级
		:return: 
		"""
		self.level_console = self.level_dic[console.upper()]
		self.level_text = self.level_dic[text.upper()]
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
