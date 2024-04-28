import streamlit as st
from utils.selenium_scraper import AmazonScraper
from utils.data_analysis import DataAnalysis

def get_product(product_url):
    scraper = AmazonScraper(product_url)
    product = {}
    product_name, product_id = scraper.getProductNameAndIDFromURL()

    product['id'] = product_id
    product['name'] = product_name

    main_image = scraper.getLeftImage()[0]
    center_div = scraper.parseCenterDiv()

    bottom, _ = scraper.parseBottomDivs()

    product['title'] = scraper.getProductTitle()
    product['brand'] = center_div['product_brand']

    product['short_description'] = center_div['product_about']
    product['long_description'] = " ".join([bottom['brand_story'], bottom['product_long_description'], bottom['product_information'], bottom['product_short_description'], bottom['misc']])

    product['image_url'] = main_image

    product['url'] = product_url

    return product

def display_product_details(product):
    st.image(product['image_url'])
    st.subheader(f"[{product['title']}]({product['url']})")
    st.markdown("## Product Info:")
    st.markdown(product['short_description'])

def display_top_similar_products(top_similar_products):
    st.markdown("## Top Similar Products:")
    
    for index, row in top_similar_products.iterrows():
        with st.expander(f"Product: {row['product_1']}"):
            st.subheader(f"[{row['product_1']}]({row['product_1_url']})")
            st.write(f"Text Short: {row['text_short']}")
            st.write(f"Text Long: {row['text_long']}")
            st.write(f"Image: {row['image']}")



st.set_page_config(layout='wide')
st.markdown("<h1 style='text-align: center; color: black;'>Welcome to White Label Detector</h1>", unsafe_allow_html=True)
st.markdown("Select the product you are planning to buy on Amazon below and we will display the top products which might be white labels of the chosen one!")
product_url = st.text_input("Enter the Amazon product URL of the smart camera you would like to search for:", placeholder="Enter Product URL and hit enter", help="Enter Product URL and hit enter")

if product_url:
    product = get_product(product_url)

    with st.container():
        display_product_details(product)
    
    col1, col2 = st.columns([1, 10])
    with col2:
        if st.button("Search for white labels", use_container_width=True, type="primary"):
            data_path = "/Users/priyankabose/Streamlit Dashboard/whitelabel-dashboard/amazon_smart_cameras_products_text_image_matrix_tfidf.csv"
            given_product_id = product['id']
            data_analysis = DataAnalysis(data_path, given_product_id)
            top_similar_products = data_analysis.find_top_similar_products()
            display_top_similar_products(top_similar_products)
