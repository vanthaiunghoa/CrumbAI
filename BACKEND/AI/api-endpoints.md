# Crumb AI API Endpoints

This document outlines the endpoints available in the Crumb AI API, along with their functionality, expected input, and output.

## Index

- [Create Video Processing Job](#create-video-processing-job)
- [Check Status of Video Processing Job](#check-status-of-video-processing-job)
- [Alternative Status Check](#alternative-status-check)
- [Retrieve Video Clips](#retrieve-video-clips)
- [Delete Video Clip](#delete-video-clip)
- [Retrieve Single Video Clip](#retrieve-single-video-clip)
- [Get Video File](#get-video-file)

---

## Create Video Processing Job

- **Endpoint:** `/create`
- **Method:** `POST`
- **Authorization:** Bearer token required
- **Input:**
  - JSON containing:
    - `youtube_url`: URL of the YouTube video to be processed
    - `user_id`: ID of the user initiating the processing job
- **Output:**
  - JSON containing:
    - `job_id`: ID of the created processing job

---

## Check Status of Video Processing Job

- **Endpoint:** `/status`
- **Method:** `POST`
- **Authorization:** Bearer token required
- **Input:**
  - JSON containing:
    - `job_id`: ID of the processing job
- **Output:**
  - JSON containing:
    - `status`: Current status of the processing job

---

## Alternative Status Check

- **Endpoint:** `/status-2`
- **Method:** `POST`
- **Authorization:** Bearer token required
- **Input:**
  - JSON containing:
    - `job_id`: ID of the processing job
- **Output:**
  - JSON containing:
    - `status`: Timeout setting of the processing job

---

## Retrieve Video Clips

- **Endpoint:** `/get-clips`
- **Method:** `POST`
- **Authorization:** Bearer token required
- **Input:**
  - JSON containing:
    - `user_id`: ID of the user to retrieve video clips for
- **Output:**
  - JSON containing:
    - `videos`: List of video clips associated with the specified user

---

## Delete Video Clip

- **Endpoint:** `/delete`
- **Method:** `POST`
- **Authorization:** Bearer token required
- **Input:**
  - JSON containing:
    - `user_id`: ID of the user who owns the video clip
    - `video_id`: ID of the video clip to be deleted
- **Output:**
  - JSON indicating successful deletion of the video clip

---

## Retrieve Single Video Clip

- **Endpoint:** `/get-clip`
- **Method:** `POST`
- **Authorization:** Bearer token required
- **Input:**
  - JSON containing:
    - `user_id`: ID of the user who owns the video clip
    - `video_id`: ID of the video clip to retrieve
- **Output:**
  - JSON containing:
    - `video`: Details of the requested video clip

---

## Get Video File

- **Endpoint:** `/videos/<path>/<video_id>`
- **Method:** `GET`
- **Authorization:** Not required
- **Input:** None
- **Output:**
  - Video file if found, otherwise JSON indicating that the video was not found

