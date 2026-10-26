#!/usr/bin/env bash
# Encode the corporate/brand masters for web: 1080 + 720 + poster frame.
# Masters range 10MB-941MB; target is a few MB each at 1.4-1.6 Mbps.
set -u
SRC="C:/Users/Jordan/Projects/higher-heights/higher-heights/vidsrc"
OUT="C:/Users/Jordan/Projects/higher-heights/site-brand/assets/vid"
IMG="C:/Users/Jordan/Projects/higher-heights/site-brand/assets/img"
mkdir -p "$OUT" "$IMG"

enc () {
  local in="$1" slug="$2" ss="${3:-3}"
  [ -f "$in" ] || { echo "MISSING $in"; return; }
  echo "── $slug"
  ffmpeg -hide_banner -loglevel error -y -i "$in" \
    -vf "scale=1920:-2:force_original_aspect_ratio=decrease,format=yuv420p" \
    -c:v libx264 -preset medium -crf 25 -profile:v high -movflags +faststart -an \
    "$OUT/$slug-1080.mp4" 2>&1 | tail -2
  ffmpeg -hide_banner -loglevel error -y -i "$in" \
    -vf "scale=1280:-2:force_original_aspect_ratio=decrease,format=yuv420p" \
    -c:v libx264 -preset medium -crf 28 -profile:v high -movflags +faststart -an \
    "$OUT/$slug-720.mp4" 2>&1 | tail -2
  ffmpeg -hide_banner -loglevel error -y -ss "$ss" -i "$in" -frames:v 1 -q:v 3 \
    -vf "scale=1600:-2" "$IMG/poster-$slug.jpg" 2>&1 | tail -2
  ls -la "$OUT/$slug-1080.mp4" "$OUT/$slug-720.mp4" "$IMG/poster-$slug.jpg" 2>/dev/null \
    | awk '{printf "   %-34s %6.2f MB\n", $NF, $5/1048576}'
}

enc "$SRC/Good Jobs__OakridgePropetyGroup.mp4"                  oakridge   6
enc "$SRC/Good Jobs__Revised v6_Revised Nexus Join Us video.M4V" nexus     4
enc "$SRC/Good Jobs__AdunaBreakfast._1.mp4"                      aduna     3
enc "$SRC/Good Jobs__COCKTAIL 3.MOV"                             cocktail  2
enc "$SRC/Good Jobs__VIDEO 5 - WALKING .MP4"                     walking   2
echo "ALL DONE"
