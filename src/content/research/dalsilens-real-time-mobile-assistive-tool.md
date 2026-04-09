---
title: "Dalsilens: A Real-Time Mobile Assistive Tool for Dichromacy Using LMS Daltonization and HSV-Based Color Identification"
shortTitle: Dalsilens
abstract: A research using mobile computer vision to help people with color blindness see colors more clearly.
field: Visual Accessibility
status: Ongoing
platform: Android
tags:
  - dichromacy
  - accessibility
  - lms-daltonization
  - hsv-identification
featured: true
publishedAt: 2026-04-09
links:
  repository: https://github.com/dalsicore
---

## Abstract
Color Vision Deficiency (CVD), commonly known
as color blindness, is a genetic condition that affects a person’s
capacity ability to differentiate between certain light wavelengths.
Although eyesight itself is usually normal, individuals with CVD
find it difficult to distinguish colors within the red, green, and
blue spectrums. The most common type is Dichromacy, which
includes Protanopia (red-blind), Deuteranopia (green-blind), and
Tritanopia (blue-blind). Existing assistive technologies, such as
color-filtering glasses, are designed to separate overlapping red
and green wavelengths, help with color distinction but are often
expensive. Additionally, many existing smartphone applications
require users to upload images for processing, which prevents
real-time operation and limits immediate visual feedback. This
paper proposes the implementation of the LMS Daltonization
algorithm on the Android platform using real-time image processing. The method converts the camera’s input from the RGB color
space to the LMS color space. This allows for the mathematical
simulation and adjustment of the missing color spectrums. The
application is expected to help users distinguish objects with
specific color spectrum through a smartphone, with low latency
that supports real-time usage.

## Why this research

Color plays a big role in everyday tasks, but for users with dichromacy, it can be unreliable and tiring to interpret. Dalsilens starts from that problem and tries to make colors easier to understand in real-life situations.

## Approach

The current approach combines two parts that work together:

1. **LMS daltonization** to shift red, green, and blue so their differences are easier to see.
2. **HSV-based identification** to show a basic color name when pointing at a specific pixel.

## What we're testing

- Whether shifting red, green, and blue through LMS daltonization actually makes color differences easier to notice in real-time.
- How useful basic color labels are when users point at specific parts of a scene.
- Whether the system can stay responsive enough to be used continuously without feeling laggy.