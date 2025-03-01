import matplotlib.pyplot as plt

a = 9999
result = []
for n in range(1,a):
    term = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 10) % 18 - 9
    result.append(term)

print(result)


plt.plot(range(1, a), result, linewidth=0.1)
plt.xlabel('n')
plt.ylabel('term_n')
plt.title('Graph of the First 50 Terms of the Sequence')
plt.show()
