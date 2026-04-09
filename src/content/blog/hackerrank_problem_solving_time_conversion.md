---
title: Hackerrank Time Conversion Problem Solving
excerpt: A HackerRank solution in the Problem Solving category titled “Time Conversion”.
publishedAt: 2024-01-24
author: Anaf Naufalian
tags:
  - hackerrank
  - dsa
featured: false
draft: false
---

Hackerrank Problem Solving: Time Conversion
===========================================

Jan 24, 2024 by Anaf Naufalian

![Photo by Lukas Blazek on Unsplash](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*xzd_NmzBzA2TAF6B)

Solusi Hackerrank kategori **Problem Solving** yang berjudul “[Time Conversion](https://www.hackerrank.com/challenges/time-conversion/problem)”.

Pada problem kali ini, kita diharuskan untuk mengkonversi waktu dari format 12 jam (AM/PM) ke format 24 jam. Cukup mudah, langsung saja ke solusinya.

**Solusi**
----------

Pertama kita buat dulu fungsi yang bernama “prependZero”, fungsi ini berguna untuk menambahkan nol di depan jika nomor yang diberikan lebih kecil dari 10.

```
/**
 * Digunakan untuk menambahkan nol didepan jika nilai dari [num] lebih kecil dari 10
 */
fun prependZero(num: Int): String {
    return if (num < 10) "0$num" else num.toString()
}
```

Contoh:

*   num = 9, maka outputnya “09”
*   num = 0, maka outputnya “00”
*   num = 10, maka outputnya “10”
*   num = 13, maka outputnya “13”

Kedua, didalam fungsi “timeConversion” kita akan mengambil jam, menit, detik, dan tipe dari parameter “s” yang bertipe String.

```
var hour = "${s[0]}${s[1]}".toInt()
val minute = "${s[3]}${s[4]}".toInt()
val second = "${s[6]}${s[7]}".toInt()
val type = "${s[8]}${s[9]}" // "AM" atau "PM"
```

Ingat bahwa input yang diberikan memakai format “hh:mm:ssAM” atau “hh:mm:ssPM”. Untuk mendapatkan jamnya, kita mengambil karakter dari parameter “s” yang berada diindex ke-0 dan ke-1, untuk menit diindex ke-3 dan ke-4, dst.

Selanjutnya, kita akan mengubah nilai dari variabel “hour” yang tadinya dalam format 12 jam ke format 24 jam, caranya seperti kode dibawah.

```
hour = when (type) {
    // Jika tipe jamnya AM
    // Cek apakah jam lebih besar dari 11, jika ya kurangi 12, sebaliknya biarkan
    "AM" -> if (hour > 11) hour - 12 else hour
    // Jika tipe jamnya PM
    // Cek apakah jam lebih kecil dari 12, jika ya tambahkan 12, sebaliknya biarkan
    "PM" -> if (hour < 12) hour + 12 else hour
    else -> hour
}
```

Pertama kita akan cek tipenya apakah “AM” atau “PM”, jika tipenya “AM” kita akan cek lagi apakah nilai dari variabel “hour” lebih besar dari 11 atau tidak, jika lebih besar dari 11 maka nilainya akan kita kurangi 12, jika tidak biarkan saja. Mengapa perlu pengecekan lagi, karena jika input yang diberikan adalah misalnya “12:00:00AM” dan kita tidak menguranginya dengan 12, maka outputnya adalah “12:00:00”, padahal seharusnya outputnya “00:00:00”, karenya jam 12 AM itu adalah jam 12 malam, jam 12 malam dalam format 24 jam adalah jam 00. Begitu juga dengan tipe “PM”, kita juga harus membuat pengecekan lagi apakah nilai dari “hour” lebih kecil atau tidak.

Lalu diakhir fungsi kita tinggal memformatnya ke bentuk “hh:mm:ss”

```
// Format variabel hour, minute, dan second ke "hh:mm:ss"
return "${prependZero(hour)}:${prependZero(minute)}:${prependZero(second)}"
```

Full code

```
/**
 * Digunakan untuk menambahkan nol didepan jika nilai dari [num] lebih kecil dari 9
 */
fun prependZero(num: Int): String {
    return if (num < 10) "0$num" else num.toString()
}
fun timeConversion(s: String): String {
    var hour = "${s[0]}${s[1]}".toInt()
    val minute = "${s[3]}${s[4]}".toInt()
    val second = "${s[6]}${s[7]}".toInt()
    val type = "${s[8]}${s[9]}" // "AM" atau "PM"
    hour = when (type) {
        // Jika tipe jamnya AM
        // Cek apakah jam lebih besar dari 11, jika ya kurangi 12, sebaliknya biarkan
        "AM" -> if (hour > 11) hour - 12 else hour
        // Jika tipe jamnya PM
        // Cek apakah jam lebih kecil dari 12, jika ya tambahkan 12, sebaliknya biarkan
        "PM" -> if (hour < 12) hour + 12 else hour
        else -> hour
    }
    // Format variabel hour, minute, dan second ke "hh:mm:ss"
    return "${prependZero(hour)}:${prependZero(minute)}:${prependZero(second)}"
}
```