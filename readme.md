# Course Project: Implement Your Modulo Scheduler (SDC-SDC)

## Introduction

This is the repository for the first student project in the course **Synthesis of Digital Circuits**.
The goal of this project is to practice the theory of modulo scheduling we have covered in this lecture.

## Installation on own machine

### Graphviz (A Graph Visualization Engine)

Graphiz should be installable on any Unix-like or Unix OS with your package manager, e.g. for Ubuntu:

```sh
sudo apt-get install graphviz graphviz-dev
```

Graphviz can be tricky to install on Windows machines, but should be possible.
Instructions can be found at https://forum.graphviz.org/t/new-simplified-installation-procedure-on-windows/224

If you manage to get it running on Windows, let us know what you did so we can share it with others.

### Python

Tested python version is 3.7

Dependencies:
pygraph
llvmlite
pulp
matplotlib

If running on Windows, our recommendation is the Anaconda Prompt through the miniconda installation: https://docs.anaconda.com/free/miniconda/

```sh
conda create --name sdc_proj_1 python=3.6
conda activate sdc_proj_1
pip install pygraphviz llvmlite pulp matplotlib
```

## Running on the VM

The password and sudo password are both "sdc".
The terminal can be opened with CTRL+T, or from the Activities panel. VS Code is available from the Activities panel.

The sdc_project1 directory is in the home directory. 

In order to activate the python virtual environment please run:
```sh
conda activate sdc_proj_1
```


