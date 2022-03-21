# -*- coding: utf-8 -*-

class 三角:
   def __init__(self,n) -> None:
      self.行 = n
      self.list = [[1]]
      i=0
      while i<self.行:
         self.添加list()
         i+=1

   def 添加list(self):
      l2 = self.list[len(self.list)-1]
      l3 = [1]
      for index,item in enumerate(l2):
         n = l2[index+1] if index<len(l2)-1 else 0
         l3.append(item+n)
      print("单行",l3)
      self.list.append(l3)



if __name__ == "__main__":
   o = 三角(10)
   print(o.list)


