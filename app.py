import streamlit as st

from utils.selenium_scraper import AmazonScraper


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


st.set_page_config(layout='wide')

product_url = st.text_input("Enter Product Name URL ")

if product_url:

    with st.container():
        product = get_product(product_url)
        print(product)
        col1, col2 = st.columns(2)

        with col1:
            st.image(product['image_url'])

        with col2:
            st.subheader(f"[{product['title']}]({product['url']})")
            "## Product Info:"
            st.markdown(product['short_description'])
        # st.write(filtered)