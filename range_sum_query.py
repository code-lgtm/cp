# https://leetcode.com/problems/range-sum-query-mutable/ 

import math

class NumArray:
  def __init__(self, nums):
    self.nums = nums
    self.b = int(math.sqrt(len(nums))) # Block Size
    self.sz = math.ceil(len(nums)/self.b) # Number of blocks
    self.blocks = [0] * self.sz # Initialize blocks with zero sum
    for i in range(self.sz):
      self.blocks[i] += sum([self.nums[i] for i in range(i*self.b, min(len(nums), i*self.b+self.b))])

  def update(self, index, val):
    self.blocks[index//self.b] += val-self.nums[index]
    self.nums[index] = val

  def sumRange(self, left, right):
    l_block, r_block = left//self.b, right//self.b
    ans = 0

    # Right Index of Left Block : block_number * block_size + block_size - 1
    for i in range(left, min(right, l_block*self.b+self.b-1)+1)
      ans += self.nums[i]

    if l_block == r_block:
      return ans

    for block in range(l_block+1, r_block):
      ans += self.blocks[block]

    for i in range(r_block*self.b, right+1):
      ans += self.nums[i]

    return ans


def test():

  numArray = NumArray([1, 3, 5])
  assert(numArray.sumRange(0, 2) == 9)
  numArray.update(1, 2)
  assert(numArray.sumRange(0, 1) == 3)
  assert(numArray.sumRange(1, 2) == 7)
  assert(numArray.sumRange(1, 1) == 2)
  assert(numArray.sumRange(0, 0) == 1)
  assert(numArray.sumRange(2, 2) == 5)

  numArray = NumArray([0, 9, 5, 7, 3])
  assert(numArray.sumRange(4, 4) == 3)
  assert(numArray.sumRange(2, 4) == 15)


test()
