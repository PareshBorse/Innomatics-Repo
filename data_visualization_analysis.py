import matplotlib.pyplot as plt
import seaborn as sns

# Load the merged data if not in memory (it is in memory as merged_df)
df = merged_df.copy()

# Convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)

# Extract time components
df['month'] = df['order_date'].dt.strftime('%Y-%m')
df['month_num'] = df['order_date'].dt.month
df['day_of_week'] = df['order_date'].dt.day_name()

# Order trends over time (Monthly Revenue and Order Count)
monthly_trends = df.groupby('month').agg({'order_id': 'count', 'total_amount': 'sum'}).rename(columns={'order_id': 'order_count', 'total_amount': 'revenue'}).reset_index()

# User behavior patterns
user_behavior = df.groupby('user_id').agg({'order_id': 'count', 'total_amount': 'mean'}).rename(columns={'order_id': 'order_frequency', 'total_amount': 'avg_spend'})

# City-wise performance
city_performance = df.groupby('city').agg({'order_id': 'count', 'total_amount': 'sum'}).rename(columns={'order_id': 'order_count', 'total_amount': 'revenue'}).sort_values(by='revenue', ascending=False).reset_index()

# Cuisine-wise performance
cuisine_performance = df.groupby('cuisine').agg({'order_id': 'count', 'total_amount': 'sum'}).rename(columns={'order_id': 'order_count', 'total_amount': 'revenue'}).sort_values(by='revenue', ascending=False).reset_index()

# Membership impact
membership_impact = df.groupby('membership').agg({'order_id': 'count', 'total_amount': ['sum', 'mean']})
membership_impact.columns = ['order_count', 'total_revenue', 'avg_order_value']
membership_impact = membership_impact.reset_index()

# Trend Plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_trends, x='month', y='revenue', marker='o', label='Revenue')
plt.title('Monthly Revenue Trend')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_revenue_trend.png')

# City Performance Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=city_performance, x='revenue', y='city', palette='viridis')
plt.title('Revenue by City')
plt.tight_layout()
plt.savefig('city_performance.png')

# Cuisine Performance Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=cuisine_performance, x='revenue', y='cuisine', palette='magma')
plt.title('Revenue by Cuisine')
plt.tight_layout()
plt.savefig('cuisine_performance.png')

# Membership Impact Plot
plt.figure(figsize=(8, 6))
sns.barplot(data=membership_impact, x='membership', y='avg_order_value', palette='coolwarm')
plt.title('Average Order Value by Membership')
plt.tight_layout()
plt.savefig('membership_impact_aov.png')

# Output summaries for the user
print("Monthly Trends Summary:")
print(monthly_trends)
print("\nCity Performance Summary:")
print(city_performance)
print("\nCuisine Performance Summary:")
print(cuisine_performance)
print("\nMembership Impact Summary:")
print(membership_impact)