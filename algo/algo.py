def term_n(n):
  return ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 25) % 50 - 25

a=1
terms = [term_n(n) for n in range(1, 501)]
print(terms)