import subprocess
import time

class FFmpegWriter():
    def __init__(self, width, height, fps, out_dir):
        self.width = width
        self.height = height
        self.fps = fps
        self.proc = None
        self.out_dir = out_dir

    def write(self, frame):
        if self.proc is None:
            self.proc = self.init_process()

        if self.proc.poll() is not None:
            self.proc = self.init_process()

        try:
            self.proc.stdin.write(frame.tobytes())
        except BrokenPipeError:
            self.clean_process()

    def stop(self):
        self.clean_process()
        self.proc = None

    def init_process(self):
        return subprocess.Popen(
            self.__ffmpeg_cmd(),
            stdin=subprocess.PIPE,
            stdout=None,
            stderr=None,
            bufsize=0,
        )

    def clean_process(self):
        if self.proc.poll() is not None:
            return

        try:
            self.proc.stdin.close()
        except Exception:
            pass

        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()

        
    def __ffmpeg_cmd(self):
        return [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "warning",
            "-y",
            "-f", "rawvideo",
            "-pix_fmt", "bgr24",
            "-video_size", f"{self.width}x{self.height}",
            "-framerate", str(self.fps),
            "-i", "-",
            "-c:v", get_encoder(),
            "-b:v", "300k",
            "-f", "segment",
            "-segment_time", "300",
            "-reset_timestamps", "1",
            "-strftime", "1",
            "-g", "50",
            self.out_dir + "/recording_%y-%m-%d_%H-%M-%S.mp4",
        ]

def get_encoder(prefer_hevc=False):
    """
    Returns a working FFmpeg hardware encoder name.

    Returns:
        str encoder name

    Raises:
        RuntimeError if no hardware encoder works.
    """

    h264_candidates = [
        "h264_v4l2m2m",      # Raspberry Pi / Linux V4L2 hardware encoder
        "h264_nvenc",        # NVIDIA
        "h264_qsv",          # Intel Quick Sync
        "h264_vaapi",        # Intel/AMD VAAPI Linux
        "h264_videotoolbox", # macOS
    ]

    hevc_candidates = [
        "hevc_v4l2m2m",
        "hevc_nvenc",
        "hevc_qsv",
        "hevc_vaapi",
        "hevc_videotoolbox",
    ]

    candidates = hevc_candidates if prefer_hevc else h264_candidates

    available = _get_listed_ffmpeg_encoders()

    for encoder in candidates:
        if encoder not in available:
            continue

        if _test_encoder(encoder):
            return encoder

    raise RuntimeError("No working hardware FFmpeg encoder found")


def _get_listed_ffmpeg_encoders():
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-encoders"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    output = result.stdout + result.stderr

    encoders = set()
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            encoders.add(parts[1])

    return encoders


def _test_encoder(encoder):
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-f", "lavfi",
        "-i", "testsrc=size=640x480:rate=10",
        "-t", "1",
        "-c:v", encoder,
        "-f", "null",
        "-",
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    return result.returncode == 0
