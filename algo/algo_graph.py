import matplotlib.pyplot as plt
a=1
def term_n(n,a):
  return ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 25) % 50 - 25
terms = [term_n(n,a) for n in range(1, 10000)]
print(terms)

plt.scatter(range(1, 10000), terms, s=2)
plt.xlabel('n')
plt.ylabel('term_n')
plt.title('Graph of the First 50 Terms of the Sequence')
plt.show()
