# -*- coding: utf-8 -*-

import time

from poly import *

class GB(list):
  def __init__(self):
    super(GB, self).__init__()

  def __str__(self):
    return ",\n".join(str(p) for p in self)

  def __repr__(self):
    return ",\n".join(repr(p) for p in self)

  def __addS(self, p1, p2):
    m = p1.lm().lcm(p2.lm())
    if m == p1.lm()*p2.lm():
      self.crit1 += 1
    else:
      if id(p1) <  id(p2):
        p1, p2 = p2, p1
      self.B.append((m, p1, p2))

  def __crit2(self, m, p1, p2):
    for g in self:
      if m.divisible(g.lm()) and id(p1) != id(g) and id(p2) != id(g):
        id1, id2 = (id(g), id(p1)) if id(g) > id(p1) else (id(p1), id(g))
        if not any(id(b[1]) == id1 and id(b[2]) == id2 for b in self.B):
          self.crit2 += 1
          return True
    return False

  def __insert(self, p):
    assert not self.find(p.lm())
    i = 0
    while i < len(self) and cmp(p.lm(), self[i].lm()) > 0:
      self.__addS(p, self[i])
      i += 1
    self.insert(i, p)
    i += 1
    while i < len(self):
      if self[i].lm().divisible(p.lm()):
        self.F.append(self.pop(i))
      else:
        self[i].NFtail(self)
        self[i].pp()
        self.__addS(p, self[i])
        i += 1
    assert self.assertValid()

  def find(self, m):
    for p in self:
      if m.divisible(p.lm()):
        return p

  def algorithm1(self, F):
    assert Monom.__cmp__ != Monom.alex
    self.time, self.crit1, self.crit2 = time.time(), 0, 0,
    self.F, self.B = F, []
    while F or self.B:
      p, i = None, 0
      while i < len(F):
        print(i, F[i].lm())
        F[i].NFhead(self)
        print('->', F[i].lm() if F[i] else '0')
        if not F[i]:
          del F[i]
        else:
          F[i].pp()
          if not p or cmp(F[i].lm(), p.lm()) < 0:
            p = F[i]
          i += 1
      if not p:
        self.B.sort()
        while self.B and not F:
          m, p1, p2 = self.B[0]
          if p1 and p2 and m == p1.lm().lcm(p2.lm()) and not self.__crit2(m, p1, p2):
            p = Poly.S(p1, p2)
            p.NFhead(self)
            if p:
              p.pp()
              F.append(p)
          del self.B[0]
      if p:
        if p.lm().degree() == 0:
          self = [Poly(1)]
          break
        F.remove(p)
        p.NFtail(self)
        p.pp()
        print("len(F) =", len(F), " p.lm() =", p.lm())
        self.__insert(p)
    del self.B
    del self.F
    self.time = time.time() - self.time

  def algorithm2(self, F):
    assert Monom.__cmp__ == Monom.deglex
    self.time, self.crit1, self.crit2 = time.time(), 0, 0,
    self.F, self.B = F, []
    while F or self.B:
      self.B.sort()
      while self.B:
        m, p1, p2 = self.B[0]
        if p1 and p2 and m == p1.lm().lcm(p2.lm()) and not self.__crit2(m, p1, p2):
          p = Poly.S(p1, p2)
          if p:
            p.pp()
            F.append(p)
        del self.B[0]
      p, i = None, 0
      while i < len(F):
        print(i, F[i].lm(),)
        F[i].NFhead(self)
        print('->', F[i].lm() if F[i] else '0')
        if not F[i]:
          del F[i]
        else:
          F[i].pp()
          if not p or cmp(F[i].lm(), p.lm()) < 0:
            p = F[i]
          i += 1
      if p:
        if p.lm().degree() == 0:
          self = [Poly(1)]
          break
        F.remove(p)
        p.NFtail(self)
        p.pp()
        print("len(F) =", len(F), " p.lm() =", p.lm())
        self.__insert(p)
    del self.B
    del self.F
    self.time = time.time() - self.time

  def assertValid(self):
    for i in range(len(self)-1):
      if not self[i] or cmp(self[i].lm(), self[i+1].lm()) >= 0:
        return False
    return not self or self[-1]

if __name__ == '__main__':
  print(sys.getsizeof(65535))
  print(sys.getsizeof(65535*65535))
  exit()
  Monom.variables = ['a', 'b', 'c']
  Monom.zero = Monom(0 for v in Monom.variables)
  Monom.__cmp__ = Monom.lex
  for i in range(len(Monom.variables)):
    p = Poly()
    p.append([Monom(0 if l != i else 1 for l in range(len(Monom.variables))), 1])
    globals()[Monom.variables[i]] = p

  G = GB()
  G.algorithm1([a**3 - b**2 + c - 1, b**3 - c**2 + a - 1, c**3 - a**2 + b - 1])
  print(G)
  print(", ".join(str(g.lm()) for g in G))
  print("crit1 =", G.crit1, "crit2 =", G.crit2)
  print("time %.2f" % G.time)

  #Monom.variables = ['x1', 'x2', 'x3', 'x4', 'x5']
  #Monom.zero = Monom(0 for v in Monom.variables)
  #Monom.__cmp__ = Monom.deglex
  #for i in range(len(Monom.variables)):
    #p = Poly()
    #p.append([Monom(0 if l != i else 1 for l in range(len(Monom.variables))), 1])
    #globals()[Monom.variables[i]] = p

  #G = GB()
  #G.algorithm2([
#x1 + x2 + x3 + x4 + x5,
#x1*x2 + x1*x5 + x2*x3 + x3*x4 + x4*x5,
#x1*x2*x3 + x1*x2*x5 + x1*x4*x5 + x2*x3*x4 + x3*x4*x5,
#x1*x2*x3*x4 + x1*x2*x3*x5 + x1*x2*x4*x5 + x1*x3*x4*x5 + x2*x3*x4*x5,
#x1*x2*x3*x4*x5 - 1
  #])
  #print G
  #print ", ".join(str(g.lm()) for g in G)
  #print "crit1 =", G.crit1, "crit2 =", G.crit2
  #print "time %.2f" % G.time

  #Monom.variables = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
  #Monom.zero = Monom(0 for v in Monom.variables)
  #Monom.__cmp__ = Monom.deglex
  #for i in range(len(Monom.variables)):
    #p = Poly()
    #p.append([Monom(0 if l != i else 1 for l in range(len(Monom.variables))), 1])
    #globals()[Monom.variables[i]] = p

  #G = GB()
  #G.algorithm2([
#x1 + x2 + x3 + x4 + x5 + x6,
#x1*x2 + x1*x6 + x2*x3 + x3*x4 + x4*x5 + x5*x6,
#x1*x2*x3 + x1*x2*x6 + x1*x5*x6 + x2*x3*x4 + x3*x4*x5 + x4*x5*x6,
#x1*x2*x3*x4 + x1*x2*x3*x6 + x1*x2*x5*x6 + x1*x4*x5*x6 + x2*x3*x4*x5 + x3*x4*x5*x6,
#x1*x2*x3*x4*x5 + x1*x2*x3*x4*x6 + x1*x2*x3*x5*x6 + x1*x2*x4*x5*x6 + x1*x3*x4*x5*x6 + x2*x3*x4*x5*x6,
#x1*x2*x3*x4*x5*x6 - 1
  #])
  #print G
  #print ", ".join(str(g.lm()) for g in G)
  #print "crit1 =", G.crit1, "crit2 =", G.crit2
  #print "time %.2f" % G.time


  #Monom.variables = ['x', 'y', 'z']
  #Monom.zero = Monom(0 for v in Monom.variables)
  #Monom.__cmp__ = Monom.deglex
  #for i in range(len(Monom.variables)):
    #p = Poly()
    #p.append([Monom(0 if l != i else 1 for l in range(len(Monom.variables))), 1])
    #globals()[Monom.variables[i]] = p

  #G = GB()
  #G.algorithm1([x*(-x**3+y*z**3), y**4*(y*z-1), y**6, x**4*y**2])
  #print
  #print G
  ##print ",\n".join(str(g.lm()) for g in G)
  #print "crit1 =", G.crit1, "crit2 =", G.crit2
  #print "time %.2f" % G.time
