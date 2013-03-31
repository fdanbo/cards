
import os
import peewee

DB = peewee.SqliteDatabase(None)

class bjplay(peewee.Model):
  # sum of hand, and whether it's soft. eg, soft 17 is actually 7 or 17
  handValue = peewee.IntegerField()
  soft = peewee.BooleanField()

  # ace=1; TJQK are all 10
  dealerRank = peewee.IntegerField()

  # whether this is the final state of the hand
  final = peewee.BooleanField()

  # whether the hand could have been hit, split, doubled, or surrendered
  canHit = peewee.BooleanField()
  canSplit = peewee.BooleanField()
  canDouble = peewee.BooleanField()
  canSurrender = peewee.BooleanField()

  parentPlay = peewee.ForeignKeyField('self', null=True)

  move = peewee.CharField(null=True)

  # total amount won on the hand as a fraction of the bet. to keep this as an integer, it's a
  # fraction of 10, typically -10, 0, or 10 (loss, push, win).  Can be -5 for a surrender or 15 for
  # a blackjack.  can even be as high as 80 or as low as -80 for multiple splits/doubles.
  handResult = peewee.IntegerField()

  class Meta:
    database = DB

  @staticmethod
  def createDatabase(fileName):
    if os.path.exists(fileName):
      os.unlink(fileName)
    DB.init(fileName)
    bjplay.create_table()
