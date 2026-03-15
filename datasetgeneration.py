import numpy as np
import pandas as pd

data = np.random.rand(1000, 784)

df = pd.DataFrame(data)
df.to_csv("data.csv", index=False)

print("Dataset saved as data.csv")