---
title: Memahami apa itu @Stable dan @Immutable di Jetpack Compose | by Anaf Naufalian
excerpt: Pernah ga kalian waktu buka layout inspector ngelihat kok ini rekomposisinya banyak banget? Padahal state yang berubah nggak semuanya, atau kalian punya composable function yang salah satu parameternya bertipe List, dan terkena recomposition padahal elemen didalam list tersebut nggak berubah? Nah, ini yang dinamakan “unnececary recomposition” atau “rekomposisi yang tidak perlu”.
publishedAt: 2023-12-30
author: Anaf Naufalian
tags:
  - android
  - jetpack compose
  - state management
featured: false
draft: false
---

Memahami apa itu @Stable dan @Immutable di Jetpack Compose | by Anaf Naufalian
==============================================================================

[Anaf Naufalian](https://medium.com/@anafthdev_?source=post_page---byline--9d2fac2a8747---------------------------------------)

Dec 30, 2023

![Photo by Luca Bravo on Unsplash](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*0j38V4VXxbdSCJ1W)

Halo teman-teman disini saya ingin membagikan informasi mengenai stabilitas di Jetpack Compose.

Pernah ga kalian waktu buka layout inspector ngelihat kok ini rekomposisinya banyak banget? Padahal state yang berubah nggak semuanya, atau kalian punya composable function yang salah satu parameternya bertipe _List,_ dan terkena recomposition padahal elemen didalam list tersebut nggak berubah? Nah, ini yang dinamakan _“unnececary recomposition”_ atau “rekomposisi yang tidak perlu”. Lalu bagaimana cara mencegahnya? Untuk mencegahnya kita bisa menggunakan anotasi `@Stable` dan `@Immutable`

> **Stable** — anotasi ini memberi tahu compiler bahwa objek yang dianotasikan mungkin akan berubah (mutable), tetapi compose runtime akan diberitahu, simplenya recomposition akan dipanggil.
>
> **Immutable** — anotasi ini memberi tahu compiler bahwa nilai properti dari objek yang dianotasikan tidak akan pernah berubah (immutable) setelah objek dibuat, tipe data primitif seperti String, Int, Float, dll. sudah immutable secara default.

Selain itu compose juga dapat menandai fungsi sebagai `skippable` dan `restartable`.

> **Skippable** — jika compiler menandai function dengan skippable, tandanya function tersebut dapat dilewati saat recomposition jika state atau argument saat ini masih sama dari yang sebelumnya.
>
> **Restartable** — jika compiler menandai function dengan restartable, artinya function tersebut dapat berfungsi sebagai “scope” dimana recomposition dapat dimulai. Perhatikan bahwa function yang memiliki kata kunci “inline” tidak dapat berfungsi sebagai “scope” untuk memulai recomposition, contoh: `Column`, `Row`, dll.

Langsung saja kita lihat contoh dibawah.

File **State.kt**:

```
data class StateWithoutStableOrImmutable(
    var word: String = "",
    val words: List<String> = emptyList(),
)
@Stable
data class StateWithStable(
    var word: String = "",
    val words: List<String> = emptyList(),
)
@Immutable
data class StateWithImmutable(
    val word: String = "",
    val words: List<String> = emptyList(),
)
```

File **StateViewModel.kt**:

```
@HiltViewModel
class StateViewModel @Inject constructor(): ViewModel() {
    private val _stateWithoutStableOrImmutable = MutableStateFlow(StateWithoutStableOrImmutable())
    val stateWithoutStableOrImmutable: StateFlow<StateWithoutStableOrImmutable> = _stateWithoutStableOrImmutable
    private val _stateWithImmutable = MutableStateFlow(StateWithImmutable())
    val stateWithImmutable: StateFlow<StateWithImmutable> = _stateWithImmutable
    private val _stateWithStable = MutableStateFlow(StateWithStable())
    val stateWithStable: StateFlow<StateWithStable> = _stateWithStable
    fun updateWord(s: String) = viewModelScope.launch {
        _stateWithoutStableOrImmutable.update { stateWithoutStableOrImmutable.value.copy(word = s) }
        _stateWithImmutable.update { stateWithImmutable.value.copy(word = s) }
        _stateWithStable.update { stateWithStable.value.copy(word = s) }
    }
    fun addWord(word: String) = viewModelScope.launch {
        _stateWithoutStableOrImmutable.update {
            stateWithoutStableOrImmutable.value.copy(
                words = stateWithoutStableOrImmutable.value.words.toMutableList().apply {
                    add(word)
                }
            )
        }
        _stateWithImmutable.update {
            stateWithImmutable.value.copy(
                words = stateWithImmutable.value.words.toMutableList().apply {
                    add(word)
                }
            )
        }
        _stateWithStable.update {
            stateWithStable.value.copy(
                words = stateWithStable.value.words.toMutableList().apply {
                    add(word)
                }
            )
        }
    }
}
```

File **StateScreen.kt**:

Di file ini kita akan membuat 3 composable function yaitu:
1. StateScreen: root untuk state screen, kita akan meng-observe state disini
2. StateScreenContent: konten yang akan ditampilkan di state screen
3. WordList: berisi lazy column dan text field untuk menambah kata

1.  **StateScreen**

```
@Composable
fun StateScreen(viewModel: StateViewModel = hiltViewModel()) {
    val state by viewModel.stateWithoutStableOrImmutable.collectAsStateWithLifecycle()
    StateScreenContent(
        state = state,
        onWordChanged = viewModel::updateWord,
        onAddClicked = {
            if (state.word.isNotBlank()) {
                viewModel.addWord(state.word)
                viewModel.updateWord("")
            }
        },
        modifier = Modifier
            .padding(24.dp)
            .fillMaxSize()
    )
}
```

2. **StateScreenContent**

```
@Composable
private fun StateScreenContent(
    state: StateWithoutStableOrImmutable,
    modifier: Modifier = Modifier,
    onWordChanged: (String) -> Unit,
    onAddClicked: () -> Unit
) {
    var progress by remember { mutableFloatStateOf(0f) }
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp),
        modifier = modifier
    ) {
        Slider(
            value = progress,
            onValueChange = {
                progress = it
            },
            modifier = Modifier
                .fillMaxWidth()
        )
        WordList(
            state = state,
            onWordChanged = onWordChanged,
            onAddClicked = onAddClicked,
            modifier = Modifier
                .fillMaxSize()
        )
    }
}
```

3. **WordList**

```
@Composable
private fun WordList(
    state: StateWithoutStableOrImmutable,
    modifier: Modifier = Modifier,
    onWordChanged: (String) -> Unit,
    onAddClicked: () -> Unit
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp),
        modifier = modifier
    ) {
        OutlinedTextField(
            value = state.word,
            onValueChange = onWordChanged,
            trailingIcon = {
                IconButton(onClick = onAddClicked) {
                    Icon(
                        imageVector = Icons.Rounded.Add,
                        contentDescription = null
                    )
                }
            },
            modifier = Modifier
                .fillMaxWidth()
        )
        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(8.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxSize()
        ) {
            items(
                items = state.words
            ) { word ->
                ListItem(
                    headlineContent = {
                        Text(word)
                    }
                )
            }
        }
    }
}
```

Jika dijalankan akan tampil seperti ini

![captionless image](https://miro.medium.com/v2/resize:fit:432/format:webp/1*0DNYp3tvbHCcjXf6rDUBqw.jpeg)

Jika sudah, coba kalian buka layout inspector dengan cara klik `Shift` 2x, lalu ketik “layout inspector”. Jika layout inspector sudah dibuka coba kalian geser slider yang ada di aplikasi.

<b>[other]State tanpa @Stable dan @Immutable[/other]</b>

Bisa kalian lihat bahwa composable function **WordList** juga ikut terkena recomposition, didalam composable function **WordList** yang terkena recomposition adalah **LazyColumn** tetapi **TextField** tidak terkena recomposition (di skip/di lewati). Hal ini bisa terjadi karena compose compiler menandai tipe data _List_ (variabel _words_) sebagai _unstable_ atau tidak stabil. Coba lihat compose metrics dibawah:

```
restartable skippable scheme("[androidx.compose.ui.UiComposable]") fun StateScreen(
  viewModel: StateViewModel? = @dynamic hiltViewModel(null, null, $composer, 0, 0b0011)
)
restartable skippable scheme("[androidx.compose.ui.UiComposable]") fun StateScreenContent(
  state: StateWithoutStableOrImmutable
  stable modifier: Modifier? = @static Companion
  stable onWordChanged: Function1<String, Unit>
  stable onAddClicked: Function0<Unit>
)
restartable skippable scheme("[androidx.compose.ui.UiComposable]") fun WordList(
  state: StateWithoutStableOrImmutable
  stable modifier: Modifier? = @static Companion
  stable onWordChanged: Function1<String, Unit>
  stable onAddClicked: Function0<Unit>
)
```

Bisa kalian lihat bahwa parameter _state_ tidak ditandai sebagai “stable” karena didalam class **StateWithoutStableOrImmutable** memiliki properti yang bertipe data _List,_ dan tidak ada jaminan bahwa list tersebut bersifat immutable, karena bisa saja kita menginisialisasikan list tersebut dengan array list atau mutable list.

Sekarang kita akan mencoba menggunakan **StateWithStable** atau **StateWithImmutable**. Ganti tipe data dari parameter state menjadi **StateWithStable** pada composable function **WordList** dan **StateScreenContent**:

```
@Composable
private fun StateScreenContent(
    state: StateWithStable,
    ...
``````
@Composable
private fun WordList(
state: StateWithStable,
...
```

dan kalian ganti juga di **StateScreen**

```
@Composable
fun StateScreen(viewModel: StateViewModel = hiltViewModel()) {
val state by viewModel.stateWithStable.collectAsStateWithLifecycle()
...
```

Sekarang kalian jalankan dan lihat di layout inspector.

Bisa kalian lihat saat kita menggeser slidernya hanya composable function **Slider** yang terrekomposisi, dan composable function **WordList** di skip/di lewati karena memang composable function tersebut tidak memerlukan rekomposisi karena datanya tidak berubah. Jika kalian lihat compose metricsnya, parameter state yang berada di composable function **StateScreenContent** dan **WordList** sudah ditandai dengan “stable”.

```
restartable skippable scheme("[androidx.compose.ui.UiComposable]") fun StateScreen(
viewModel: StateViewModel? = @dynamic hiltViewModel(null, null, $composer, 0, 0b0011)
)
restartable skippable scheme("[androidx.compose.ui.UiComposable]") fun StateScreenContent(
stable state: StateWithStable
stable modifier: Modifier? = @static Companion
stable onWordChanged: Function1<String, Unit>
stable onAddClicked: Function0<Unit>
)
restartable skippable scheme("[androidx.compose.ui.UiComposable]") fun WordList(
stable state: StateWithStable
stable modifier: Modifier? = @static Companion
stable onWordChanged: Function1<String, Unit>
stable onAddClicked: Function0<Unit>
)
```

Hal ini juga berlaku di state yang diberi anotasi `@Immutable` . Semoga bermanfaat.

Sumber:

*   [https://medium.com/androiddevelopers/jetpack-compose-stability-explained-79c10db270c8](https://medium.com/androiddevelopers/jetpack-compose-stability-explained-79c10db270c8)
*   [https://developer.android.com/jetpack/compose/performance/stability](https://developer.android.com/jetpack/compose/performance/stability)
*   [https://youtu.be/_FtKhWvHiTg?si=4Z6GJoqj8BWn73rO](https://youtu.be/_FtKhWvHiTg?si=4Z6GJoqj8BWn73rO)