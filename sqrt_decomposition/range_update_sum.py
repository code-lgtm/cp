import unittest
import math

class RangeUpdates:
  def __init__(self, nums):
    self.nums = nums
    self.b = int(math.sqrt(len(nums))) # Block Size
    self.sz = math.ceil(len(nums)/self.b) # Number of blocks
    self.blocks = [0] * self.sz # Initialize blocks with zero sum
    for i in range(self.sz):
      self.blocks[i] += sum([self.nums[i] for i in range(i*self.b, min(len(nums), i*self.b+self.b))])
    self.lazy = [0 for _ in  range(self.sz)]

  def update(self, left, right, x):
    l_block, r_block = left//self.b, right//self.b
    for i in range(left, min(right, l_block*self.b+self.b-1)+1):
      self.nums[i] += x
      self.blocks[l_block] += x # Update sum for the left block

    if l_block == r_block:
      return

    for block in range(l_block+1, r_block):
      self.lazy[block] += x*self.b # Lazily Store sum of block

    for i in range(r_block*self.b, right+1):
      self.nums[i] += x
      self.blocks[r_block] += x # Update sum for the right block

  def query(self, left, right):
    l_block, r_block = left//self.b, right//self.b
    ans = 0

    for i in range(left, min(right, l_block*self.b+self.b-1)+1):
      ans += self.nums[i]
    ans += self.lazy[l_block]

    if l_block == r_block:
      return ans
    
    for block in range(l_block+1, r_block):
      ans += self.lazy[block]
      ans += self.blocks[block]

    for i in range(r_block*self.b, right+1):
      ans += self.nums[i]
    ans += self.lazy[r_block]

    return ans

class TestRangeUpdate(unittest.TestCase):
  def test_update_same_block(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5] 
    ru = RangeUpdates(a)
    self.assertEqual(ru.query(3, 5), 24)
    self.assertEqual(ru.query(2, 5), 32)
    ru.update(3, 4, 2)
    self.assertEqual(ru.query(3, 5), 28)
    self.assertEqual(ru.query(2, 5), 36)

  def test_update_single_element(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 8] 
    ru = RangeUpdates(a)
    ru.update(0, 0, 2)
    self.assertEqual(ru.query(0, 5), 44)
    self.assertEqual(ru.query(1, 5), 38)

  def test_update_complete_array(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 8] 
    ru = RangeUpdates(a)
    ru.update(0, 9, 3)
    self.assertEqual(ru.query(0, 9), 97)
    self.assertEqual(ru.query(1, 5), 53)

  def test_left_subarray(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 8] 
    ru = RangeUpdates(a)
    ru.update(0, 4, 1)
    self.assertEqual(ru.query(1, 5), 42)
    self.assertEqual(ru.query(0, 2), 21)

  def test_right_subarray(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 8] 
    ru = RangeUpdates(a)
    ru.update(5, 9, 1)
    self.assertEqual(ru.query(4, 9), 45)

  def test_last_block(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 8, 3] 
    ru = RangeUpdates(a)
    ru.update(9, 10, 2)
    self.assertEqual(ru.query(8, 10), 20)
