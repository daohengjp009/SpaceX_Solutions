# Flight Number vs. Launch Site Analysis

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Create scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='FlightNumber', y='LaunchSite', 
                hue='Class', style='Class',
                palette={0: 'red', 1: 'blue'},
                markers={0: 'X', 1: 'o'})

plt.title('Flight Number vs. Launch Site')
plt.xlabel('Flight Number')
plt.ylabel('Launch Site')
plt.grid(True)
plt.legend(title='Landing Success', 
           labels=['Failed', 'Successful'])
plt.tight_layout()
plt.show()
```

## Plot Explanation

This scatter plot visualizes the relationship between flight numbers and launch sites, with color and marker style indicating landing success (blue circles for successful landings, red X's for failures). The plot reveals several important patterns:

1. **Launch Site Distribution**: Shows how launches are distributed across different SpaceX launch sites (CCAFS SLC 40, VAFB SLC 4E, KSC LC 39A)

2. **Temporal Pattern**: The increasing flight numbers on the x-axis represent the chronological progression of launches, allowing us to see how launch frequency and success rates evolved over time at each site

3. **Success Rate Visualization**: The color coding makes it easy to identify patterns in landing success rates across different launch sites and over time

4. **Site-Specific Trends**: Helps identify if certain launch sites show improving or declining success rates as flight numbers increase

This visualization is particularly useful for understanding the historical progression of SpaceX's launch operations and identifying any site-specific patterns in landing success. 