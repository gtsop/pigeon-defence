import os
import subprocess

def get_video_quota():
    return dehumanize(os.environ.get("PD_VIDEO_QUOTA") or "15 GB")

def get_video_disk_stats():

    quota = get_video_quota()

    size = get_dir_size(get_video_dir())

    return {
        "free": humanize(quota - size),
        "total": humanize(quota),
        "used": humanize(size),
        "used_percent": f"{size / quota * 100:.2f}",
    }

def get_video_dir():
    return os.environ.get("PD_VIDEO_DIR") or "/var/lib/pd-node/videos"

def init_video_dir():
    
    video_dir = get_video_dir()

    # Ensure the directory exists
    try:
        os.makedirs(video_dir, exists_ok=True)
    except PermissionError:
        log(video_dir, ": Directory does not exist")
        log(video_dir, ": Process does not have permission to create this directory")

        return False

    return True


def get_dir_size(directory):
    return int(subprocess.check_output("du -b " + directory + " | awk '{print $1}'", shell=True, text=True))


UNITS = {
    "B": 1,
    "KB": 1024,
    "MB": 1024**2,
    "GB": 1024**3,
    "TB": 1024**4,
    "PB": 1024**5,
}

def humanize(num):
    for unit in UNITS:
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024

def dehumanize(s):
    number, unit = s.split()
    return int(float(number) * UNITS[unit.upper()])
