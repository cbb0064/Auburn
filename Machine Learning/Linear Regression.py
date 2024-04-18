import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the csv file as a DataFrame
data = pd.read_csv("numpydataset.csv")
# Display the first 5 rows in the dataset
data.head()

# Calculating number of samples
samples = len(data)

def MSE(points, m, b):
    totalError = 0
    for i in range(0, len(points)):
        x = points.iat[i, 0]  # Assumes first column as feature
        y = points.iat[i, 1]  # Assumes second column as target
        totalError += (y - (m * x + b)) ** 2
    return totalError / float(len(points))

def gradient_descent(m_current, b_current, points, learning_rate):
    m_gradient = 0
    b_gradient = 0
    N = float(len(points))
    for i in range(0, len(points)):
        x = points.iat[i, 0]
        y = points.iat[i, 1]
        m_gradient += -(2/N) * x * (y - ((m_current * x) + b_current))
        b_gradient += -(2/N) * (y - ((m_current * x) + b_current))

    m_updated = m_current - (learning_rate * m_gradient)
    b_updated = b_current - (learning_rate * b_gradient)
    return m_updated, b_updated

m, b = 0, 0  # initial parameters
L = 0.001    # initial learning rate
epochs = 100 # number of iterations over the dataset

for epoch in range(1, epochs+1):
    m, b = gradient_descent(m, b, data, L)
    loss = MSE(data, m, b)
    print(f"Epoch {epoch}, m: {m}, b:{b}, Loss: {loss}")

# Plotting the first graph
fig, ax = plt.subplots(1,1)
ax.scatter(data.Features, data.Targets, color="red", linewidths=0.5, label="Points")
ax.plot(data.Features, [m * x + b for x in data.Features], linewidth=3, linestyle="dashed", label="$ f(x) = mx+c $")
ax.legend(loc="lower right", bbox_to_anchor=(.96, 0.0))
ax.set_xlabel("Features")
ax.set_ylabel("Targets")
plt.savefig('LinearRegression001.png')
plt.close()

# Reset parameters for new learning rate
m, b = 0, 0
L = 0.01   # new learning rate
epochs = 100

for epoch in range(1, epochs+1):
    m, b = gradient_descent(m, b, data, L)
    loss = MSE(data, m, b)
    print(f"Epoch {epoch}, m: {m}, b:{b}, Loss: {loss}")

# Plotting the second graph
fig, ax = plt.subplots(1,1)
ax.scatter(data.Features, data.Targets, color="red", linewidths=0.5, label="Points")
ax.plot(data.Features, [m * x + b for x in data.Features], linewidth=3, linestyle="dashed", label="$ f(x) = mx+c $")
ax.legend(loc="lower right", bbox_to_anchor=(.96, 0.0))
ax.set_xlabel("Features")
ax.set_ylabel("Targets")
plt.savefig('LinearRegression01.png')
plt.close()
