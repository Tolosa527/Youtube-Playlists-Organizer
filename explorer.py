import argparse
from dataclasses import dataclass
from typing import Dict, List

import requests


@dataclass
class Video:
    url: str
    title: str
    updated_at: str

    def __str__(self):
        return f"Title: {self.title}\nURL: {self.url}\nUpdated_at: {self.updated_at}\n"


def get_playlist_videos(google_script_url: str, playlist_id: str) -> List[Video]:
    response = requests.post(google_script_url, params={"playlist_id": playlist_id})
    return [Video(**video) for video in response.json()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Youtube Playlist tool")
    parser.add_argument("--playlist_id", metavar="playlist_id", help="playlist_id")
    parser.add_argument(
        "--filter_by_word", metavar="filter_by_word", help="search by word"
    )
    parser.add_argument("--order_by", metavar="order_by", help="order by title or date")
    parser.add_argument(
        "--ascending", action="store_true", help="ascending or descending"
    )
    parser.add_argument(
        "--descending", action="store_true", help="ascending or descending"
    )

    args = parser.parse_args()
    playlist_id = args.playlist_id
    filter_by_word = args.filter_by_word
    ascending = args.ascending
    descending = args.descending
    order_by = args.order_by

    if not playlist_id:
        print("Please enter playlist id")
        print("Usage: python explorer.py --playlist_id <playlist_id>")
        exit(1)
    else:
        playlist_videos = get_playlist_videos(
            google_script_url="https://script.google.com/macros/s/AKfycbyMt1N38_08QgBZ0tOMeCIWMtpWI1gq5MjpD3i5TCi9nY_Qs6nGVDrgioJ1JQ43Cgz0/exec",
            playlist_id=playlist_id,
        )
        if filter_by_word:
            playlist_videos_filtered = [
                video
                for video in playlist_videos
                if filter_by_word.lower() in video.title.lower()
            ]
            playlist_videos = playlist_videos_filtered
        if order_by:
            order_direction = True if ascending else False
            if order_by == "title":
                playlist_videos.sort(key=lambda x: x.title, reverse=order_direction)
            elif order_by == "date":
                playlist_videos.sort(key=lambda x: x.updated_at, reverse=order_direction)
    
    for video in playlist_videos:
        print(video)