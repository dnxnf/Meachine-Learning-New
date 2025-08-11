import argparse

import torch
import torchvision
from torchvision import transforms, models
from PIL import Image
import matplotlib.pyplot as plt
import copy
import numpy as np

# 图像预处理
transform = transforms.Compose([
    transforms.Resize([224, 224]),
    transforms.ToTensor()
])
parser = argparse.ArgumentParser()
parser.add_argument('--content_img', type=str, default='./data/4.jpg', help='content image path')
parser.add_argument('--style_img', type=str, default='./data/1.jpg', help='style image path')

def loadimg(path=None):
    """加载并预处理图像，确保转换为RGB格式"""
    img = Image.open(path)
    # 添加图像模式转换
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = transform(img)
    img = img.unsqueeze(0)  # 增加batch维度
    return img


# 检查CUDA可用性
use_gpu = torch.cuda.is_available()
print(f"Using GPU: {use_gpu}")

# 加载内容图和风格图
content_img = loadimg("./data/4.jpg")
style_img = loadimg("./data/1.jpg")

if use_gpu:
    content_img = content_img.cuda()
    style_img = style_img.cuda()


# 初始化模型
cnn = torchvision.models.vgg16(weights=False)
weights_path = "D:/py/pycharmProjects/MachineLearning/CV-main/model/vgg16-397923af.pth"
state_dict = torch.load(weights_path)
cnn.load_state_dict(state_dict)

# 获取特征提取部分
cnn_features = cnn.features
cnn_features.eval()

if use_gpu:
    cnn_features = cnn_features.cuda()

# 配置损失层
content_layers = ["conv_3"]
style_layers = ["conv_1", "conv_2", "conv_3", "conv_4"]
content_losses = []
style_losses = []
content_weight = 10
style_weight = 1000


class ContentLoss(torch.nn.Module):
    """内容损失模块"""

    def __init__(self, weight, target):
        super().__init__()
        self.weight = weight
        self.register_buffer('target', target.detach() * weight)
        self.loss_fn = torch.nn.MSELoss()

    def forward(self, input):
        self.loss = self.loss_fn(input * self.weight, self.target)
        return input


class GramMatrix(torch.nn.Module):
    """计算Gram矩阵"""

    def forward(self, input):
        batch, channel, h, w = input.size()
        features = input.view(batch * channel, h * w)
        gram = torch.mm(features, features.t())
        return gram / (batch * channel * h * w)


class StyleLoss(torch.nn.Module):
    """风格损失模块"""

    def __init__(self, weight, target):
        super().__init__()
        self.weight = weight
        self.register_buffer('target', target.detach())
        self.loss_fn = torch.nn.MSELoss()
        self.gram = GramMatrix()

    def forward(self, input):
        self.Gram = self.gram(input.clone())
        self.loss = self.loss_fn(self.Gram, self.target) * self.weight
        return input


# 替换池化层
for i, layer in enumerate(cnn_features):
    if isinstance(layer, torch.nn.MaxPool2d):
        cnn_features[i] = torch.nn.AvgPool2d(kernel_size=2, stride=2, padding=0)

# 构建模型
model = torch.nn.Sequential()
conv_counter = 1

for layer in cnn_features.children():
    if isinstance(layer, torch.nn.Conv2d):
        name = f"conv_{conv_counter}"
        model.add_module(name, layer)

        if name in content_layers:
            target = model(content_img).detach()
            content_loss = ContentLoss(content_weight, target)
            model.add_module(f"content_loss_{conv_counter}", content_loss)
            content_losses.append(content_loss)

        if name in style_layers:
            gram = GramMatrix()
            if use_gpu:
                gram = gram.cuda()
            target = gram(model(style_img)).detach()
            style_loss = StyleLoss(style_weight, target)
            model.add_module(f"style_loss_{conv_counter}", style_loss)
            style_losses.append(style_loss)

        conv_counter += 1

    elif isinstance(layer, torch.nn.ReLU):
        model.add_module(f"relu_{conv_counter}", layer)

    elif isinstance(layer, (torch.nn.AvgPool2d, torch.nn.MaxPool2d)):
        model.add_module(f"pool_{conv_counter}", layer)

if use_gpu:
    model = model.cuda()

# 优化过程
input_img = content_img.clone().requires_grad_(True)
# optimizer = torch.optim.LBFGS([input_img])
optimizer = torch.optim.Adam([input_img], lr=0.01, betas=[0.99, 0.999])

epochs = 1000
for epoch in range(1, epochs + 1):
    def closure():
        optimizer.zero_grad()
        model(input_img)

        style_score = 0
        content_score = 0

        for sl in style_losses:
            style_score += sl.loss
        for cl in content_losses:
            content_score += cl.loss

        total_loss = style_score + content_score
        total_loss.backward()

        if epoch % 50 == 0:
            print(f"Epoch: {epoch} Style Loss: {style_score.item():.4f} Content Loss: {content_score.item():.4f}")

        return total_loss


    optimizer.step(closure)
    input_img.data.clamp_(0, 1)

# 结果处理与显示
output_img = input_img.detach().cpu().squeeze(0).permute(1, 2, 0).numpy()

plt.figure(figsize=(10, 5))
plt.imshow(np.clip(output_img, 0, 1))
plt.axis('off')
plt.tight_layout()
plt.show()