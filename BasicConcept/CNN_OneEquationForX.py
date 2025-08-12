import torch
import matplotlib.pyplot as plt

# 1. 输入方程参数
# ax+b+cx
a = float(input("请输入第一个方程的系数a（例如：2）: "))
b = float(input("请输入第一个方程的截距b（例如：1）: "))
c = float(input("请输入第二个方程的系数c（例如：1）: "))

# 2. 计算真实解
if a != c:
    x_true = (b) / (c - a)
else:
    print('No solution (a == c)')
    exit()

# 3. 初始化参数
x = torch.tensor([1.0], requires_grad=True)  # 初始值设为1
learning_rate = 0.1  # 初始学习率
num_epochs = 1000  # 迭代次数

# 4. 记录x的收敛过程
x_history = []

# 5. 梯度下降迭代
for epoch in range(num_epochs):
    # 计算预测值
    x_pred = x

    # 计算损失（与真实值的差）
    loss = torch.pow(x_pred - x_true, 2)  # 平方损失函数

    # 反向传播计算梯度
    loss.backward()

    # 更新参数
    with torch.no_grad():
        # x=x−lr×(∂x/∂loss)
        x -= learning_rate * x.grad
        x.grad.zero_()  # 清空梯度

    # 记录当前x的预测值
    x_history.append(x.item())

    # 打印每100轮的信息
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, Predicted x: {x.item():.4f}')

# 6. 输出结果
print(f'True solution: x = {x_true:.4f}')
print(f'Predicted solution: x = {x.item():.4f}')

# 7. 绘制x的收敛过程
plt.figure(figsize=(10, 6))
plt.plot(x_history, label='Predicted x')
plt.axhline(y=x_true, color='r', linestyle='--', label='True x')
plt.xlabel('Epoch')
plt.ylabel('x')
plt.title('Convergence of Predicted x to True Solution')
plt.legend()
plt.show()