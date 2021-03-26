"use strict";

const mediaStreamConstraints = {
  video: true,
};

const videoElement = document.querySelector("video");
var videoCaption = document.getElementById("videoCaption");

function toVideoElement(mediaStream)
{
  let videoStreamSettings = mediaStream.getVideoTracks()[0].getSettings();
  videoCaption.innerHTML = "Resolution: " + videoStreamSettings.width + "x" + videoStreamSettings.height;
  videoCaption.style.visibility = "visible";
  videoElement.srcObject = mediaStream;
}

function handleMediaStreamError(error)
{
  console.log("navigator.getUserMedia error: ", error);
}

navigator.mediaDevices.getUserMedia(mediaStreamConstraints).then(toVideoElement).catch(handleMediaStreamError);
