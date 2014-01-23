
# playing strategies
S1 = {
  1:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'hit', 11:'hit', 12:'hit', 13:'hit',
    14:'hit', 15:'surrender,hit', 16:'surrender,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  },
  2:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'split,hit', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  3:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'split,hit', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  4:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  5:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'double,hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'double,hit', 's14':'double,hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  6:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'double,hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'double,hit', 's14':'double,hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  7:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'split,hit', 15:'hit', 16:'split,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  8:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'hit', 16:'split,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  9:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'hit', 16:'surrender,split,hit',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  10: {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'surrender,hit', 16:'surrender,split,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  }
}

MISTER_SPLITTER = {
  1:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'hit', 10:'split,hit', 11:'hit', 12:'split,hit', 13:'hit',
    14:'split,hit', 15:'surrender,hit', 16:'split,hit',
    17:'stand', 18:'split,stand', 19:'stand', 20:'split,stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  },
  2:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'hit', 10:'split,double,hit', 11:'double,hit', 12:'split,hit', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'split,stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  3:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'hit', 10:'split,double,hit', 11:'double,hit', 12:'split,hit', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'split,stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  4:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'hit', 10:'split,double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'split,stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  5:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'double,hit', 10:'split,double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'split,stand',
    's12':'split', 's13':'double,hit', 's14':'double,hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  6:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'double,hit', 10:'split,double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'split,stand',
    's12':'split', 's13':'double,hit', 's14':'double,hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  7:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'hit', 10:'split,double,hit', 11:'double,hit', 12:'split,hit', 13:'hit',
    14:'split,hit', 15:'hit', 16:'split,hit',
    17:'stand', 18:'split,stand', 19:'stand', 20:'split,stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  8:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'split,double,hit', 11:'double,hit', 12:'split,hit', 13:'hit',
    14:'split,hit', 15:'hit', 16:'split,hit',
    17:'stand', 18:'split,stand', 19:'stand', 20:'split,stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  9:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'hit', 10:'split,double,hit', 11:'double,hit', 12:'split,hit', 13:'hit',
    14:'split,hit', 15:'hit', 16:'split,surrender,hit',
    17:'stand', 18:'split,stand', 19:'stand', 20:'split,stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  10: {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'hit', 10:'split,hit', 11:'double,hit', 12:'split,hit', 13:'hit',
    14:'split,hit', 15:'surrender,hit', 16:'split,surrender,hit',
    17:'stand', 18:'split,stand', 19:'stand', 20:'split,stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  }
}

T1 = {
  1:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'hit', 11:'hit', 12:'hit', 13:'hit',
    14:'hit', 15:'hit', 16:'hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  },
  2:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'split,hit', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  3:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'split,hit', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  4:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  5:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'double,hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'double,hit', 's14':'double,hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  6:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'double,hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'double,hit', 's14':'double,hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  7:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'split,hit', 15:'hit', 16:'split,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  8:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'hit', 16:'split,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  9:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'hit', 16:'surrender,split,hit',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  10: {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'hit', 16:'hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  }
}

T2 = {
  1:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'hit', 11:'hit', 12:'hit', 13:'hit',
    14:'hit', 15:'stand', 16:'stand',
    17:'surrender,stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  },
  2:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'split,hit', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  3:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'split,hit', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  4:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  5:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'double,hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'double,hit', 's14':'double,hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  6:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'double,hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'double,hit', 's14':'double,hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  7:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'split,hit', 15:'hit', 16:'split,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  8:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'hit', 16:'split,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  9:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'hit', 16:'surrender,split,hit',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  10: {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'surrender,hit', 16:'surrender,split,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  }
}

DANO = {
  1:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'surrender,hit', 16:'surrender,split,hit',
    17:'surrender', 18:'stand', 19:'stand', 20:'stand',
    's12':'split,hit', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  },
  2:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'split,hit', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split,hit', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  3:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'double,hit', 10:'double,hit', 11:'double,hit', 12:'split,hit', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split,hit', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  4:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'double,hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  5:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'double,hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'double,hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'stand', 's20':'stand'
  },
  6:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'split,hit',
    9:'double,hit', 10:'double,hit', 11:'double,hit', 12:'split,stand', 13:'stand',
    14:'split,stand', 15:'stand', 16:'split,stand',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'double,hit', 's14':'double,hit', 's15':'double,hit', 's16':'double,hit',
    's17':'double,hit', 's18':'double,stand', 's19':'double,stand', 's20':'stand'
  },
  7:  {
    4:'split,hit', 5:'hit', 6:'split,hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'split,hit', 15:'hit', 16:'split,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  8:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'hit', 16:'split,hit',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'stand', 's19':'stand', 's20':'stand'
  },
  9:  {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'double,hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'hit', 16:'split,surrender,hit',
    17:'stand', 18:'split,stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  },
  10: {
    4:'hit', 5:'hit', 6:'hit', 7:'hit', 8:'hit',
    9:'hit', 10:'hit', 11:'double,hit', 12:'hit', 13:'hit',
    14:'hit', 15:'surrender,hit', 16:'split,surrender,hit',
    17:'stand', 18:'stand', 19:'stand', 20:'stand',
    's12':'split', 's13':'hit', 's14':'hit', 's15':'hit', 's16':'hit',
    's17':'hit', 's18':'hit', 's19':'stand', 's20':'stand'
  }
}

class SimpleBettingStrategy:
  class State:
    def getBet(self): return 100

    def getNextState(self, winnings, shoe):
      return self

  @staticmethod
  def createInitialState():
    return SimpleBettingStrategy.State()

class StreakBettingStrategy:
  class WinState:
    def getBet(self): return 1000

    def getNextState(self, winnings, shoe):
      return (StreakBettingStrategy.LoseState() if winnings<0 else self)

  class LoseState:
    def getBet(self): return 10

    def getNextState(self, winnings, shoe):
      return (StreakBettingStrategy.WinState() if winnings>0 else self)

  @staticmethod
  def createInitialState():
    return StreakBettingStrategy.LoseState()

class MemoryBettingStrategy():
  class MemoryState():
    # we must only modify the state in __init__ and nowhere else, since they are assumed immutable
    # (they can be reused later assuming to refer to the same state)
    def __init__(self, other=None, winnings=None):
      if other:
        self.lastTenWinnings = other.lastTenWinnings
        self.lastTenWinnings.append(winnings)
        if len(self.lastTenWinnings) > 10:
          self.lastTenWinnings.pop(0)
      else:
        self.lastTenWinnings = []
    def getBet(self):
      if len(self.lastTenWinnings) > 0:
        avg = sum(self.lastTenWinnings)/len(self.lastTenWinnings)
        assert(type(avg)==float)
        return (1000 if avg>0 else 10)
      else:
        return 10
    def getNextState(self, winnings, shoe):
      return MemoryBettingStrategy.MemoryState(self, winnings)

  @staticmethod
  def createInitialState():
    return MemoryBettingStrategy.MemoryState()

class AcesLeftBettingStrategy():
  class State():
    def __init__(self, acesLeft=32):
      self.acesLeft = acesLeft
    def getBet(self):
      return 1000 if self.acesLeft>16 else 10
    def getNextState(self, winnings, shoe):
      return AcesLeftBettingStrategy.State(shoe.getCardsLeft(1))
  @staticmethod
  def createInitialState():
    return AcesLeftBettingStrategy.State()
