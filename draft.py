#!/bin/env python
# -*- coding: utf-8 -*-
#@Filename: draft
#@Author: bigman
#@Date: 2018/1/11
import psutil
p = psutil.Process(4)

dic = p.as_dict()
print(dic)

