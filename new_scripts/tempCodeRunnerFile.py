# fuzzy_testing_with_deploy.py

from brownie import accounts, network, project
import random
import string

# Load Brownie project
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *

# Import contract after loading the project
RestrictedText = p.RestrictedText