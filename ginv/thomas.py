try:
  from .janet import *
except ImportError:
  from janet import *

class Thomas:
  def __init__(self):
    self.__reduction = 0
    self.__count = 0
    self.elems = []
    self.bylm = {}
    self.h = None

  def is_forest(self):
    return False

  def findWrap(self, m):
    if self.elems:
      assert self.pos == m.position()
      w = self.bylm.get(tuple(map(min, m, self.h)))
      if w:
        self.__reduction += 1
      return w

  def find(self, m):
    w = self.findWrap(m)
    return w.poly if w else None

  def __iter__(self):
    return iter(list(self.elems))

  def GB(self):
    return (w for w in self.elems if w.isGB())

  def __insert(self, w, lst):
    assert isinstance(w, Wrap)
    if not self.elems:
      self.pos = w.lm.position()
    assert self.pos == w.lm.position()

    keep = []
    for u in self.elems:
      if u.lm.divisibleTrue(w.lm):
        lst.append(u)
      else:
        keep.append(u)
    self.elems = keep + [w]
    self.__count += 1

  def __refresh(self):
    self.h = [max(d) for d in zip(*(w.lm for w in self.elems))]
    self.bylm = {tuple(w.lm): w for w in self.elems}
    for w in self.elems:
      w.nonmult[:] = [d < h for d, h in zip(w.lm, self.h)]

  def insert(self, q):
    lst = []
    for w in q:
      self.__insert(w, lst)
    self.__refresh()
    self.__count -= len(lst)
    return lst

  def degMinProlong(self):
    d = 0
    for w in self:
      for v, f in enumerate(w.nonmult):
        if f and not w.prolong[v]:
          d = min(d, w.degree()) if d else w.degree()
    return d

  def prolong(self, d):
    r = []
    for w in self:
      if d == 0 or d == w.degree():
        for v, f in enumerate(w.nonmult):
          if f and not w.prolong[v]:
            r.append(Wrap(w, v))
    return r

  def reduction(self):
    return self.__reduction

  def count(self):
    return self.__count

  def HP(self):
    hp = HilbertPoly(len(Monom._Monom__var))
    for w in self:
      hp -= CombRepet(w.multi() + 1, w.degree())
    return hp
