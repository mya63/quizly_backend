from urllib.parse import parse_qs, urlparse


def get_youtube_video_id(url):
    """
    Extracts the YouTube video id from different YouTube URL formats.
    """

    parsed_url = urlparse(url)
    host = parsed_url.netloc.replace("www.", "").replace("m.", "")

    if host == "youtu.be":
        return parsed_url.path.strip("/")

    if host in ["youtube.com", "music.youtube.com"]:
        query = parse_qs(parsed_url.query)

        if parsed_url.path == "/watch":
            return query.get("v", [None])[0]

        if parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/shorts/")[1].split("/")[0]

        if parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/embed/")[1].split("/")[0]

    return None


def normalize_youtube_url(url):
    """
    Converts different YouTube URL formats into a clean watch URL.
    """

    video_id = get_youtube_video_id(url)

    if not video_id:
        return None

    return f"https://www.youtube.com/watch?v={video_id}"