import streamlit as st
from utils.selenium_scraper import AmazonScraper
from utils.data_analysis import DataAnalysis
import utils.app_name_extract_spacy as app_name_extract_spacy
import utils.app_name_extract_bert as app_name_extract_bert
from annotated_text import annotated_text
import logging
import nltk

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')

# Configure logging
logging.basicConfig(level=logging.WARNING)
st_logger = logging.getLogger('streamlit')
st_logger.setLevel(logging.WARNING)


def get_product(product_url):
    """
    Scrapes product details from Amazon.

    Args:
        product_url (str): The URL of the Amazon product.

    Returns:
        dict: A dictionary containing product details.
    """
    scraper = AmazonScraper(product_url)
    product = {}
    product_name, product_id = scraper.getProductNameAndIDFromURL()

    product['id'] = product_id
    product['name'] = product_name

    # Scrape main image and product information
    main_image = scraper.getLeftImage()[0]
    center_div = scraper.parseCenterDiv()
    bottom, _ = scraper.parseBottomDivs()

    # Populate product dictionary
    product['title'] = scraper.getProductTitle()
    product['brand'] = center_div['product_brand']
    product['short_description'] = center_div['product_about']
    product['long_description'] = " ".join([bottom['brand_story'], bottom['product_long_description'],
                                            bottom['product_information'], bottom['product_short_description'],
                                            bottom['misc']])
    product['image_url'] = main_image
    product['url'] = product_url

    return product


def display_product_details(product):
    """
    Displays product details in Streamlit.

    Args:
        product (dict): A dictionary containing product details.
    """
    col1, col2 = st.columns(2)
    with col1:
        st.image(product['image_url'])
        st.subheader(f"[{product['title']}]({product['url']})")

    with col2:
        st.markdown("## Product Info:")
        st.markdown(product['short_description'])


def display_top_similar_products(top_similar_products):
    """
    Displays the top similar products in Streamlit.

    Args:
        top_similar_products (DataFrame): A DataFrame of top similar products.
    """
    st.markdown("## Top Similar Products:")

    for index, row in top_similar_products.iterrows():
        with st.expander(f"Product: {row['product_1']}"):
            st.subheader(f"[{row['product_1']}]({row['product_1_url']})")
            st.write(f"Text Short: {row['text_short']}")
            st.write(f"Text Long: {row['text_long']}")
            st.write(f"Image: {row['image']}")


# Configure the Streamlit page layout
st.set_page_config(layout='wide')
st.markdown("<h1 style='text-align: center; color: black;'>Welcome to White Label Detector</h1>", unsafe_allow_html=True)
st.markdown("Select the product you are planning to buy on Amazon below and we will display the top products which might be white labels of the chosen one!")

# Input for the product URL
product_url = st.text_input("Enter the Amazon product URL of the smart camera you would like to search for:", 
                            placeholder="Enter Product URL and hit enter", 
                            help="Enter Product URL and hit enter")

if product_url:
    product = get_product(product_url)

    with st.container():
        display_product_details(product)
    
        col1, col2 = st.columns(2)
        with col1:
            # Button to search for white labels
            if st.button("Search for white labels", use_container_width=True, type="primary"):
                data_path = "./amazon_smart_cameras_products_text_image_matrix_tfidf.csv"
                given_product_id = product['id']
                data_analysis = DataAnalysis(data_path, given_product_id)
                top_similar_products = data_analysis.find_top_similar_products()
                
                ## Store the results in session state
                # this is required because once we click the Get app names button, the content under col2 gets removed
                st.session_state['top_similar_products'] = top_similar_products  


            if 'top_similar_products' in st.session_state:
                display_top_similar_products(st.session_state['top_similar_products'])
        with col2:
            # Button to get app names
            if st.button("Get app names", use_container_width=True, type="secondary"):
                app_result = app_name_extract_bert.get_app_name(product)

                st.session_state['app_result'] = app_result  # Store the results in session state
                        

            if 'app_result' in st.session_state:
                result = st.session_state['app_result']
                if 'err' in result:
                    st.warning(f"Could not complete inference! {result['err']}", icon="⚠️")
                else:
                    if result['app']:
                        annotated_text(
                            (result['app'], "APP_NAME")
                        )
                    else:
                        st.warning(f"No APP Name Found!", icon="⚠️")
