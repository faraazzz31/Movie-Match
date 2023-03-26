def cosine_similarity(m1: list[int], m2: list[int]) -> int:
  """Returns the cosine similarity value between two lists.
  
  Preconditions:
  - len(m1) == len(m2)
  """
  dot = sum([m1[i] * m2[i] for i in range(0, len(m1))])
  n1 = sum([m1[i] ** 2 for i in range(0, len(m1))]) ** 0.5
  n2 = sum([m2[i] ** 2 for i in range(0, len(m2))]) ** 0.5
  
  return dot / (n1 * n2) 

if __name__ == '__main__':
  print("Hello World")
  for i in range(0, 5):
    print(i)
