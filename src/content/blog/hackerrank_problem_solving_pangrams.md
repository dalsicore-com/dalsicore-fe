---
title: Hackerrank Pangrams Problem Solving
excerpt: Solusi Hackerrank kategori Problem Solving yang berjudul “Pangrams”.
publishedAt: 2024-01-24
author: Anaf Naufalian
tags:
  - hackerrank
  - dsa
featured: false
draft: false
---

Hackerrank Problem Solving: Pangrams
====================================

[Anaf Naufalian](https://medium.com/@anafthdev_?source=post_page---byline--77a4232bc0ad---------------------------------------)

Jan 24, 2024

![Photo by Sven Brandsma on Unsplash](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*rOGP-gN03lrd25Kd)

Solusi Hackerrank kategori **Problem Solving** yang berjudul “[Pangrams](https://www.hackerrank.com/challenges/pangrams/problem)”.

> A pangram is a string that contains every letter of the alphabet. Given a sentence determine whether it is a pangram in the English alphabet. Ignore case. Return either `pangram` or `not pangram` as appropriate.

Singkatnya, pangram adalah suatu kalimat yang dimana di kalimat tersebut terdapat alfabet dari “a” sampai “z”. Contoh pangram yang paling populer adalah kalimat “The quick brown fox jumps over a lazy dog”. Oke langsung saja.

Pada problem tersebut kita diberi sebuah fungsi dengan nama “pangrams”, fungsi tersebut memiliki 1 parameter “s” yang bertipe String dan harus mengembalikan String juga. Output dari fungsi tersebut harus berupa kalimat “pangram” jika nilai dari parameter “s” adalah pangram, dan “not pangram” jika bukan.

**Solusi**
----------

Kita tahu bahwa total huruf alfabet ada 26, oleh karena itu kita harus menghitung ada berapa karakter alfabet di string tersebut. Kita dapat memanfaatkan _Set._ Bagi kalian yang belum tahu apa itu set, Set adalah bagian dari struktur data yang menyimpan elemen unik, maksudnya setiap elemen yang ada di dalam set itu tidak bisa duplikat. Set ini mirip array, hanya saja elemen di dalam set tidak bisa di duplikat.

Code

```
fun pangrams(s: String): String {
    // Buat variabel set untuk menyimpan alfabet
    val set = mutableSetOf<Char>() // Gunakan mutable set supaya kita bisa menambahkan elemen ke dalam set ini
    
    // Loop variabel "s"
    for (c in s) {
        // Cek apakah karakter dari variabel "c" adalah spasi
        // Jika iya jangan tambahkan ke dalam set, jika bukan tambahkan ke dalam set
        if (!c.isWhitespace()) {
            set.add(c.lowercaseChar())
        }
    }
    // Untuk outputnya 
    // kita akan cek apakah size dari variabel set adalah 26 (jumlah alfabet) atau bukan
    // Jika totalnya ada 26 berarti "pangram" jika bukan "not pangram"
    return if (set.size == 26) "pangram" else "not pangram"
}
```

Kode yang lebih singkat

```
fun pangrams(s: String): String {
    return mutableSetOf<Char>().apply {
        for (c in s) if (!c.isWhitespace()) add(c.lowercaseChar())
    }.let { if (it.size >= 26) "pangram" else "not pangram" }
}
```