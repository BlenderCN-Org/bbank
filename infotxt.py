import os
# displays the README.txt for now...
# but eventually change this to a hardcoded string
infotxt = open(os.path.join(os.path.dirname(__file__),"README.txt"),'r',encoding='utf-8').read().split(os.linesep)

