# https://www.spoj.com/problems/GIVEAWAY/

import math
import bisect

class GiveAway:
  def __init__(self, N, arr):
    self.nums = arr
    self.N = N
    self.b = int(math.sqrt(N)) # Block Size
    self.sz = math.ceil(N/self.b) # Number of blocks
    self.blocks = []
    for i in range(self.sz):
      self.blocks.append(sorted([self.nums[i] for i in range(i*self.b, min(N, i*self.b+self.b))]))

  def update(self, index, val):
    block_no = index//self.b
    self.nums[index] = val
    self.blocks[block_no] = sorted([self.nums[i] for i in range(block_no*self.b, min(N, block_no*self.b+self.b))])

  def rangeQuery(self, left, right, val):
    l_block, r_block = left//self.b, right//self.b
    ans = 0

    for i in range(left, min(right, l_block*self.b+self.b-1)+1):
      if self.nums[i] >= val:
        ans += 1

    if l_block == r_block:
      print(ans)
      return

    for block in range(l_block+1, r_block):
      ans += len(self.blocks[block]) - bisect.bisect_left(self.blocks[block], val)

    for i in range(r_block*self.b, right+1):
      if self.nums[i] >= val:
        ans += 1 
    print(ans)

N = int(input())
nums = list(map(int, input().split()))
Q = int(input())
G = GiveAway(N, nums)

for _ in range(Q):
  query = list(map(int, input().split()))
  
  if query[0]: # update query
    G.update(query[1]-1, query[2])
  else:
    G.rangeQuery(query[1]-1, query[2]-1, query[3])
