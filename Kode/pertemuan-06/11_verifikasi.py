"""Pemeriksaan tambahan seluruh pasangan dan identitas penting."""
from ztools import *

a = 0.6
n = np.arange(200)
z = 1.4*np.exp(0.3j)
for values, expected in [
    (np.ones_like(n), z/(z-1)),
    (n, z/(z-1)**2),
    (n*n, z*(z+1)/(z-1)**3),
    (n**3, z*(z*z+4*z+1)/(z-1)**4),
    (a**n, z/(z-a)),
    (n*a**n, a*z/(z-a)**2),
    (n*n*a**n, a*z*(z+a)/(z-a)**3),
    (n**3*a**n, a*z*(z*z+4*a*z+a*a)/(z-a)**4),
    (np.sin(0.7*n), z*np.sin(0.7)/(z*z-2*z*np.cos(0.7)+1)),
    (np.cos(0.7*n), z*(z-np.cos(0.7))/(z*z-2*z*np.cos(0.7)+1)),
]:
    cocok(zt(values, n, z), expected)
nl = -np.arange(1, 201)
zl = 0.2*np.exp(0.4j)
cocok(zt(-nl*a**nl, nl, zl), a*zl/(zl-a)**2)
print('Seluruh pasangan pada tabel yang diuji sesuai.')
# Perkalian waktu melalui integral domain z untuk dua eksponensial kausal.
a, b = 0.5, 0.4
z = 1.2*np.exp(0.3j)
v = 0.7*np.exp(2j*np.pi*np.arange(2048)/2048)
product = np.mean((v/(v-a))*((z/v)/(z/v-b)))
cocok(product, z/(z-a*b))
print('Integral domain Z dari perkalian dua eksponensial sesuai.')
# Nilai akhir yang memenuhi syarat pole.
zz = 1+1e-7
cocok((1-1/zz)*zz/(zz-1), 1, 1e-7)
cocok((1-1/zz)*zz/(zz-0.5), 0, 1e-6)
# Respons persamaan selisih pada n>=0 dengan keadaan awal tak nol.
N = 30
y = np.empty(N)
prev = 3.0
for i in range(N):
    y[i] = 0.5*prev+2
    prev = y[i]
m = np.arange(N)
zero_state = 4*(1-0.5**(m+1))
initial_part = 1.5*0.5**m
cocok(y, zero_state+initial_part)
print('Respons keadaan nol dan kontribusi keadaan awal sesuai.')
print('SEMUA PEMERIKSAAN BERHASIL.')
