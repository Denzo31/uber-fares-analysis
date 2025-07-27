import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("="*50)
print("UBER FARES DATASET ANALYSIS")
print("="*50)

# 1. DATA LOADING AND UNDERSTANDING
print("\n1. LOADING THE DATASET...")
# Load your dataset (replace 'your_dataset.csv' with your actual file path)
df = pd.read_csv(r"C:\Users\educa\Downloads\shema derrick\uber.csv")


print(f"Dataset loaded successfully!")
print(f"Dataset shape: {df.shape}")
print(f"Total records: {df.shape[0]:,}")
print(f"Total features: {df.shape[1]}")

# 2. INITIAL DATA EXPLORATION
print("\n2. INITIAL DATA EXPLORATION")
print("-" * 30)

print("\nColumn Information:")
print(df.info())

print("\nDataset Structure:")
print(df.head(10))

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nDataset Description:")
print(df.describe())

# 3. DATA QUALITY ASSESSMENT
print("\n3. DATA QUALITY ASSESSMENT")
print("-" * 30)

print("\nMissing Values:")
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
missing_df = pd.DataFrame({
    'Column': missing_values.index,
    'Missing_Count': missing_values.values,
    'Missing_Percentage': missing_percentage.values
})
print(missing_df)

print("\nDuplicated Rows:")
print(f"Number of duplicated rows: {df.duplicated().sum()}")

print("\nUnique Values per Column:")
for col in df.columns:
    print(f"{col}: {df[col].nunique():,} unique values")

# 4. DATA CLEANING
print("\n4. DATA CLEANING")
print("-" * 20)

# Create a copy for cleaning
df_clean = df.copy()

# Convert pickup_datetime to datetime
print("Converting pickup_datetime to datetime format...")
df_clean['pickup_datetime'] = pd.to_datetime(df_clean['pickup_datetime'], utc=True)

# Remove rows with zero coordinates (likely invalid data)
print("Removing invalid coordinate data...")
initial_count = len(df_clean)
df_clean = df_clean[
    (df_clean['pickup_longitude'] != 0) & 
    (df_clean['pickup_latitude'] != 0) &
    (df_clean['dropoff_longitude'] != 0) & 
    (df_clean['dropoff_latitude'] != 0)
]
removed_coords = initial_count - len(df_clean)
print(f"Removed {removed_coords:,} rows with invalid coordinates")

# Remove negative fare amounts
print("Removing negative fare amounts...")
initial_count = len(df_clean)
df_clean = df_clean[df_clean['fare_amount'] > 0]
removed_fares = initial_count - len(df_clean)
print(f"Removed {removed_fares:,} rows with invalid fares")

# Remove unrealistic fare amounts (likely outliers)
print("Removing extreme fare outliers...")
Q1 = df_clean['fare_amount'].quantile(0.25)
Q3 = df_clean['fare_amount'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

initial_count = len(df_clean)
df_clean = df_clean[
    (df_clean['fare_amount'] >= lower_bound) & 
    (df_clean['fare_amount'] <= upper_bound)
]
removed_outliers = initial_count - len(df_clean)
print(f"Removed {removed_outliers:,} fare outliers")

# Remove invalid passenger counts
print("Cleaning passenger count data...")
initial_count = len(df_clean)
df_clean = df_clean[
    (df_clean['passenger_count'] > 0) & 
    (df_clean['passenger_count'] <= 6)
]
removed_passengers = initial_count - len(df_clean)
print(f"Removed {removed_passengers:,} rows with invalid passenger counts")

print(f"\nFinal cleaned dataset shape: {df_clean.shape}")
print(f"Total rows removed: {len(df) - len(df_clean):,}")
print(f"Data retention rate: {(len(df_clean)/len(df)*100):.2f}%")

# 5. FEATURE ENGINEERING
print("\n5. FEATURE ENGINEERING")
print("-" * 25)

# Extract time features
print("Creating time-based features...")
df_clean['pickup_hour'] = df_clean['pickup_datetime'].dt.hour
df_clean['pickup_day'] = df_clean['pickup_datetime'].dt.day
df_clean['pickup_month'] = df_clean['pickup_datetime'].dt.month
df_clean['pickup_year'] = df_clean['pickup_datetime'].dt.year
df_clean['pickup_dayofweek'] = df_clean['pickup_datetime'].dt.dayofweek
df_clean['pickup_weekday'] = df_clean['pickup_datetime'].dt.day_name()

# Create peak/off-peak indicators
def categorize_time_period(hour):
    if 7 <= hour <= 9 or 17 <= hour <= 19:
        return 'Peak'
    elif 22 <= hour <= 23 or 0 <= hour <= 5:
        return 'Late Night'
    else:
        return 'Off-Peak'

df_clean['time_period'] = df_clean['pickup_hour'].apply(categorize_time_period)

# Calculate trip distance using Haversine formula
def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

print("Calculating trip distances...")
df_clean['trip_distance_km'] = haversine_distance(
    df_clean['pickup_longitude'], df_clean['pickup_latitude'],
    df_clean['dropoff_longitude'], df_clean['dropoff_latitude']
)

# Calculate fare per km
df_clean['fare_per_km'] = df_clean['fare_amount'] / (df_clean['trip_distance_km'] + 0.001)  # Add small value to avoid division by zero

# Create season feature
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df_clean['season'] = df_clean['pickup_month'].apply(get_season)

print("Feature engineering completed!")
print(f"New features added: {len(df_clean.columns) - len(df.columns)}")

# 6. EXPLORATORY DATA ANALYSIS
print("\n6. EXPLORATORY DATA ANALYSIS")
print("-" * 35)

# Basic statistics
print("\nDescriptive Statistics for Key Variables:")
print("\nFare Amount Statistics:")
print(f"Mean: ${df_clean['fare_amount'].mean():.2f}")
print(f"Median: ${df_clean['fare_amount'].median():.2f}")
print(f"Standard Deviation: ${df_clean['fare_amount'].std():.2f}")
print(f"Min: ${df_clean['fare_amount'].min():.2f}")
print(f"Max: ${df_clean['fare_amount'].max():.2f}")

print("\nTrip Distance Statistics:")
print(f"Mean: {df_clean['trip_distance_km'].mean():.2f} km")
print(f"Median: {df_clean['trip_distance_km'].median():.2f} km")
print(f"Standard Deviation: {df_clean['trip_distance_km'].std():.2f} km")

print("\nPassenger Count Distribution:")
print(df_clean['passenger_count'].value_counts().sort_index())

print("\nTime Period Distribution:")
print(df_clean['time_period'].value_counts())

print("\nTop 10 Busiest Hours:")
hourly_rides = df_clean['pickup_hour'].value_counts().sort_index()
print(hourly_rides.head(10))

print("\nSeasonal Distribution:")
print(df_clean['season'].value_counts())

# 7. CORRELATION ANALYSIS
print("\n7. CORRELATION ANALYSIS")
print("-" * 25)

# Select numeric columns for correlation
numeric_cols = ['fare_amount', 'pickup_longitude', 'pickup_latitude', 
                'dropoff_longitude', 'dropoff_latitude', 'passenger_count',
                'pickup_hour', 'pickup_day', 'pickup_month', 'pickup_year',
                'trip_distance_km', 'fare_per_km']

correlation_matrix = df_clean[numeric_cols].corr()
print("\nCorrelation with Fare Amount:")
fare_correlations = correlation_matrix['fare_amount'].sort_values(ascending=False)
print(fare_correlations)

# 8. SAVE CLEANED DATASET
print("\n8. SAVING CLEANED DATASET")
print("-" * 30)

# Save the cleaned and enhanced dataset
output_filename = 'uber_fares_cleaned_enhanced.csv'
df_clean.to_csv(output_filename, index=False)
print(f"Cleaned dataset saved as: {output_filename}")
print(f"Final dataset shape: {df_clean.shape}")

# Create a summary of the cleaning process
cleaning_summary = {
    'Original_Records': len(df),
    'Final_Records': len(df_clean),
    'Records_Removed': len(df) - len(df_clean),
    'Retention_Rate': f"{(len(df_clean)/len(df)*100):.2f}%",
    'New_Features_Added': len(df_clean.columns) - len(df.columns),
    'Final_Features': len(df_clean.columns)
}

print("\n" + "="*50)
print("DATA CLEANING SUMMARY")
print("="*50)
for key, value in cleaning_summary.items():
    print(f"{key.replace('_', ' ')}: {value}")

print("\n" + "="*50)
print("ANALYSIS COMPLETE!")
print("="*50)
print("\nNext Steps:")
print("1. Import the cleaned CSV file into Power BI")
print("2. Create visualizations using the enhanced features")
print("3. Build your interactive dashboard")
print("4. Generate insights for your report")

# Display final column list
print(f"\nFinal Dataset Columns ({len(df_clean.columns)}):")
for i, col in enumerate(df_clean.columns, 1):
    print(f"{i:2d}. {col}")