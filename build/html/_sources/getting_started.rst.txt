.. raw:: html

    <script type="text/javascript" src="_static/javascript/toggle_visibility.js"></script>

.. _getting_started:


***************
Lua自动编程界面介绍
***************

.. _installing-docdir:

目录结构
=============================
目录结构打印::

    ├── build               编译html文件的生成文件
    ├── config.py           自动生成docs的配置文件
    ├── demos               应用Lua自动编程界面的demos(重要)
    ├── dependencies        依赖
    ├── __init__.py
    ├── __init__.pyc
    ├── Main.py             主程序入口文件
    ├── Main.pyc
    ├── make.bat
    ├── Makefile            编译html文件的MakeFile
    ├── README.md
    ├── source              编译html文件的源文件
    ├── src                 已发布版本的文件目录
    └── test                测试开发版本的文件目录(重要)




.. _important_dir:

重要文件目录
=============================


+-------+-----------------------------------------------------------------+
| 目录  | 说明                                                            |
+-------+-----------------------------------------------------------------+
| demos | 包含底层自动转出代码的引擎及对Commands重写的文件                |
+-------+-----------------------------------------------------------------+
| test  | 包含所有自动Lua编程GUI的逻辑代码及调用demos中的引擎写命令的逻辑 |
+-------+-----------------------------------------------------------------+


.. _realization_result:

实现效果
=============================

集成在主界面作为自动编程功能
-----------------------------

.. image:: _static/add_with_Main_panel.png

独立实现的效果
-----------------------------

.. image:: _static/only_one_panel.png

.. _execution_principle:

运行模型
=============================

#. :ref:`simple_model`

#. :ref:`link_relationship_between_functions`


.. _simple_model:

简单模型
----------------------------

简单的来讲， 软件模型是典型的MVC结构。
通过publisher机制对界面数据与底层数据之间的交互进行解耦，统一由Controller进行管理。


.. _link_relationship_between_functions:


功能间调用关系模型
----------------------------

.. image:: _static/images/Design_images/luaprogramming_model_communication.png


.. _control_model:

控制模型
===========================
| 相对于界面层的数据刷新显示以及数据模型层的数据结构，控制层提供了界面数据的刷新及界面控件的响应，数据模型的存取修改以及转化等功能。
| 因此独立对控制层的逻辑进行进一步分析。

.. _control_relationship:

控制交互关系图
---------------------------

.. image:: _static/images/Design_images/lua_programming_control_model.png

.. _controlmodel_analyze:

控制模块分析
---------------------------

未完待续........

