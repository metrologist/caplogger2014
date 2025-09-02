import matplotlib.pyplot as plt
print('simplest plot')
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

plt.plot(x, y)

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Simple Plot')

plt.show()