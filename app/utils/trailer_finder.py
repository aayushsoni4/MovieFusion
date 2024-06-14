from googleapiclient.discovery import build
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os
from logger import logger

load_dotenv()
YT_API = os.environ["YT_API"]
youtube = build("youtube", "v3", developerKey=YT_API)


def findYTtrailer(movie_title):
    """
    Find the YouTube trailer for a given movie title using YouTube API.

    Args:
        movie_title (str): The title of the movie.

    Returns:
        str: The URL of the YouTube trailer.
    """
    try:
        search_query = movie_title
        logger.debug(f"Searching YouTube trailer for: {search_query}")

        request = youtube.search().list(
            part="snippet",
            q=search_query,
            type="video",
            order="relevance",
            videoCategoryId="1",
        )

        response = request.execute()
        logger.debug(f"YouTube API response: {response}")

        item = response["items"][0]
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        logger.info(
            f"Found YouTube trailer URL: {video_url} for movie title: {movie_title}"
        )
        return video_url
    except Exception as e:
        logger.error(f"Error finding YouTube trailer for {movie_title}: {e}")
        return "https://www.youtube.com/watch?v=5PSNL1qE6VY"


def findYTtrailerbs4(query):
    """
    Find the YouTube trailer for a given query using BeautifulSoup to scrape YouTube search results.

    Args:
        query (str): The search query.

    Returns:
        str: The URL of the YouTube trailer.
    """
    try:
        logger.debug(
            f"Searching YouTube trailer using BeautifulSoup for query: {query}"
        )
        query = query.split(" ")
        query = "+".join(query)
        search_url = f"https://www.youtube.com/results?search_query={query}"

        logger.debug(f"Search URL: {search_url}")

        # Send an HTTP GET request to YouTube
        response = requests.get(search_url)
        logger.debug(f"HTTP GET response status: {response.status_code}")

        if response.status_code == 200:
            # Parse the HTML response
            soup = BeautifulSoup(response.text, "html.parser")

            # Convert the soup into a string
            soup = str(soup)

            # Find the index where 'href="/watch?v=' is present in the soup
            index = soup.find("watch?v=")
            video_url = (
                "https://www.youtube.com"
                + soup[index - 1 : soup.find("\\", index + 10)]
            )

            logger.info(
                f"Found YouTube trailer URL using BeautifulSoup: {video_url} for query: {query}"
            )
            return video_url
        else:
            logger.error(
                f"Failed to fetch YouTube search results. Status code: {response.status_code}"
            )
            return "https://www.youtube.com/watch?v=5PSNL1qE6VY"
    except Exception as e:
        logger.error(
            f"Error finding YouTube trailer using BeautifulSoup for query {query}: {e}"
        )
        return "https://www.youtube.com/watch?v=5PSNL1qE6VY"
