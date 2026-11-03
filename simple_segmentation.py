# ==============================================================================
# PROJECT: E-COMMERCE CUSTOMER SEGMENTATION USING MACHINE LEARNING
# Pipeline: Data Preprocessing -> RFM -> Scaling -> K-Means -> DBSCAN -> PCA -> t-SNE -> Personas
# ==============================================================================
"""
CONCEPT OVERVIEW:
In e-commerce, customers have varying shopping cadences and spending habits.
This script demonstrates an end-to-end Unsupervised Learning workflow:
1. Preprocess raw transaction data (filter out cancelled/refunded orders).
2. Engineer RFM (Recency, Frequency, Monetary) metrics per customer.
3. Transform power-law distributions (np.log1p) and standardize (StandardScaler).
4. Perform K-Means clustering (using the Elbow Method to pick K=4).
5. Apply DBSCAN (density-based spatial clustering) to detect dense groups & noise.
6. Reduce dimensionality to 2D with PCA (linear) and t-SNE (non-linear manifold).
7. Profile cluster averages to assign meaningful marketing personas.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Non-interactive backend to save plots as images
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# ------------------------------------------------------------------------------
# STEP 1: LOAD AND CLEAN TRANSACTION DATA
# ------------------------------------------------------------------------------
# EXPLANATION:
# - The raw file 'orders.csv' is a transaction log where each row is an order.
# - We filter for status == 'completed' because refunded/cancelled orders do not
#   represent true customer spending or retained revenue.
# - We convert 'ordered_at' to datetime so we can perform calendar date arithmetic.

print("--- Step 1: Loading and Cleaning Data ---")
orders = pd.read_csv('dataset/rfm-analysis-customers-and-orders-for-e-commerce-segmentation-v1-csv-orders.csv')
print(f"Total raw orders in file: {len(orders)}")

# Keep only completed transactions
orders = orders[orders['status'] == 'completed'].copy()
orders['ordered_at'] = pd.to_datetime(orders['ordered_at'])
print(f"Cleaned completed orders: {len(orders)}")

# ------------------------------------------------------------------------------
# STEP 2: RFM FEATURE ENGINEERING
# ------------------------------------------------------------------------------
# EXPLANATION:
# Customer segmentation requires exactly ONE row per customer. We calculate:
# 1. Recency (R): Days since the customer's most recent purchase.
#    Formula: Reference Date (day after latest order) - max(order_date).
#    Interpretation: Lower is better (customer is actively engaged).
# 2. Frequency (F): Number of unique orders placed by the customer.
#    Interpretation: Higher is better (customer is loyal and repeats visits).
# 3. Monetary (M): Total dollar amount spent across all completed orders.
#    Interpretation: Higher is better (customer generates more revenue).

print("\n--- Step 2: Calculating RFM Features ---")
ref_date = orders['ordered_at'].max() + pd.Timedelta(days=1)
print(f"Snapshot Reference Date: {ref_date}")

rfm = orders.groupby('customer_id').agg(
    Recency=('ordered_at', lambda x: (ref_date - x.max()).days),
    Frequency=('order_number', 'nunique'),
    Monetary=('order_total', 'sum')
).reset_index()

print(f"Total unique customers: {len(rfm)}")
print(rfm.head())

# ------------------------------------------------------------------------------
# STEP 3: DATA TRANSFORMATION AND SCALING
# ------------------------------------------------------------------------------
# EXPLANATION:
# 1. Log Transformation (np.log1p):
#    E-commerce spend and order frequencies universally follow power-law (skewed)
#    distributions. A few high-spenders create extreme right tails. Log1p: ln(1 + x)
#    compresses the tail and normalizes the variance.
# 2. Standardization (StandardScaler):
#    Both K-Means and DBSCAN rely on Euclidean distance: sqrt(sum((x - y)^2)).
#    Without scaling, Monetary ($100s) would completely overpower Frequency (1-10),
#    reducing clustering to 1D spend. StandardScaler sets mean=0 and std=1 for all features.

print("\n--- Step 3: Scaling Features ---")
rfm_log = np.log1p(rfm[['Recency', 'Frequency', 'Monetary']])
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_log)
print("Features successfully log-transformed and standardized.")

# ------------------------------------------------------------------------------
# STEP 4: K-MEANS CLUSTERING (ELBOW METHOD & FITTING)
# ------------------------------------------------------------------------------
# EXPLANATION:
# K-Means partitions data into K spherical clusters by minimizing Within-Cluster
# Sum of Squares (WCSS / Inertia).
# - The Elbow Method plots WCSS against K. The "elbow" marks the point where
#   adding more clusters gives diminishing returns.
# - We select K=4 because it cleanly separates:
#   1. Active VIPs (Champions)
#   2. Lapsed VIPs (At-Risk High-Spenders)
#   3. New/Recent buyers (Occasional Buyers)
#   4. Dormant low-spend buyers (Hibernating)

print("\n--- Step 4: K-Means Clustering ---")
wcss = []
for k in range(1, 9):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(rfm_scaled)
    wcss.append(km.inertia_)

# Save elbow plot to disk
plt.figure(figsize=(6, 4))
plt.plot(range(1, 9), wcss, marker='o', color='#1f77b4')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia (WCSS)')
plt.grid(True)
plt.savefig('elbow_plot.png')
plt.close()
print("Saved Elbow Curve to 'elbow_plot.png'.")

# Fit K-Means with chosen K=4
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm['KMeans_Cluster'] = kmeans.fit_predict(rfm_scaled)

# ------------------------------------------------------------------------------
# STEP 5: DBSCAN CLUSTERING (DENSITY-BASED)
# ------------------------------------------------------------------------------
# EXPLANATION:
# DBSCAN groups points based on spatial density reachability:
# - eps: neighborhood radius around each point.
# - min_samples: minimum neighbors required within radius eps to form a core point.
# - Label -1: marks noise points / outliers that do not belong to dense clusters.
# Note: K-Means is better for business CRM because 100% of customers get assigned.

print("\n--- Step 5: DBSCAN Clustering ---")
dbscan = DBSCAN(eps=0.55, min_samples=4)
rfm['DBSCAN_Cluster'] = dbscan.fit_predict(rfm_scaled)

n_db_clusters = len(set(rfm['DBSCAN_Cluster'])) - (1 if -1 in rfm['DBSCAN_Cluster'] else 0)
n_db_noise = (rfm['DBSCAN_Cluster'] == -1).sum()
print(f"DBSCAN clusters found: {n_db_clusters}")
print(f"DBSCAN noise points (-1): {n_db_noise} ({n_db_noise/len(rfm)*100:.1f}%)")

# ------------------------------------------------------------------------------
# STEP 6: DIMENSIONALITY REDUCTION (PCA - LINEAR)
# ------------------------------------------------------------------------------
# EXPLANATION:
# PCA projects 3D RFM features onto 2 orthogonal axes of maximum variance.
# It is linear, deterministic, and preserves global data structure.

print("\n--- Step 6: PCA Dimensionality Reduction ---")
pca = PCA(n_components=2)
pca_coords = pca.fit_transform(rfm_scaled)
rfm['PCA1'] = pca_coords[:, 0]
rfm['PCA2'] = pca_coords[:, 1]
print(f"PCA Explained Variance Ratio: {pca.explained_variance_ratio_.round(3)}")

# ------------------------------------------------------------------------------
# STEP 7: MANIFOLD VISUALIZATION (t-SNE - NON-LINEAR)
# ------------------------------------------------------------------------------
# EXPLANATION:
# t-SNE converts distances to probabilities and visualizes non-linear clusters in 2D.
# IMPORTANT EXAM RULE:
# t-SNE is strictly a VISUALIZATION technique, NOT a clustering algorithm.
# Never cluster directly on t-SNE coordinates.

print("\n--- Step 7: t-SNE Visualization ---")
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
tsne_coords = tsne.fit_transform(rfm_scaled)
rfm['tSNE1'] = tsne_coords[:, 0]
rfm['tSNE2'] = tsne_coords[:, 1]

# Save side-by-side plot of PCA and t-SNE
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.scatterplot(data=rfm, x='PCA1', y='PCA2', hue='KMeans_Cluster', palette='tab10', ax=axes[0])
axes[0].set_title('PCA (2D Linear Projection)')
sns.scatterplot(data=rfm, x='tSNE1', y='tSNE2', hue='KMeans_Cluster', palette='tab10', ax=axes[1])
axes[1].set_title('t-SNE (2D Non-Linear Visualization)')
plt.tight_layout()
plt.savefig('pca_tsne_clusters.png')
plt.close()
print("Saved PCA & t-SNE side-by-side plot to 'pca_tsne_clusters.png'.")

# ------------------------------------------------------------------------------
# STEP 8: CLUSTER PROFILING & MARKETING PERSONAS
# ------------------------------------------------------------------------------
# EXPLANATION:
# To assign business personas, we compute average Recency, Frequency, and Monetary
# values per cluster and match them to marketing playbooks:
# - Low Recency, High Freq, High Spend  -> Champions (VIPs: reward with perks)
# - High Recency, High Freq, High Spend -> At-Risk High-Spenders (win-back offers)
# - Low Recency, Low Freq, Modest Spend -> Recent Occasional (onboarding sequence)
# - High Recency, Low Freq, Low Spend  -> Hibernating (cut ad spend, email clearance)

print("\n--- Step 8: Cluster Profiling & Actionable Personas ---")
profile = rfm.groupby('KMeans_Cluster').agg(
    Recency_Mean=('Recency', 'mean'),
    Frequency_Mean=('Frequency', 'mean'),
    Monetary_Mean=('Monetary', 'mean'),
    Count=('customer_id', 'count')
)
print("=== Cluster Profile Averages ===")
print(profile.round(2))

persona_map = {
    0: 'Hibernating Customers',
    1: 'Recent Occasional Buyers',
    2: 'At-Risk High-Spenders',
    3: 'Champions'
}

rfm['Persona'] = rfm['KMeans_Cluster'].map(persona_map)

print("\n=== Final Persona Customer Counts ===")
print(rfm['Persona'].value_counts())

# Save final customer-level dataset
rfm.to_csv('customer_segments.csv', index=False)
print("\n[SUCCESS] Saved customer-level results to 'customer_segments.csv'.")
print("All steps completed successfully!")
