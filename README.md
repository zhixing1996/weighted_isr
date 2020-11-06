# Tookits for An Iterative Weighting Method to Apply the ISR Correction
Maybe you have noticed that a new method for ISR iteration has been proposed by Liangliang Wang(llwang@ihep.ac.cn) and Wenyu Sun(sunwenyu@ihep.ac.cn) (the theory of the method could be seen in doc/Introduction.pdf), recently. After the check of Tong Liu(liutong2016@ihep.ac.cn) (MC generation example could be seen in example/), this method has been proved to be correct and very time saving. This repository provide a relative general package for user to use the method to do ISR iteration. 

## Install

> cd [Your Work Directory]

> git clone https://github.com/zhixing1996/weighted_isr.git

## Setup

ROOT Version: 5.34/09 or later

Python Version: 2.7.3, should not be python3.x

## Execute

> cd [Your Work Directory]

> python main.py

## Structure of this Repository

> weight_isr.conf: configure file, user changes will mostly happen in here

1. [patch] 
    1. label: a very simple description of the cross sections you put
    2. iter_old: description of the patch of iteration right now
    3. iter_new: description of the patch of next iteration


## How to use

The aim of this repository is to provide a general package for users and the only thing users have to do is changing configure file (weight_isr.conf). However, due to the complexity of user defined function and plot style of canvas or pad, it is very hard to provide a general script. Therefore, the developer have to leave this space to users and the structure of this repository is based on python2. Fortunately, the things user has to change is not very much and easier to understand without much python knowledge.

> In main.py: line 74 - 135, defination of fit functions for input cross sections;

> In tools/fit_xs.py: line 26 - 34, defination of cross section formula;

> In tools/update.py: line 127 - 148, import module of user defined fit function (to get number of events, if the calculation of cross section is mc shape dependent) and usage of it, this section could be dismissed by setting [weight]: shape_dep = False and update the number of events manually and continue your work by setting [weight]: manual_update = False before updating and then True after updating;

> In tools/fill_xs.py: line 30 - 38, defination of cross section formula.
