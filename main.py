import streamlit as st
import pandas as pd
from scrape import (
    scrape_website_with_sbr,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)

from parse import parse_with_ollama

st.title("AI Driven Web Scraping with LLM")
url = st.text_input("Paste the Website URL:")


if st.button("Scrape it", key="scrape_button"):
    st.spinner("Scraping the website...")
    try:
        result = scrape_website_with_sbr(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)

        st.session_state.dom_content = cleaned_content

        with st.expander("View DOM content"):
            st.text_area("Cleaned content", cleaned_content, height=300)
            st.success("Website scraped successfully!")
    except Exception as e:
        st.error(f"An error occurred during scraping: {e}")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want from the website?")

    if st.button("Parse Content", key="parse_button"):
        if not parse_description:
            st.error("Please enter a description of what to extract.")
        else:
            st.spinner("Parsing the content...")
            try:

                dom_chunks = split_dom_content(st.session_state.dom_content)
                

                result = parse_with_ollama(dom_chunks, parse_description)
                
                parsed_df = pd.DataFrame(result, columns=["Content"])

                st.write("Parsed Content:")
                st.table(parsed_df)
                
                st.session_state.parsed_content = parsed_df

            except Exception as e:
                st.error(f"An error occurred during parsing: {e}")