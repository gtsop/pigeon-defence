const API_URL = "http://" + window.location.hostname + ":8000";

function post(url, body) {
  return fetch(API_URL + url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
}

function a_delete(url) {
  return fetch(API_URL + url, {
    method: "DELETE",
  });
}

function get(url) {
  return fetch(API_URL + url, {
    method: "GET",
  });
}

function $(selector) {
  return document.querySelector(selector);
}

function main() {
  $("#angle").addEventListener("change", (event) => {
    setTimeout(() => {
      post("/motor/angle", {
        angle: parseInt(96 - event.target.value),
      });
    });
  });
  document.querySelector("#live").src = API_URL + "/video/stream";

  $("[name='video']").addEventListener("click", (event) => {
    const verb = Boolean(event.target.checked) ? "start" : "stop";
    post(`/video/${verb}`);
  });

  $("[name='inference']").addEventListener("click", (event) => {
    const verb = Boolean(event.target.checked) ? "start" : "stop";
    post(`/inference/${verb}`);
  });

  $("[name='composer']").addEventListener("click", (event) => {
    const verb = Boolean(event.target.checked) ? "start" : "stop";
    post(`/composer/${verb}`);
  });

  $("#record-start").addEventListener("click", () => {
    post("/recorder/start");
  });

  $("#record-stop").addEventListener("click", async () => {
    await post("/recorder/stop");
  });

  $("#video-live").addEventListener("click", () => {
    $("#live").src = API_URL + "/video/stream";
  });
  $("#video-live-stop").addEventListener("click", () => {
    $("#live").src = "";
  });

  initStatus();
}

async function initStatus() {
  const response = await get("/engines/status");

  const status = await response.json();

  $("[name='video']").checked = status.video;
  $("[name='inference']").checked = status.inference;
  $("[name='composer']").checked = status.composer;
}

function createNameCell(name) {
  const cell = document.createElement("td");
  cell.innerText = name;
  return cell;
}

function createPlayCell(name) {
  const cell = document.createElement("td");
  const play = document.createElement("button");
  play.innerText = "Play";
  play.onclick = function () {
    const newSrc = API_URL + "/recorder/videos/" + name;
    console.log("setting src", newSrc);
    $("#live").src = newSrc;
  };
  const remove = document.createElement("button");
  remove.innerText = "Delete";
  remove.onclick = async function () {
    await a_delete("/recorder/videos/" + name);
    listVideos();
  };
  cell.appendChild(play);
  cell.appendChild(remove);
  return cell;
}

main();
