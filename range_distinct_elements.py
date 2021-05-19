# https://www.spoj.com/problems/GIVEAWAY/

import unittest
import math
import bisect
from collections import defaultdict

class RangeDistinctElements:
  def __init__(self, a):
    """ Compute an auxillary array where each array value represents where that element in the original array is coming next.

    Args:
      a: Input array.
    """
    self.n = len(a)
    self.a = a
    self.nxt = [self.n] * self.n
    self.prev = [-1] * self.n
    self.b = int(math.sqrt(self.n))
    self.sz = int(math.ceil(self.n/self.b))
    self.pos = defaultdict(list)
    m = {}

    # Calculate next occurences for each element in the input array
    for i in range(self.n):
      if self.a[i] in m:
        self.nxt[m[self.a[i]]] = i
        self.prev[i] = m[self.a[i]]
      m[self.a[i]] = i
      self.pos[self.a[i]].append(i)

    # Divide next array into blocks and sort elements within each block
    self.blocks = []
    for i in range(self.sz):
      l, r = i*self.b, min(self.n-1, i*self.b+self.b-1)
      self.blocks.append(sorted(self.nxt[l:r+1]))

  def query(self, l, r):
    """ Query number of distinct elements in [l, r] in input array.

    Args:
      l - Left Index
      r - Right Index
    """
    l_block, r_block = l//self.b, r//self.b
    ans = 0

    for i in range(l, min(r, l_block*self.b+self.b-1)+1):
      if self.nxt[i] > r:
          ans += 1

    if l_block == r_block:
      return ans

    for block in range(l_block+1, r_block):
      ans += len(self.blocks[block]) - bisect.bisect_left(self.blocks[block], r+1)

    for i in range(r_block*self.b, r+1):
      if self.nxt[i] > r:
        ans += 1

    return ans

  def update(self, elem, i):
    """ Update value at index of input array to elem

    Args:
       elem : new value
       i: index at which new value needs to be updated
    """
    # If new and old values are same.
    if elem == self.a[i]:
      return    

    # Update next reference of prev occuring element.
    if self.prev[i] >= 0:
      self.nxt[self.prev[i]] = self.nxt[i]

    # Update prev reference of next occuring element.
    if self.nxt[i] < self.n:
      self.prev[self.nxt[i]] = self.prev[i]
   
    # Remove the current index from list of indexes where previous value is occuring
    self.pos[self.a[i]].remove(i)

    # Is there an occurence of new element in array
    if elem not in self.pos:
      self.nxt[i] = self.n
      self.prev[i] = -1
      return

    elem_pos = self.pos[elem]
    pos = bisect.bisect_left(elem_pos, i)

    # Update prev of new element at current index and next of prev occurence to current index
    if pos == 0:
      self.prev[i] = -1
    else:
      self.prev[i] = elem_pos[pos-1]
      self.nxt[elem_pos[pos-1]] = i

    # Update next of new element at current index and prev of next occurence to current index
    if pos == len(elem_pos):
      self.nxt[i] = self.n
    else:
      self.nxt[i] = elem_pos[pos]
      self.prev[elem_pos[pos]] = i

    # Update list indexes at which new element occurs. Also, new value at index i in the original array
    self.pos[elem].insert(pos, i)
    self.a[i] = elem

    # Update and resort the block in which new value is present
    block_no = i//self.b
    l, r = block_no*self.b, min(self.n-1, block_no*self.b+self.b-1)
    self.blocks[block_no] = sorted(self.nxt[l:r+1])

class TestDistinctRangeQuery(unittest.TestCase):
  def test_perfect_square(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5] 
    rde = RangeDistinctElements(a)
    self.assertEqual(rde.query(2, 6), 3)

  def test_non_perfect_square(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 7] 
    rde = RangeDistinctElements(a)
    self.assertEqual(rde.query(2, 7), 4)

  def test_equal_elements(self):
    a = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]  
    rde = RangeDistinctElements(a)
    self.assertEqual(rde.query(2, 7), 1)

  def test_distinct_elements(self):
    a = [4, 5, 6, 1, 2, 3, 7, 8, 9, 0] 
    rde = RangeDistinctElements(a)
    self.assertEqual(rde.query(2, 7), 6)

  def test_full_list(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 7] 
    rde = RangeDistinctElements(a)
    self.assertEqual(rde.query(0, 9), 6)

  def test_partial_list_1(self):
    a = [4, 6, 8, 9, 9, 9, 8, 4, 5, 7] 
    rde = RangeDistinctElements(a)
    self.assertEqual(rde.query(2, 9), 5)

  def test_partial_list_2(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 7] 
    rde = RangeDistinctElements(a)
    self.assertEqual(rde.query(0, 6), 4)

  def test_one_element_query(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 7] 
    rde = RangeDistinctElements(a)
    self.assertEqual(rde.query(6, 6), 1)

  def test_update(self):
    a = [4, 6, 8, 9, 6, 9, 8, 6, 5] 
    rde = RangeDistinctElements(a)
    self.assertEqual(rde.query(2, 6), 3)

    rde.update(9, 4)
    self.assertEqual(rde.query(2, 6), 2)

    rde.update(4, 4)
    self.assertEqual(rde.query(2, 6), 3)
    self.assertEqual(rde.query(0, 4), 4)

    rde.update(10, 4)
    self.assertEqual(rde.query(2, 6), 3)
    self.assertEqual(rde.query(0, 4), 5)
    self.assertEqual(rde.query(0, 8), 6)

if __name__ == '__main__':
  unittest.main()
