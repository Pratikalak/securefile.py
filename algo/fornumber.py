import matplotlib.pyplot as plt

def term_n(n):
    return ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 10) % 18 - 9


a=1
terms = [term_n(n) for n in range(1, 1000000)]
print(terms)

plt.scatter(range(1, 1000000), terms, s=1)
plt.xlabel('n')
plt.ylabel('term_n')
plt.title('Graph of the First 50 Terms of the Sequence')
plt.show()
