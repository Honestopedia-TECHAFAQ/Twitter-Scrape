import requests
from bs4 import BeautifulSoup
import streamlit as st

def get_twitter_spaces_info(username):
    url = f"https://twitter.com/{username}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            spaces_section = soup.find("div", {"data-testid": "ProfileSpacesProfile"})
            if spaces_section:
                spaces = spaces_section.find_all("div", {"data-testid": "ProfileSpacesProfile"})
                space_info = []
                for space in spaces:
                    space_name = space.find("div", {"data-testid": "SpaceTitle"}).get_text()
                    space_hosted_by = space.find("div", {"data-testid": "SpaceCreatorUsername"}).get_text()
                    space_info.append({"Space Name": space_name, "Hosted By": space_hosted_by})
                return space_info
            else:
                return "No spaces found on the profile."
        else:
            return f"Failed to retrieve data. HTTP Status Code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
st.title("Twitter Spaces Scraper")
twitter_username = st.text_input("Enter the Twitter username:")
if st.button("Get Spaces Info"):
    if twitter_username:
        st.write(f"Fetching spaces hosted by {twitter_username}...")
        spaces_info = get_twitter_spaces_info(twitter_username)
        if spaces_info != "No spaces found on the profile.":
            st.write(f"Spaces hosted by {twitter_username}:")
            for space in spaces_info:
                st.write(f"Space Name: {space['Space Name']}, Hosted By: {space['Hosted By']}")
        else:
            st.write(spaces_info)
    else:
        st.warning("Please enter a Twitter username.")
st.text("Note: Twitter's website structure may change over time, so the scraper may require updates.")
