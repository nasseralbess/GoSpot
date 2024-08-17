import numpy as np
from annoy import AnnoyIndex
import time

def create_sample_data(n_samples=1000, n_features=50):
    return np.random.random((n_samples, n_features)).astype('float32')

def build_annoy_index(data, n_trees=10):
    n_samples, n_features = data.shape
    index = AnnoyIndex(n_features, 'angular')
    
    start_time = time.time()
    
    print("Adding items to the index...")
    for i in range(n_samples):
        index.add_item(i, data[i])
    
    print("Building the index...")
    index.build(n_trees)
    
    end_time = time.time()
    print(f"Index built in {end_time - start_time:.2f} seconds")
    
    return index

def test_annoy_search(index, data, n_neighbors=5):
    print("Testing search functionality...")
    start_time = time.time()
    
    query = data[0]  # Use the first item as a query
    neighbors = index.get_nns_by_vector(query, n_neighbors)
    
    end_time = time.time()
    print(f"Search completed in {end_time - start_time:.4f} seconds")
    print(f"Nearest neighbors for the first item: {neighbors}")

if __name__ == "__main__":
    # Create sample data
    data = create_sample_data()
    print(f"Created sample data with shape: {data.shape}")
    
    # Build Annoy index
    index = build_annoy_index(data)
    
    # Test search functionality
    test_annoy_search(index, data)
    
    print("Script completed successfully!")