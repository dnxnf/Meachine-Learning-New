# 八种激活函数常见图像
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-4, 4, 200)
plt.figure(figsize=(15, 10))

# 1. Sigmoid
plt.subplot(2, 4, 1)
plt.plot(x, 1 / (1 + np.exp(-x)))
plt.title("Sigmoid")

# 2. Tanh
plt.subplot(2, 4, 2)
plt.plot(x, np.tanh(x))
plt.title("Tanh")

# 3. ReLU
plt.subplot(2, 4, 3)
plt.plot(x, np.maximum(0, x))
plt.title("ReLU")

# 4. LeakyReLU
plt.subplot(2, 4, 4)
plt.plot(x, np.where(x >= 0, x, 0.01 * x))
plt.title("LeakyReLU (α=0.01)")

# 5. Swish
plt.subplot(2, 4, 5)
plt.plot(x, x * (1 / (1 + np.exp(-x))))
plt.title("Swish")

# 6. GELU
plt.subplot(2, 4, 6)
plt.plot(x, 0.5 * x * (1 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3))))
plt.title("GELU")

# 7. ELU
plt.subplot(2, 4, 7)
alpha = 1.0
plt.plot(x, np.where(x >= 0, x, alpha * (np.exp(x) - 1)))
plt.title("ELU (α=1.0)")

# 8. Softmax (需多输入演示)
plt.subplot(2, 4, 8)
x_softmax = np.array([1.0, 2.0, 3.0])
plt.bar(range(3), np.exp(x_softmax) / np.sum(np.exp(x_softmax)))
plt.title("Softmax (示例输入)")

plt.tight_layout()
plt.show()