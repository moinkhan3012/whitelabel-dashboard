import pandas as pd

class DataAnalysis:
    def __init__(self, data_path, product_id):
        self.data_path = data_path
        self.product_id = product_id
        self.product_matrix_df = pd.read_csv(data_path)
    
    def find_top_similar_products(self, top_n=3):
        filtered_df = self.product_matrix_df[(self.product_matrix_df['product_1'] == self.product_id) | (self.product_matrix_df['product_2'] == self.product_id)]
        
        # Calculating combined similarity score: as just the addition of 3 fields for now
        filtered_df['combined_score'] = filtered_df['text_short'] + filtered_df['text_long'] + filtered_df['image']
        
        sorted_df = filtered_df.sort_values(by='combined_score', ascending=False)
        
        top_similar_products = sorted_df[sorted_df['product_1'] != self.product_id].head(top_n)
        
        print(top_similar_products)

        return top_similar_products

