import pandas as pd

class DataAnalysis:
    """
    A class to analyze product similarity based on a provided data matrix.

    Attributes:
        data_path (str): The path to the data file.
        product_id (str): The ID of the product to analyze.
        product_matrix_df (DataFrame): The dataframe containing product similarity data.
    """

    def __init__(self, data_path, product_id):
        """
        Initializes the DataAnalysis class.

        Args:
            data_path (str): The path to the data file.
            product_id (str): The ID of the product to analyze.
        """
        self.data_path = data_path
        self.product_id = product_id
        self.product_matrix_df = pd.read_csv(data_path)

    def find_top_similar_products(self, top_n=3):
        """
        Finds the top similar products for the specified product ID.

        Args:
            top_n (int): The number of top similar products to return. Defaults to 3.

        Returns:
            DataFrame: A DataFrame containing the top similar products.
        """
        # Filter the dataframe to include only rows involving the given product ID
        filtered_df = self.product_matrix_df[
            (self.product_matrix_df['product_1'] == self.product_id) | 
            (self.product_matrix_df['product_2'] == self.product_id)
        ]

        #filtered_df based on the feature score
        filtered_df = filtered_df.query('text_long >= 0.2 and text_short >= 0.6 and image >= 0.8')
        
        #make sure make brands are present
        sorted_df = filtered_df[filtered_df['brand_1']!=filtered_df['brand_2']].sort_values(by=['text_short', 'text_long', 'image'], ascending=False)

        # Sort the dataframe based on the combined similarity score in descending order
        # sorted_df = filtered_df.sort_values(by='combined_score', ascending=False)

        # Exclude the original product and take the top N similar products
        top_similar_products = sorted_df[sorted_df['product_1'] != self.product_id].head(top_n)

        # Print the top similar products
        print(top_similar_products)

        return top_similar_products