def LegacyGithubImport(Module, Creator, ImportName):
  #This only works with legacy modules, all other modules require GIT and such, and for now, I'm not going through that again.
  import os
  os.system("pip install git+https://github.com/" + str(Creator) + "/" + str(Module) + "#egg=" + str(ImportName))

def SilentExit():
  import time
  time.sleep(9223372036)

def SearchDict(Dict, Key, DictSubLevels):
  import math
  Indexes = {}
  IndexesAppend = {}
  AllIndexes = {}
  Counter1 = 0
  for x in Dict:
    IndexesAppend.update({Counter1: Dict[x]})
    Counter1 += 1
  Indexes.update({0: IndexesAppend})
  IndexesAppend = {}
  Counter3 = 0
  Counter4 = 0
  for z in range(DictSubLevels):
    Counter2 = 0
    Counter1 = 0
    for x in list(Indexes[Counter3]):
      for y in Indexes[Counter3][Counter2]:
        try:
          if str(type(Indexes[Counter3][Counter2])) == "<class 'dict'>":
            IndexesAppend.update({Counter1: Indexes[Counter3][Counter2][y]})
            AllIndexes.update({y: Indexes[Counter3][Counter2][y]})
            Counter1 += 1
            Counter4 += 1
        except:
          pass
      Counter2 += 1
    Counter3 += 1
    Indexes.update({Counter3: IndexesAppend})
    IndexesAppend = {}
  if Key in AllIndexes:
    return AllIndexes[Key]
  elif Key in Dict:
    return Dict[Key]
  else:
    raise NameError("Invalid key name. (If this is a key, try increasing the third paramater. (How deep this searches.)")
