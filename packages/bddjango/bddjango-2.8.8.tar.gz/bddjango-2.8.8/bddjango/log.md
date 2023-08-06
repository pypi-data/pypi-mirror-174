# bddjango版本更新


## 相关链接

- [wiki文档地址_内网](https://www.bodexiong.vip/mkdocs/)
- [wiki文档地址_外网](https://wiki-bddjango.readthedocs.io/zh/)
- [pypi项目地址](https://pypi.org/project/bddjango/)
- [查看当前最新版本号](https://pypi.org/search/?q=bddjango)


## 更新信息

### 2.8.1
- 更改项目信息
- 整合Readme.md文件

### 2.8.2
- test

# 2.8.3
- 导入导出数据AdminMixin开放给前端

# 2.8.4
- 导入导出优化, `.save`改为`.create`

# 2.8.5
- 导入导出修复: 解决了数据库中str字段导入时被pandas解析为float的bug

# 2.8.6
- 修复导出文件时, 空文件报错的bug

# 2.8.7
- 修复导出文件时, 有FileField字段导致报错的bug
- 可能还存在导出时有`None`没替换为空白的情况.

# 2.8.8
- 修复导出文件时, 有`DateField`时间格式字段解析失败的bug







