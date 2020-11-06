# Tookits for An Iterative Weighting Method to Apply the ISR Correction
Maybe you have noticed that a new method for ISR iteration has been proposed by Liangliang Wang (llwang@ihep.ac.cn) and Wenyu Sun (sunwenyu@ihep.ac.cn) (theory introduction of this method could be found in doc/Introduction.pdf), recently. After the check doing by Tong Liu (liutong2016@ihep.ac.cn) (MC generation examples could be found in example/), this method has been proved to be correct and is very time saving. This repository provides a relative general package for user to use this method to do ISR iteration. The main codes are based on Lianjin Wu's codes (wulj@ihep.ac.cn), which is very appreciating. If you are not familiar with GitHub operation, you can copy the codes from /besfs/groups/cal/dedx/jingmq/bes/weighted_isr, if the storage patch changed, the newest path will be shown in here, also all the changes will be updated to repository in GitHub. 

## Install

> cd [Your Work Directory]

> git clone https://github.com/zhixing1996/weighted_isr.git

## Setup

ROOT Version: 5.34/09 or later

Python Version: 2.7.3, should not be python3.x

## Structure of this Repository

> weight_isr.conf: configure file, user's changes will happen in here mostly.

1. [patch]: patch info, mainly used to create plots name and files name. 
    1. label: a very simple description of the cross sections you put;
    2. iter_old: description of the patch of iteration right now;
    3. iter_new: description of the patch of next iteration.

2. [path]: path info of input cross sections and ouput cross sections as well as initial isr factor.
    1. xs_old: input cross sections info;
    2. xs_new: output cross sections info;
    3. ini_isr: initial isr factors calculated by scripts like example/ (referred as INI).

3. [draw]: xtitles and ytitles of output plots.
    1. xtitle
    2. xs_ytitle: ytitle of cross section plots;
    3. eff_ytitle: ytitle of isr factors times relative efficiencies plots.

3. [weight]: necessary info for weighting mc and new cross sections calculation.
    1. shape_dep: True/true or False/false: whether the fitting concerning number of events (referred as FIT_EVT) is mc shape dependent or not;
    2. root_path: root path of INI root files;
    3. event_root: name of root files after selection, should be put under root_path, if the name contains sample info, like sigMC_D1_2420_4420_after.root, please replace 4420 with ECMS;
    4. truth_root: name of root files containing MC truth info, should be put under root_path, if the name contains sample info, like sigMC_D1_2420_4420_truth.root, please replace 4420 with ECMS;
    5. event_tree: tree name in [3], M(truth) branch name in tree must be m_m_truthall;
    6. truth_tree: tree name in [4], M(truth) branch name in tree must be m_m_truthall;
    7. cut_weight: some extra cuts, not recommend to add in the this repository, better to apply all the cuts before executing the program;
    8. pyroot_fit: True/true or False/false, only if shape_dep is set to be True/true, this part will be useful: using dedicated pyROOT Roofit program (tools/simul_fit.py) in this package to do FIT_EVT, this is a recommended way to do iteration since it will be very automatically, however, this will also put a pretty strict requirement of user's pyROOT knowledge, user can also dismiss this function by setting this part to be False/false with manual_update to be False(false), and then update out put files (relative nsignal info) in xs_new, and then execute 'python main.py' again, especially, if you want to use pyROOT Roofit program, this part must be set to be False/false;
    9. manual_update: whether user has updated output results in xs_new (relative nsignal info) manually or not.

4. [WIP]: Working in progress, any recommends will be welcomed sincerely! Some functions of this repository haven't been tested by explicit analysis, if you would like to use this repository, please be sure to share your feelings and errors encountered!

List input of [patch] -- label, [path] -- xs_old, and xs_new, and ini_isr, [draw] -- xtitle, xs_ytitle, and eff_ytitle, and [weight] -- root_path, event_root, and truth_root is supported in case the number of components in your FIT_EVT is larger than one, but you have to pay attention to the order of your input.

> main.py: main program of this repository.

> tools: programs used in main.py, especially, tools/simul_fit_cal.py is used for calibration of FIT_EVT, and params.py stores the parameters used in FIT_EVT, if you have set pyroot_fit to be False, tools/simul_fit.py, tools/simul_fit_cal.py, and tools/params.py will not be used.

> log: input and out put cross sections info (without the value of cross sections, will be provided in another directory)

1. The format of the input cross sections info files could be found in the cloned repository;
2. Commenting is supported from line 2 of files in log/ by using '#' in head of the line, but no black space is allowed between '#' and head of the line, if '#' is added, when doing cross sections fitting (referred as FIT_XS) corresponding data sample will not be used, this is very useful if there is some data sample which has very low statistics level existing in your FIT_XS.

## Some Codes You Have to Change

The aim of this repository is to provide a general package for users and the only thing user has to do is changing configure file (weight_isr.conf). However, due to the complexity of user defined functions in FIT_XS and plot styles of canvas or some thing else, it is very hard to provide a total general script. Therefore, the developer has to leave this space to users and the structure of this repository is based on python2. Fortunately, the thing user has to change is not very much and very easy to understand without very deep python knowledge.

> In main.py: line 74 - 135, defination of fit functions for input cross sections;

> In tools/fit_xs.py: line 26 - 34, defination of cross sections formula;

> In tools/update.py: line 127 - 148, import module of user defined fit function (in FIT_EVT, if the calculation of cross section is mc shape dependent) and usage of it, this section could be dismissed by setting [weight]: pyroot_fit = False and update the number of events manually and continue your work by setting [weight]: manual_update = False before updating and then True after updating;

> In tools/fill_xs.py: line 30 - 38, defination of cross section formula.

Or user can use 'grep "USER DEFINE SECTION" [files]' command to search which sections you have to change.

## Execute

> cd [Your Work Directory]/weighted_isr

> python main.py

## Output When Executing

> figs: directory, created automatically by main.py, stores output figures when doing FIT_XS(fitting results of cross sections and isr times efficiency) and doing FIT_EVT(if you like) (created by main.py);

> log: directory, cloned from GitHub, stores updated cross sections info (created by tools/update.py);

> txts: directoy, created automatically by main.py, stores cross sections info (containing the values of cross sections, created by tools/fill_xs.py);

> weights: directory, created automatically by main.py, stores root files containing calculated events weights used in FIT_EVT (created by tools/update.py, scaling MC shape).

## For developers 
 
- Fork the code with your personal github ID. See [details](https://help.github.com/articles/fork-a-repo/)
 
> git clone https://github.com/zhixing1996/weighted_isr.git
 
- Make your change, commit and push
 
> git commit -a -m "Added feature A, B, C"
 
> git push
 
- Make a pull request. See [details](https://help.github.com/articles/using-pull-requests/)
 
## Some styles to follow 
- Minimize the number of main codes
- Keep functions length less than one screen
- Seperate hard-coded cuts into script file
- Use pull-request mode on git 
- Document well the high-level bash file for work flow 
