import unittest
import math
import bisect

def pre_compute_nxt(a):
  """ Compute an auxillary array where each array value represents where that element in the original array is coming next.

  Args:
    a: Input array.

  Returns:
    auxillary array with the characteristics described above
  """
  n = len(a)
  nxt = [n] * n
  m = {}

  for i in range(n):
    if a[i] in m:
      nxt[m[a[i]]] = i
    m[a[i]] = i
  
  return nxt 

def pre_compute_block_unique_elements(a):
  """ Divide input array into blocks and sort elements within blocks

  Args:
    a: Input Array

  Returns:
    blocks: array with sorted elements in each block
  """
  n = len(a)
  b = int(math.sqrt(n))
  sz = int(math.ceil(n/b))

  blocks = []
  for i in range(sz):
    l, r = i*b, min(n-1, i*b+b-1)
    blocks.append(sorted(a[l:r+1])) 
  
  return blocks

def distinct_elements(a, l, r):
  n = len(a)
  b = int(math.sqrt(n))

  # Calculate next occurences for each element in the input array
  nxt = pre_compute_nxt(a)

  # Divide next array into blocks and sort elements within each block
  blocks = pre_compute_block_unique_elements(nxt)

  l_block, r_block = l//b, r//b
  ans = 0

  for i in range(l, min(r, l_block*b+b-1)+1):
    if nxt[i] > r:
        ans += 1

  if l_block == r_block:
    return ans

  for block in range(l_block+1, r_block):
    ans += len(blocks[block]) - bisect.bisect_left(blocks[block], r+1)

  for i in range(r_block*b, r+1):
    if nxt[i] > r:
      ans += 1

  return ans


class TestDistinctRangeQuery(unittest.TestCase):
  def test_perfect_square(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5] 
    self.assertEqual(distinct_elements(a, 2, 6), 3)

  def test_non_perfect_square(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 7] 
    self.assertEqual(distinct_elements(a, 2, 7), 4)

  def test_equal_elements(self):
    a = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4] 
    self.assertEqual(distinct_elements(a, 2, 7), 1)

  def test_distinct_elements(self):
    a = [4, 5, 6, 1, 2, 3, 7, 8, 9, 0] 
    self.assertEqual(distinct_elements(a, 2, 7), 6)

  def test_full_list(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 7] 
    self.assertEqual(distinct_elements(a, 0, 9), 6)

  def test_partial_list_1(self):
    a = [4, 6, 8, 9, 9, 9, 8, 4, 5, 7] 
    self.assertEqual(distinct_elements(a, 2, 9), 5)

  def test_partial_list_2(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 7] 
    self.assertEqual(distinct_elements(a, 0, 6), 4)

  def test_one_element_query(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 7] 
    self.assertEqual(distinct_elements(a, 6, 6), 1)

  def test_pre_compute_nxt(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 7] 
    self.assertEqual(pre_compute_nxt(a), [7, 4, 6, 5, 10, 10, 10, 10, 10, 10])

    a = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4] 
    self.assertEqual(pre_compute_nxt(a), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

  def test_block_unique_elements(self):
    a = [4, 6, 8, 9, 6, 9, 8, 4, 5, 7] 
    self.assertEqual(pre_compute_block_unique_elements(a), [[4, 6, 8], [6, 9, 9], [4, 5, 8], [7]])

    a = [4, 6, 8, 9, 6, 9, 8, 4, 5] 
    self.assertEqual(pre_compute_block_unique_elements(a), [[4, 6, 8], [6, 9, 9], [4, 5, 8]])

if __name__ == '__main__':
  unittest.main()
