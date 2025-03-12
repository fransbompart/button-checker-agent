import glob 

def get_videos(path: str) -> str:
    video_files = glob.glob(path)
    if video_files:
        return video_files
    return None