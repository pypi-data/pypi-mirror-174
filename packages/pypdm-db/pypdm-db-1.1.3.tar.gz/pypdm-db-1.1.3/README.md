# pypdm-db

> mysql/sqlite 的 PDM 生成器

------

## 运行环境

![](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg) ![](https://img.shields.io/badge/PyCharm-4.0.4%2B-brightgreen.svg)


## 安装说明

执行脚本： 

```
python -m pip install --upgrade pip
python -m pip install pypdm-db
```


## 使用指引

示例代码可参考单元测试：

- sqlite: [test_pypdm_sqlite.py](tests/test_pypdm_sqlite.py)
- mysql: [test_pypdm_mysql.py](tests/test_pypdm_mysql.py)

通过以下函数可生成对应数据库的连接对象：

- `from pypdm.dbc._sqlite import SqliteDBC`
- `from pypdm.dbc._mysql import MysqlDBC`

通过函数 `from pypdm.builder import build` 可生成指定数据表的 PDM 文件。

例如数据库中已有表 [`t_teachers`](tests/db/sqlite/init_db.sql) ，会在指定的 package 目录生成两个代码文件：

- Bean 文件： [*/bean/t_teachers.py](tests/tmp/pdm/sqlite/bean/t_teachers.py)
- DAO 文件：  [*/dao/t_teachers.py](tests/tmp/pdm/sqlite/dao/t_teachers.py)


其中 Bean 文件与表 `t_teachers` 的表结构一一对应， DAO 文件则封装了针对表 `t_teachers` 的增删改查函数。利用这两个文件，就可以方便地对表 `t_teachers` 进行操作。


