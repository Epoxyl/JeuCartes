from datetime import datetime

from Game import game_directory

class Log:
  save = False
  path = "{}/Logs/log.txt".format(game_directory)

  @staticmethod
  def printlog(message):
    log = "[{}] : {} ".format(datetime.now(), message)

    if Log.save:
      Log.savelog(log)
    print(log)

  @staticmethod
  def savelog(log):
    with open(Log.path, "a", encoding="utf-8") as file_log:
      file_log.write("{} \n".format(log))
