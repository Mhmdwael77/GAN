import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd

data = pd.read_csv("data.csv").values
data = torch.tensor(data, dtype=torch.float32)

latent_dim = 100

class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 784),
            nn.Tanh()
        )

    def forward(self, z):
        return self.model(z)

class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

generator = Generator()
discriminator = Discriminator()

criterion = nn.BCELoss()
optimizer_G = optim.Adam(generator.parameters(), lr=0.0002)
optimizer_D = optim.Adam(discriminator.parameters(), lr=0.0002)

epochs = 10
batch_size = 64

for epoch in range(epochs):
    for i in range(0, len(data), batch_size):
        real = data[i:i+batch_size]
        current_batch = real.size(0)

        valid = torch.ones(current_batch, 1)
        fake = torch.zeros(current_batch, 1)

        z = torch.randn(current_batch, latent_dim)
        gen_imgs = generator(z)
        g_loss = criterion(discriminator(gen_imgs), valid)

        optimizer_G.zero_grad()
        g_loss.backward()
        optimizer_G.step()

        real_loss = criterion(discriminator(real), valid)
        fake_loss = criterion(discriminator(gen_imgs.detach()), fake)
        d_loss = (real_loss + fake_loss) / 2

        optimizer_D.zero_grad()
        d_loss.backward()
        optimizer_D.step()

    print(f"Epoch {epoch+1}/{epochs} | D Loss: {d_loss.item()} | G Loss: {g_loss.item()}")

print("Training finished.")