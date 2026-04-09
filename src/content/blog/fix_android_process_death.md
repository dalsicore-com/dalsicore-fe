---
title: Mengatasi UI State yang hilang akibat Process Death di Android | by Anaf Naufalian
excerpt: Oke, apa itu process death?, Process Death atau yang biasa disebut System-initiated process death adalah kejadian yang terjadi karena sistem Android menghentikan suatu proses dari aplikasi yang sedang berjalan di background (latar belakang) untuk membebaskan sumber daya/RAM yang nantinya akan dipakai oleh aplikasi yang sedang berjalan di foreground (latar depan).
publishedAt: 2023-09-15
author: Anaf Naufalian
tags:
  - android
  - jetpack compose
featured: true
draft: false
---

Mengatasi UI State yang hilang akibat Process Death di Android | by Anaf Naufalian
==================================================================================

[Anaf Naufalian](https://medium.com/@anafthdev_?source=post_page---byline--d4b0b6c026da---------------------------------------)

Sep 15, 2023

![Photo by charlesdeluvio on Unsplash](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*vlXjxG5Z7VXIC1Jt)

Process Death, siapa si yang nggak kesel sama masalah ini?, misalnya kita lagi buka aplikasi chatting dan kita udah ketik pesan panjang lebar, pas kita pindah ke aplikasi lain, misalnya ke aplikasi edit video, dan kita mengedit video di aplikasi tersebut, setelah selesai mengedit video kita pindah ke aplikasi chatting tadi, eh tiba-tiba pesan yang kita ketik panjang lebar tadi hilang, nahhh bisa jadi itu karena process death.

Oke, apa itu process death?, _Process Death_ atau yang biasa disebut _System-initiated process death_ adalah kejadian yang terjadi karena sistem Android menghentikan suatu proses dari aplikasi yang sedang berjalan di _background_ (latar belakang) untuk membebaskan sumber daya/RAM yang nantinya akan dipakai oleh aplikasi yang sedang berjalan di _foreground_ (latar depan).

> _Perbedaan_ User-initiated process death _dan_ System-initiated process death _adalah_ User-initiated process death _prosesnya di kill oleh user, seperti saat mengklik home button._ System-initiated process death _prosesnya di kill oleh sistem, contohnya seperti perubahan konfigurasi_

Seperti contoh diatas, saat kita membuka aplikasi chatting dan kita mengetik pesan di EditText/TextField, biasanya pesan atau state dari EditText/TextField tersebut disimpan di dalam memori (RAM), ketika kita berpindah dari aplikasi chatting ke aplikasi edit video, maka aplikasi chatting beralih ke mode _background_ dan aplikasi edit video beralih ke mode _foreground_. Saat kita mengedit video pastinya kita membutuhkan lebih banyak sumber daya, ketika sumber daya tidak cukup disinilah sistem Android akan _mematikan/kill_ aplikasi-aplikasi yang berjalan di _background_, tetapi sebelum sistem Android mematikan aplikasi yang berjalan di _background_, sistem akan memanggil fungsi _onSavedInstanceState()_ untuk menyimpan state yang kita berikan, setelah fungsi tersebut dipanggil barulah sistem akan mematikan aplikasi tersebut. Nah, setelah edit video tadi kan kita buka lagi aplikasi chatting, tapi kenapa teks yang sudah kita ketik tadi bisa hilang?, itu mungkin karena developer dari aplikasi tersebut tidak mengimplementasikan _onSavedInstanceState()_ untuk menyimpan state.

Ada beberapa cara untuk menyimpan state di android, yaitu:

*   Jetpack Compose: bisa memakai [_rememberSaveable_](https://developer.android.com/reference/kotlin/androidx/compose/runtime/saveable/package-summary#rememberSaveable(kotlin.Array,androidx.compose.runtime.saveable.Saver,kotlin.String,kotlin.Function0))
*   View: bisa menggunakan fungsi [_onSavedInstanceState()_](https://developer.android.com/reference/android/app/Activity#onSaveInstanceState(android.os.Bundle)) di activity
*   ViewModel: bisa menggunakan [_SavedStateHandle_](https://developer.android.com/topic/libraries/architecture/viewmodel/viewmodel-savedstate)

Untuk kasus ini saya akan mengimplementasikannya di _ViewModel_ dan menggunakan library _hilt_ untuk _dependency injection_-nya, oke langsung saja pertama kita buat kelas _BaseViewModel_, untuk apa class _BaseViewModel_? kelas ini nantinya akan digunakan sebagai _parent class_ dari view model yang akan kita buat, kelas ini juga akan mewarisi (extends) kelas _ViewModel._

**_BaseViewModel.kt_**

```
/**
 *  kelas dasar (base class) untuk view model.
 *  Ini berarti kelas ini memberikan kerangka dasar untuk view model
 *  yang akan diturunkan (derived) oleh kelas-kelas lain.
 *
 *  @param savedStateHandle savedStateHandle yang digunakan untuk menyimpan state
 *  @param defaultState default state
 *
 *  @author kafri8889
 */
abstract class BaseViewModel<STATE: Parcelable>(
    private val savedStateHandle: SavedStateHandle,
    private val defaultState: STATE
): ViewModel() {
    // Key yang digunakan untuk menyimpan dan mengambil state di savedStateHandle
    private val KEY_STATE = "state"
    val state: StateFlow<STATE> = savedStateHandle.getStateFlow(KEY_STATE, defaultState)
    /**
     * Function yang digunakan untuk memperbarui state dari [savedStateHandle]
     *
     * @param newState parameter ini akan memberikan state saat ini sebagai `this`.
     */
    protected fun updateState(newState: STATE.() -> STATE) {
        // get current state
        savedStateHandle.get<STATE>(KEY_STATE)?.let { state ->
            // simpan state baru ke savedStateHandle
            savedStateHandle[KEY_STATE] = newState(state)
        }
    }
}
```

Dari kode diatas _BaseViewModel_ membutuhkan 2 parameter yaitu _savedStateHandle_ dan _defaultState._

Kata kunci “_STATE”_ dari kode diatas adalah sebuah [_generic type_](https://kotlinlang.org/docs/generics.html) yang menggambarkan tipe data dari _state_ yang akan digunakan didalam kelas _BaseViewModel,_ “_STATE”_ yang diberikan juga harus mewarisi kelas [_Parcelable_](https://developer.android.com/reference/android/os/Parcelable), kenapa harus menggunakan _Parcelable_?, karena _state_ yang kita berikan adalah kustom _data class,_ dan _savedStateHandle_ menggunakan [_Bundle_](https://developer.android.com/reference/android/os/Bundle) untuk menyimpan _state_ yang diberikan, jika kita tidak mengimplementasikan _Parcelable_ ke _state_ yang kita punya dan kita tetap memaksa untuk menyimpan state ke dalam _savedStateHandle_, maka akan terjadi error.

Selanjutnya kita membuat kelas _MyState_ yang digunakan sebagai tipe data _state_ dalam kelas _BaseViewModel._

**_MyState.kt_**

```
@Parcelize
data class MyState(
    val text: String = ""
): Parcelable
```

Setelah itu kita akan membuat kelas _MyViewModel (_kelas ini harus mewarisi kelas _BaseViewModel_).

**_MyViewModel.kt_**

```
@HiltViewModel
class MyViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle
): BaseViewModel<MyState>(
    savedStateHandle = savedStateHandle,
    defaultState = MyState()
) {
    /**
     * Funtion yang digunakan untuk memperbarui teks dari text field ke [savedStateHandle]
     */
    fun updateText(newText: String) {
        updateState {
            copy(
                text = newText
            )
        }
    }
}
```

Selanjutnya kita akan membuat UI yang akan ditampilkan ke pengguna

**_MyScreen.kt_**

```
@Composable
fun MyScreen(
    viewModel: MyViewModel = hiltViewModel()
) {
    // Observe state
    val state by viewModel.state.collectAsStateWithLifecycle()
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .fillMaxSize()
    ) {
        OutlinedTextField(
            value = state.text,
            onValueChange = viewModel::updateText
        )
    }
}
```

Lalu di _MainActivity._

**_MainActivity.kt_**

```
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ComposeResearchTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    MyScreen()
                }
            }
        }
    }
}
```

Jika semuanya sudah selesai, saat kita menjalankan aplikasi harusnya muncul tampilan seperti dibawah

![Preview aplikasi](https://miro.medium.com/v2/resize:fit:432/format:webp/1*OATiO6o-PFD4EX_Di2FcaA.png)

Untuk mensimulasikan _System-initiated process death_ ikuti cara dibawah:

*   **Pertama:** Run aplikasi di android studio.

![Run aplikasi di android studio](https://miro.medium.com/v2/resize:fit:800/format:webp/1*lmpUDHKN7ksQIpPmvcpcnQ.png)

*   **Kedua:** Minimize aplikasi dengan cara menekan tombol “_home”_.

<b>[other]Minimize aplikasi[/other]</b>

*   **Ketiga:** Buka “_Device Explorer_” di android studio dan pindah ke tab “_Processes_”, disini kita akan melihat package name aplikasi kita jika aplikasi berjalan.

![captionless image](https://miro.medium.com/v2/resize:fit:816/format:webp/1*0oLr2mwhDn1Q2DI7AcfRCQ.png)

*   **Keempat:** Pilih aplikasi kalian dan tekan tombol “_Kill process_”.

<b>[other]Kill app from device exploler[/other]</b>

*   **Kelima:** Buka kembali aplikasi, jika saat membuka aplikasi muncul splash screen atau blank itu tandanya aplikasi sudah di kill sebelumnya, dan jika sebelumnya kalian mengetik teks ke dalam text field sebelum aplikasi di minimize, maka setelah kalian kill aplikasi tadi dan kalian kembali ke aplikasi, seharusnya text yang kalian ketik tadi masih ada.

<b>[other]Preview[/other]</b>

Jika saat kalian mencoba dan hasilnya seperti video diatas maka implementasinya sudah benar, untuk source kodenya bisa klik link dibawah.

[Github-kafri8889/Compose-Research:Processdeath
----------------------------------------------

### Contribute to kafri8889/Compose-Research development by creating an account on GitHub.

github.com](https://github.com/kafri8889/Compose-Research/tree/master/app/src/main/java/com/anafthdev/composeresearch/research/base?source=post_page-----d4b0b6c026da---------------------------------------)

Contoh penggunaanya bisa kalian lihat di projek ini

[GitHub - kafri8889/DailyCost: Aplikasi pengelola keuangan
---------------------------------------------------------

### Aplikasi pengelola keuangan. Contribute to kafri8889/DailyCost development by creating an account on GitHub.

github.com](https://github.com/kafri8889/DailyCost?source=post_page-----d4b0b6c026da---------------------------------------)

terima kasih sudah membaca artikel ini.

**Referensi**

*   [https://developer.android.com/topic/libraries/architecture/saving-states](https://developer.android.com/topic/libraries/architecture/saving-states)
*   [https://developer.android.com/topic/libraries/architecture/viewmodel/viewmodel-savedstate](https://developer.android.com/topic/libraries/architecture/viewmodel/viewmodel-savedstate)