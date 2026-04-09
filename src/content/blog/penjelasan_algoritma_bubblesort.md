---
title: Penjelasan algoritma Bubble Sort dan contoh implementasinya | by Anaf Naufalian
excerpt: Kali ini saya akan menjelaskan apa itu algoritma bubble sort dan bagaimana cara kerja algoritma tersebut dan bagaimana mengimplementasikannya, disini saya akan menggunakan bahasa kotlin untuk mengimplementasikan dan menjelaskannya.
publishedAt: 2023-09-05
author: Anaf Naufalian
tags:
  - dsa
  - sorting
featured: false
draft: false
---

Penjelasan algoritma _Bubble Sort dan contoh implementasinya_ | by Anaf Naufalian
=================================================================================

[Anaf Naufalian](https://medium.com/@anafthdev_?source=post_page---byline--3a51cdfd255f---------------------------------------)

Sep 5, 2023

![Photo by Alfred Kenneally on Unsplash](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*PlzLXS1Wj7rYb1rq)

Kali ini saya akan menjelaskan apa itu algoritma _bubble sort_ dan bagaimana cara kerja algoritma tersebut dan bagaimana mengimplementasikannya, disini saya akan menggunakan bahasa kotlin untuk mengimplementasikan dan menjelaskannya.

<b>[other]Bubble Sort Visualization[/other]</b>

Algoritma _bubble sort_ atau bisa juga disebut pengurutan tenggelam (_sinking sort_) adalah algoritma pengurutan yang paling mudah dibandingkan algoritma pengurutan lainnya seperti _selection sort, merge sort, radix sort, dll._ Algoritma _bubble sort_ ini mengurutkan nilai dengan cara membandingkan nilai **saat ini** dengan **nilai selanjutnya**, jika kedua nilai tersebut lebih besar atau lebih kecil (sesuai implementasinya, _ascending_ order atau _descending_ order) maka kedua nilai tersebut di _swap_ atau ditukar posisinya sampai semua nilainya sudah terurut. Agar lebih mudah untuk memahami, lihat contoh dibawah.

Misalnya kita mempunyai array dengan nilai [6, 2, 1, 5, 4, 3], dan kita ingin mengurutkannya dengan _ascending_ order atau dari nilai yang terkecil sampai yang terbesar.

![Unsorted array](https://miro.medium.com/v2/resize:fit:400/format:webp/1*hZvI7gYnuxCNrXVeajoceA.png)

**Langkah pertama, buat fungsi _“swap”:_**

fungsi ini akan kita gunakan untuk menukar nilai didalam array tanpa membuat _instance_ array baru.
Cara kerjanya yaitu:

1.  buat variable “temp”, variable ini akan kita gunakan untuk menyimpan elemen dari array di index ke-i
2.  tukar elemen diindex ke-i dengan elemen diindex ke-j
3.  tukar elemen diindex ke-j dengan nilai dari variable “temp” (elemen diindex ke-i sebelum diubah)

```
/**
 * Swap value dari index i ke j, dan index j ke i
 */
private fun swap(arr: Array<Int>, i: Int, j: Int) {
    val temp = arr[i] // simpan nilai arr[i] ke dalam variable temp
    arr[i] = arr[j] // ganti nilai di index ke-i dengan nilai di index ke-j
    arr[j] = temp // ganti nilai di index j dengan nilai dari variable temp (nilai di index ke-i sebelum diubah)
}
```

**Langkah kedua, buat fungsi _“shouldSwap”:_**

karena kita ingin algoritma _bubble sort_ yang kita buat bisa mengurutkan nilai dari yang terkecil ke yang terbesar (_ascending_) atau dari yang terbesar ke yang terkecil (_descending_), maka kita membuat fungsi _shouldSwap_ yang berfungsi untuk mengecek apakah kedua nilai yang diberikan (_n1_ dan _n2_) harus ditukar atau tidak. Fungsi ini mengembalikan nilai _true_ jika kedua nilai yang diberikan harus ditukar, _false_ jika kedua nilai tidak boleh ditukar

Fungsi ini mempunyai 3 parameter yaitu _n1, n2,_ dan _ascending_.

1.  _n1_: nilai yang akan dibandingkan dengan _n2_
2.  _n2_: nilai yang akan dibandingkan dengan _n1_
3.  _ascending_: order pengurutan, _true_ jika ingin mengurutkan dari yang terkecil ke yang terbesar (_ascending_), _false_ jika ingin mengurutkan dari yang terbesar ke yang terkecil (_descending_)

```
/**
 * Cek apakah kedua nilai [n1] dan [n2] harus ditukar
 *
 * @param n1 nilai ke-1
 * @param n2 nilai ke-2
 * @param ascending sort order
 *
 * @return true jika kedua nilai tersebut harus ditukar, false otherwise
 */
private fun shouldSwap(n1: Int, n2: Int, ascending: Boolean): Boolean {
    return if (ascending) n1 < n2 else n1 > n2
}
```

**Langkah ketiga, buat fungsi _“bubbleSort”:_**

Di fungsi inilah algoritma penyortiran akan dilakukan. Fungsi ini memiliki 2 parameter yaitu _arr_ dan _ascending_.

1.  _arr_: Array yang akan disortir, bertipe Integer
2.  _ascending_: order pengurutan

```
/**
 * @param arr array
 * @param ascending sort order, ascending (true) smallest to greatest, descending (false) otherwise
 */
fun bubbleSort(arr: Array<Int>, ascending: Boolean = true) {
    // Jika array kosong atau hanya berisi satu elemen saja, batalkan penyortiran
    if (arr.size <= 1) return
    // Iterasi sebanyak size array
    // Variable "x" tidak dipakai
    for (x in 0 until arr.size) {
        for (i in 0 until arr.size) {
            // Jika "i" adalah index terakhir, maka hentikan perulangan
            // Jika tidak dihentikan, maka akan terjadi error IndexOutOfBoundsException di bagian "arr[i + 1]"
            if (i == arr.size - 1) break
            
            // Cek apakah kedua nilai harus di tukar
            val shouldSwap = shouldSwap(arr[i + 1], arr[i], ascending)
            // Jika kedua nilai harus ditukar, maka tukar kedua nilai tersebut
            if (shouldSwap) swap(arr, i, i + 1)
        }
    }
}
```

Lihat kode diatas, dibaris pertama didalam blok kode fungsi _bubbleSort_ kita mengecek apakah array mempunyai elemen yang lebih kecil atau sama dengan satu, jika benar maka kita tidak akan melakukan penyortiran, jika salah maka penyortiran akan dilakukan.

Selanjutnya kita melakukan iterasi/perulangan sebanyak x kali atau sebanyak jumlah elemen didalam array.

Didalam blok kode perulangan for selanjutnya kita akan melakukan iterasi lagi, dengan variabel _i_ adalah index, dibaris selanjutnya kita akan memeriksa apakah index saat ini adalah index terakhir, jika iya, maka hentikan iterasi, jika tidak, lanjutkan iterasi. Mengapa kita harus memeriksa apakah index saat ini adalah index terakhir?.

> **Ingat!** indeks pertama itu dimulai dari NOL (0), tetapi ada juga dibeberapa bahasa pemrograman yang dimulai dari SATU (1).

Coba perhatikan kode dibagian _arr[i + 1]_, maksud dari kode ini adalah kita akan mengambil elemen yang berada diindex selanjutnya dari index _i_,
Contoh misalnya kita mempunyai array dengan isi sebagai berikut [6, 2, 1, 5, 4, 3], misal index _i_ saat ini berada diindex ke-2 (1), maka index selanjutnya atau _arr[i + 1]_ berada diindex ke-3 (5).

![index i dan index i + 1 (index selanjutnya)](https://miro.medium.com/v2/resize:fit:400/format:webp/1*rdSAEyXeVZR8v65rCrd5GQ.png)

Balik lagi ke pertanyaan diatas, mengapa kita harus memeriksa apakah index saat ini adalah index terakhir?, supaya saat index _i_ berada diindex terakhir, program akan menghentikan iterasinya, jika kita tidak memeriksa kondisi tersebut, maka saat index _i_ berada diindex terakhir program akan melempar error _IndexOutOfBoundsException_ yaitu error yang didapat ketika kita ingin mengambil elemen yang berada diluar jangkauan.

![IndexOutOfBoundsException](https://miro.medium.com/v2/resize:fit:576/format:webp/1*up4BhQwbKU-mTCakpSuT5g.png)

Oke, selanjutnya kita akan memeriksa apakah kedua nilai yang berada diindex _i_ dan _i + 1_ harus ditukar, disini kita akan menggunakan fungsi _shouldSwap_ yang sudah kita buat, untuk penjelasannya baca diatas.

Lalu dibaris selanjutnya, jika value dari variabel _shouldSwap_ bernilai _“true”_, maka tukar elemen yang berada diindex _i_ dan index _i + 1_, jika tidak maka jangan ditukar.

Jika kita menjalankan fungsi _bubbleSort_ diatas dengan array yang kita buat tadi, maka setiap iterasi, elemen-elemen yang berada didalam array akan berubah seperti dibawah.

![Initial array](https://miro.medium.com/v2/resize:fit:400/format:webp/1*hZvI7gYnuxCNrXVeajoceA.png)![Perulangan pertama](https://miro.medium.com/v2/resize:fit:400/format:webp/1*viJpuYmjESxq1mKihdMq-g.png)![Perulangan kedua](https://miro.medium.com/v2/resize:fit:400/format:webp/1*J9350i-EmJl5jQftpeZYuQ.png)![Perulangan ketiga, dan seterusnya](https://miro.medium.com/v2/resize:fit:400/format:webp/1*RNCHgCCPdmzae1MKyVPdUA.png)

Seperti itulah cara kerja algoritma _bubble sort_ dan contoh implementasinya, terima kasih sudah membaca, semoga bermanfaat.

**Full code**

```
/**
 * Swap value dari index i ke j, dan index j ke i
 */
private fun swap(arr: Array<Int>, i: Int, j: Int) {
    val temp = arr[i] // simpan nilai arr[i] ke dalam variable temp
    arr[i] = arr[j] // ganti nilai di index ke-i dengan nilai di index ke-j
    arr[j] = temp // ganti nilai di index j dengan nilai dari variable temp (nilai di index ke-i sebelum diubah)
}
/**
 * Cek apakah kedua nilai [n1] dan [n2] harus ditukar
 *
 * @param n1 nilai ke-1
 * @param n2 nilai ke-2
 * @param ascending sort order
 *
 * @return true jika kedua nilai tersebut harus ditukar, false otherwise
 */
private fun shouldSwap(n1: Int, n2: Int, ascending: Boolean): Boolean {
    return if (ascending) n1 < n2 else n1 > n2
}
/**
 * @param arr array
 * @param ascending sort order, ascending (true) smallest to greatest, descending (false) otherwise
 */
fun bubbleSort(arr: Array<Int>, ascending: Boolean = true) {
    // Jika array kosong atau hanya berisi satu elemen saja, batalkan penyortiran
    if (arr.size <= 1) return
    // Iterasi sebanyak size array
    // Variable "x" tidak dipakai
    for (x in 0 until arr.size) {
        for (i in 0 until arr.size) {
            // Jika "i" adalah index terakhir, maka hentikan perulangan
            // Jika tidak dihentikan, maka akan terjadi error IndexOutOfBoundsException di bagian "arr[i + 1]"
            if (i == arr.size - 1) break
            // Cek apakah kedua nilai harus di tukar
            val shouldSwap = shouldSwap(arr[i + 1], arr[i], ascending)
            // Jika kedua nilai harus ditukar, maka tukar kedua nilai tersebut
            if (shouldSwap) swap(arr, i, i + 1)
        }
    }
}
```

**Kode yang dipersingkat**

```
/**
 * Swap value dari index i ke j, dan index j ke i
 */
private fun swap(arr: Array<Int>, i: Int, j: Int) {
    arr[i] = arr[j].also { arr[j] = arr[i] }
}
/**
 * Cek apakah kedua nilai [n1] dan [n2] harus ditukar
 *
 * @param n1 nilai ke-1
 * @param n2 nilai ke-2
 * @param ascending sort order
 *
 * @return true jika kedua nilai tersebut harus ditukar, false otherwise
 */
private fun shouldSwap(n1: Int, n2: Int, ascending: Boolean): Boolean = if (ascending) n1 < n2 else n1 > n2
/**
 * @param arr array
 * @param ascending sort order, ascending (true) smallest to greatest, descending (false) otherwise
 */
fun bubbleSort(arr: Array<Int>, ascending: Boolean = true) {
    if (arr.size <= 1) return
    for (x in arr.indices) {
        for (i in arr.indices) {
            if (i == arr.size - 1) break
            if (shouldSwap(arr[i + 1], arr[i], ascending)) swap(arr, i, i + 1)
        }
    }
}
```