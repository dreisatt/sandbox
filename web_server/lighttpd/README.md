# Lighttpd serving WebRTC app

Based upon: https://codelabs.developers.google.com/codelabs/webrtc-web/#0

## Setup

* Install lighttpd and chromium web browser e.g. sudo apt install lighttpd chromium-browser
* Adjust document-root & username/usergroup in lighttpd.conf

## Running

* lighttpd -D -f lighttpd.conf
* chromium-browser http://localhost:45432
