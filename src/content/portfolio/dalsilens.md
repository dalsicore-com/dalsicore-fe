---
title: Dalsilens
tagline: A camera app that helps people with color blindness tell colors apart
summary: A mobile assistive tool that corrects confusing reds and greens on screen and names the color you point at, all running on the phone in real time.
status: research-phase
stack:
  - Android
  - Kotlin
  - Accessibility
  - Computer Vision
featured: true
order: 2
links:
  github: https://github.com/dalsicore
---

## Research direction

For people with dichromacy, red and green objects can look nearly identical, and that makes everyday tasks harder than they should be. Dalsilens runs two jobs on the same camera feed. It shifts reds and greens so the difference becomes visible, and it names the color under the reticle when a name is what you actually need. Both run on-device, so there is no upload and no lag.

## Focus areas

- Real-time camera processing optimized for mobile performance.
- Experimenting with daltonization under different lighting conditions.
- Integration of color identification through HSV-based classification for contextual feedback.