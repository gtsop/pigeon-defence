document.addEventListener("DOMContentLoaded", function () {
  renderTimeline();
});

const finishTime = new Date();
let startTime = new Date();
startTime.setDate(finishTime.getDate() - 2);

async function listVideos() {
  const response = await get("/recorder/videos");
  const videos = await response.json();

  return videos.sort((a, b) => {
    if (a.created_at > b.created_at) return -1;
    if (a.created_at < b.created_at) return 1;
    return 0;
  });
}

function findVideoContainingTimestamp(videos, time) {
  return videos.find((video) => {
    console.log(
      Math.floor(video.created_at),
      Math.floor(time.getTime() / 1000),
    );
    return Math.floor(video.created_at) <= Math.floor(time.getTime() / 1000);
  });
}

async function renderTimeline() {
  const timeline = $("#timeline");
  const cursor = $("#timeline__cursor");
  const cursorLegend = $("#timeline__cursor__legend");

  const videos = await listVideos();

  timeline.addEventListener("mousemove", function (e) {
    const rect = timeline.getBoundingClientRect();
    const left = e.clientX - rect.left;

    cursor.style.left = left + "px";

    const timelineWidth = rect.width;
    const totalSecondsInTimeline = Math.floor(
      (finishTime.getTime() - startTime.getTime()) / 1000,
    );
    const secondsPerPixel = totalSecondsInTimeline / rect.width;

    const cursorTime = new Date(
      startTime.getTime() + left * secondsPerPixel * 1000,
    );

    const formatted = new Intl.DateTimeFormat("sv-SE", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    }).format(cursorTime);

    cursorLegend.textContent = formatted;
  });

  timeline.addEventListener("click", function (e) {
    const rect = timeline.getBoundingClientRect();
    const left = e.clientX - rect.left;

    cursor.style.left = left + "px";

    const timelineWidth = rect.width;
    const totalSecondsInTimeline = Math.floor(
      (finishTime.getTime() - startTime.getTime()) / 1000,
    );
    const secondsPerPixel = totalSecondsInTimeline / rect.width;

    const cursorTime = new Date(
      startTime.getTime() + left * secondsPerPixel * 1000,
    );

    const video = findVideoContainingTimestamp(videos, cursorTime);

    const newSrc = API_URL + "/recorder/videos/" + video.name;
    $("#live").src = newSrc;
  });
}
