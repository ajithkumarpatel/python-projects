// Fetch the list of reels (video files) from the backend and display them
fetch("/reels")
  .then(response => response.json())
  .then(videos => {
    const container = document.getElementById("reels-container");
    videos.forEach(video => {
      let videoEl = document.createElement("video");
      videoEl.src = "/static/videos/" + video;
      videoEl.controls = true;
      videoEl.style.width = "100%";
      videoEl.style.margin = "10px 0";
      container.appendChild(videoEl);
    });
  })
  .catch(error => console.error("Error fetching reels:", error));
