---
title: Create MediaStyle Notification in Android | by Anaf Naufalian
excerpt: MediaStyle notification is a powerful feature in Android that allows developers to create rich, interactive notifications for media playback applications.
publishedAt: 2023-03-18
author: Anaf Naufalian
tags:
  - android
featured: false
draft: false
---

Create MediaStyle Notification in Android | by Anaf Naufalian
=============================================================

[Anaf Naufalian](https://medium.com/@anafthdev_?source=post_page---byline--70fe7df3397e---------------------------------------)

Mar 18, 2023


![Photo by Jamie Street on Unsplash](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*B4rW5wkZAb8tcwqf)

MediaStyle notification is a powerful feature in Android that allows developers to create rich, interactive notifications for media playback applications. These notifications provide users with a seamless media playback experience, giving them control over their media playback directly from the notification panel.

In this article, we will explore the MediaStyle notification feature in Android and how it can be used to create an immersive media playback experience for users.

**What is MediaStyle notification?**

MediaStyle notification is a type of notification that is used for media playback applications. These notifications are designed to provide users with a rich and interactive experience that allows them to control media playback directly from the notification panel.

MediaStyle notifications provide several advantages over regular notifications. For example, users can control media playback without having to switch to the media player app, making it easy to pause, play, and skip tracks. Additionally, these notifications can display album art, media information, and other relevant information, providing users with a comprehensive overview of their media playback experience.

**How to create a MediaStyle notification in Android?**

Creating a MediaStyle notification in Android is a straightforward process that involves a few steps. Here’s how you can do it:

**Step 1:**

Create kotlin object named `NotificationUtil`:

from the code above, we have made:

*   **channelID:** a unique identifier for a notification channel, which is a way to group related notifications together. Each notification channel has a unique ID, which can be used to set the notification’s priority, sound, vibration pattern, and other settings.
*   **channelName:** a user-facing name for the notification channel, which is displayed to the user in the Android system settings. It should be a descriptive and meaningful name that helps the user understand what kind of notifications will be delivered through that channel.

and `createChannel` function to create a notification channel if the android version is above or equal to level 26.

**Step 2:**

Create class `SongAction` and `SongController`:

*   **Pause:** pause song
*   **Resume:** resume song
*   **Stop:** stop song
*   **Next:** next song
*   **Previous:** previous song

the functions inside `SongController`will call other functions of the `ExoPlayer`class, such as `stop()` , `pause()`, `play()`, etc.

**Step 3:**

Create kotlin data class model named `MusicState`:

*   **isPlaying:** whether song is playing or not
*   **currentDuration:** current played song position
*   **title:** song title
*   **album:** song album name
*   **artist:** artist name
*   **albumArt:** album art from bitmap
*   **duration:** song max duration

**Step 4:**

Create service named `MediaPlayerService`:

Inside `MediaPlayerService`we have a `mediaSession`variable that serves to provides a way to control media playback from a remote control or a notification. It allows an app to expose its media playback controls, such as play, pause, skip, and stop, to external devices or services that support media playback, such as Android Auto, Chromecast, and Bluetooth devices. `mediaStyle` media style notification. `notificationManager`the notification manager. `binder` used for bind service to activity. `songController`used for control the song. `binder` used to check whether the service is running in the foreground or not.

Then, add the `onCreate`function:

Inside the `onCreate` function, we initialize the previous variable, and add a callback for the mediaSession variable. This callback works for example controlling song from bluetooth device, etc. after adding the callback we call the `startForeground` function to start the service in the foreground.

before that, reopen the NotificationUtil object and add the function below:

after that, create a broadcast receiver named `MediaPlayerReceiver`:

This class serves to transmit actions from notification to `MediaPlayerService` and will be forwarded to `SongController`

After that reopen `MediaPlayerService` and add `onStartCommand` function

This function, serves to receive the action from the `MediaPlayerReceiver`, and update the notification with the new `MusicState`value.

Finally, add another function to `MediaPlayerService`

**Step 5:**

Open `MainActivity` class, and add the following code:

**Step 6:**

Create class named `MusicApplication` :

And don’t forget to edit `AndroidManifest.xml`

**Step 7:**

Run app, and the result will be like this

Thankyou for reading ❤

Full source code

[GitHub - kafri8889/MediaStyle-Notification
------------------------------------------

### MediaStyle Notification Android

github.com](https://github.com/kafri8889/MediaStyle-Notification?source=post_page-----70fe7df3397e---------------------------------------)