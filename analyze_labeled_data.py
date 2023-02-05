"""
This python program analyzes the labeled data and makes a graph from it
"""

from os import path, getcwd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

data = path.join(getcwd(), 'labeled_data.csv')
df = pd.read_csv(data, sep=';')

# Filter data
df = df[df['Type decision'] != 'Duplicate']
df['Type decision'] = df['Type decision'].str.strip()


group_labels = []
grouped_executive = []
grouped_existence = []
grouped_property = []

# Count decisions
executive_count = 0
existence_count = 0
property_count = 0
for i in range(499):
    if 'Executive' == df['Type decision'].iloc[i]:
        executive_count += 1
    if 'Existence' == df['Type decision'].iloc[i]:
        existence_count += 1
    if 'Property' == df['Type decision'].iloc[i]:
        property_count += 1

print(existence_count, executive_count, property_count)

# Count decisions
for i in range(50):
    grouped_labels = df['Type decision'].iloc[i * 10:(i * 10) + 10].value_counts()

    executive_count = 0
    existence_count = 0
    property_count = 0

    if 'Executive' in grouped_labels:
        executive_count = grouped_labels['Executive']
    if 'Existence' in grouped_labels:
        existence_count = grouped_labels['Existence']
    if 'Property' in grouped_labels:
        property_count = grouped_labels['Property']

    grouped_executive.append(executive_count)
    grouped_existence.append(existence_count)
    grouped_property.append(property_count)
    group_labels.append(i * 10)


grouped_executive = np.array(grouped_executive)
grouped_existence = np.array(grouped_existence)
grouped_property = np.array(grouped_property)

# Calculate correlation
grouped_probability = []
i = 0
while i < len(df.Probability):
    val = np.mean(df.Probability[i:i + 10])
    grouped_probability.append(val)
    i += 10

total_decisions = np.array(grouped_executive + grouped_existence + grouped_property)

# Get variance
covariance = np.cov(total_decisions, grouped_probability)
print(covariance)

# Get Pearson's correlation
print(pearsonr(total_decisions, grouped_probability))

# Plot data
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

plt.xlabel('Commit number')
plt.ylabel('Probability')

fig, ax = plt.subplots()
width = 6
ax.bar(group_labels, grouped_executive, width, label='Executive', color='blue')
ax.bar(group_labels, grouped_existence, width, bottom=grouped_executive, label='Existence', color='green')
ax.bar(group_labels, grouped_property, width, bottom=grouped_executive + grouped_existence, label='Property', color='cyan')
ax.set_ylabel("Decision types found", color="blue", fontsize=10)
ax.set_xlabel("Issues", color="black", fontsize=10)
ax.legend(loc='upper right')


ax2 = ax.twinx()
ax2.plot(df.Probability, color="red")
ax2.set_ylabel("Probability", color="red", fontsize=10)

plt.show()

