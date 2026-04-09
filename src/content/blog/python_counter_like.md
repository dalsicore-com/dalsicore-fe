---
title: Creating a Python Counter-Like in Java and Kotlin | by Anaf Naufalian
excerpt: Hello in this article i will show you how to create counter like python counter in java and kotlin. Before that, what is counter? In python, a counter is alibrary used for counting the frequency of element in a list or collection.
publishedAt: 2023-09-29
author: Anaf Naufalian
tags:
  - dsa
featured: true
draft: false
---

Creating a Python Counter-Like in Java and Kotlin | by Anaf Naufalian
=====================================================================

[Anaf Naufalian](https://medium.com/@anafthdev_?source=post_page---byline--3facf2cad2fd---------------------------------------)

Sep 29, 2023

![Photo by David Clode on Unsplash](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*065qdsGZctvOqrMz)

Hello in this article i will show you how to create counter like python counter in java and kotlin.

Before that, what is counter? In python, a counter is alibrary used for counting the frequency of element in a list or collection. For example, we have an array with the following elements: _[‘h’, ‘e’, ‘l’, ‘l’, ‘o’],_ Each element in this array has a different frequency such as:
- h = 1
- e = 1
- l = 2
- o = 1
  To get this value in python, we can use the Counter class from _collections_ library, see the code below.

```
# First, import collections library
from collections import Counter
list = ['h', 'e', 'l', 'l', 'o']
print(Counter(list)) # Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})
```

The return value of the Counter class is a dictionary (similar to Map in java or kotlin). To create this in kotlin or java, we can use _HashMap_ class, see the code below.

```
class Counter<T>() {
    constructor(iterable: Iterable<T>): this() {
        _map = hashMapOf<T, Int>().apply {
            for (k in iterable) set(k, if (k in keys) get(k)!! + 1 else 1)
        }
    }
    constructor(map: Map<T, Int>): this() {
        _map = HashMap(map)
    }
    /**
     * Mutable map to store value
     */
    private var _map: HashMap<T, Int> = hashMapOf()
    /**
     * Immutable map
     */
    val map: Map<T, Int>
        get() = _map.toMap()
}
```

First, create _Counter_ class and its constructor. To initialize _Counter_ class we can pass parameter with type _Iterable_ interface, _Map_ interface, or empty parameter. We also add two variables, “__map_ ”and “_map”_ variable to store values. In addition, in python, counter have a function like _total, most_common, subtract,_ and _update._

```
    /**
     * Sum of the counts
     */
    fun total(): Int = _map.values.sum()
    /**
     * List the n most common elements and their counts from the most
     * common to the least.
     *
     * >>> Counter('abracadabra').mostCommon(3)
     * [('a', 5), ('b', 2), ('r', 2)]
     */
    fun mostCommon(n: Int): Map<T, Int> {
        val sorted = _map.entries.sortedByDescending { it.value }
        return buildMap {
            var count = 0
            for ((k, v) in sorted) if (count < n) put(k, v).also { count++ } else break
        }
    }
    /**
     * add counts instead of replacing them.
     *
     * >>> val c = Counter("which".asIterable())
     * >>> c.update("witch".asIterable())           # add elements from another iterable
     * >>> val d = Counter("watch".asIterable())
     * >>> c.update(d)                              # add elements from another counter
     * >>> c.map['h']                               # four 'h' in which, witch, and watch
     * 4
     */
    fun update(other: Counter<T>): Counter<T> {
        plusAssign(other)
        return this
    }
    /**
     * add counts instead of replacing them.
     *
     * >>> val c = Counter("which".asIterable())
     * >>> c.update("witch".asIterable())           # add elements from another iterable
     * >>> val d = Counter("watch".asIterable())
     * >>> c.update(d)                              # add elements from another counter
     * >>> c.map['h']                               # four 'h' in which, witch, and watch
     * 4
     */
    fun update(other: Iterable<T>): Counter<T> {
        plusAssign(other)
        return this
    }
    /**
     * add counts instead of replacing them.
     *
     * >>> val c = Counter("which".asIterable())
     * >>> c.update("witch".asIterable())           # add elements from another iterable
     * >>> val d = Counter("watch".asIterable())
     * >>> c.update(d)                              # add elements from another counter
     * >>> c.map['h']                               # four 'h' in which, witch, and watch
     * 4
     */
    fun update(other: Map<T, Int>): Counter<T> {
        plusAssign(other)
        return this
    }
```

Because in python the _update_ function adds the existing frequency with the new frequency of the given object, then, we can use this function like the _plusAssign_ function

```
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plusAssign(other: Counter<T>) {
        _map = plus(other)._map
    }
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plusAssign(other: Iterable<T>) {
        _map = plus(other)._map
    }
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plusAssign(other: Map<T, Int>) {
        _map = plus(other)._map
    }
``````
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plus(other: Counter<T>): Counter<T> {
        return copy().apply {
            for ((k, v) in other.map) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! + v else v
            }
        }
    }
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plus(other: Iterable<T>): Counter<T> {
        return copy().apply {
            for (k in other) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! + 1 else 1
            }
        }
    }
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plus(other: Map<T, Int>): Counter<T> {
        return copy().apply {
            for ((k, v) in other) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! + v else v
            }
        }
    }
``````
    /**
     * Copy [Counter] instance
     */
    fun copy(): Counter<T> = Counter(hashMapOf<T, Int>().apply { putAll(map) })
```

For the subtract function we make it the same as the plus function, only the operation is different.

```
    /**
     * Subtract count.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minusAssign(other: Counter<T>) {
        _map = minus(other)._map
    }
    /**
     * Subtract count.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minusAssign(other: Iterable<T>) {
        _map = minus(other)._map
    }
    /**
     * Subtract count.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minusAssign(other: Map<T, Int>) {
        _map = minus(other)._map
    }
    /**
     * Subtract count and return new [Counter] object.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minus(other: Counter<T>): Counter<T> {
        return copy().apply {
            for ((k, v) in other.map) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! - v else -v
            }
        }
    }
    /**
     * Subtract count and return new [Counter] object.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minus(other: Iterable<T>): Counter<T> {
        return copy().apply {
            for (k in other) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! - 1 else -1
            }
        }
    }
    /**
     * Subtract count and return new [Counter] object.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minus(other: Map<T, Int>): Counter<T> {
        return copy().apply {
            for ((k, v) in other) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! - v else -v
            }
        }
    }
```

After we have implemented all these functions, we will make unit test for this class. Create _CounterTest_ class in _test_ module, and paste the code below.

```
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
class CounterTest {
    @Test
    fun testTotal() {
        val total = Counter("abracadabra".asIterable()).total()
        assertEquals(11, total)
    }
    @Test
    fun testMostCommon() {
        val mostCommon = Counter("abracadabra".asIterable()).mostCommon(3)
        assertTrue(mostCommon.containsKey('a'))
        assertTrue(mostCommon.containsKey('b'))
        assertTrue(mostCommon.containsKey('r'))
        assertEquals(5, mostCommon['a'])
        assertEquals(2, mostCommon['b'])
        assertEquals(2, mostCommon['r'])
    }
    @Test
    fun testUpdateWithCounter() {
        val counter = Counter("which".asIterable())
        counter.update(Counter("witch".asIterable())).update(Counter("watch".asIterable()))
        assertEquals(4, counter.map['h'])
    }
    @Test
    fun testUpdateWithIterable() {
        val counter = Counter("which".asIterable())
        counter.update("watch".asIterable()).update("watch".asIterable())
        assertEquals(4, counter.map['h'])
    }
    @Test
    fun testMinusAssignWithCounter() {
        val counter = Counter("which".asIterable())
        counter -= Counter("witch".asIterable())
        counter -= Counter("watch".asIterable())
        assertEquals(0, counter.map['h'])
        assertEquals(-1, counter.map['w'])
    }
    @Test
    fun testMinusAssignWithIterable() {
        val counter = Counter("which".asIterable())
        counter -= "witch".asIterable()
        counter -= "watch".asIterable()
        assertEquals(0, counter.map['h'])
        assertEquals(-1, counter.map['w'])
    }
    @Test
    fun testMinusWithCounter() {
        val counter = Counter("which".asIterable())
        counter - Counter("witch".asIterable())
        counter - Counter("watch".asIterable())
        assertEquals(2, counter.map['h'])
        assertEquals(1, counter.map['w'])
    }
    @Test
    fun testMinusWithIterable() {
        val counter = Counter("which".asIterable())
        counter - "witch".asIterable()
        counter - "watch".asIterable()
        assertEquals(2, counter.map['h'])
        assertEquals(1, counter.map['w'])
    }
    @Test
    fun testPlusAssignWithCounter() {
        val counter = Counter("which".asIterable())
        counter += Counter("witch".asIterable())
        counter += Counter("watch".asIterable())
        assertEquals(4, counter.map['h'])
        assertEquals(3, counter.map['w'])
    }
    @Test
    fun testPlusAssignWithIterable() {
        val counter = Counter("which".asIterable())
        counter += "witch".asIterable()
        counter += "watch".asIterable()
        assertEquals(4, counter.map['h'])
        assertEquals(3, counter.map['w'])
    }
    @Test
    fun testPlusWithCounter() {
        val counter = Counter("which".asIterable())
        counter + Counter("witch".asIterable())
        counter + Counter("watch".asIterable())
        assertEquals(2, counter.map['h'])
        assertEquals(1, counter.map['w'])
    }
    @Test
    fun testPlusWithIterable() {
        val counter = Counter("which".asIterable())
        counter + "witch".asIterable()
        counter + "watch".asIterable()
        assertEquals(2, counter.map['h'])
        assertEquals(1, counter.map['w'])
    }
}
```

If all tests is successfull, means the code implementation is correct.

*   **Full code for Kotlin**

```

class Counter<T>() {
    constructor(iterable: Iterable<T>): this() {
        _map = hashMapOf<T, Int>().apply {
            for (k in iterable) set(k, if (containsKey(k)) get(k)!! + 1 else 1)
        }
    }
    constructor(map: Map<T, Int>): this() {
        _map = hashMapOf<T, Int>().apply { putAll(map) }
    }
    /**
     * Mutable map to store value
     */
    private var _map: HashMap<T, Int> = hashMapOf()
    /**
     * Immutable map
     */
    val map: Map<T, Int>
        get() = _map.toMap()
    /**
     * Sum of the counts
     */
    fun total(): Int = _map.values.sum()
    /**
     * List the n most common elements and their counts from the most
     * common to the least.
     *
     * >>> Counter('abracadabra').mostCommon(3)
     * [('a', 5), ('b', 2), ('r', 2)]
     */
    fun mostCommon(n: Int): Map<T, Int> {
        val sorted = _map.entries.sortedByDescending { it.value }
        return buildMap {
            var count = 0
            for ((k, v) in sorted) if (count < n) put(k, v).also { count++ } else break
        }
    }
    /**
     * add counts instead of replacing them.
     *
     * >>> val c = Counter("which".asIterable())
     * >>> c.update("witch".asIterable())           # add elements from another iterable
     * >>> val d = Counter("watch".asIterable())
     * >>> c.update(d)                              # add elements from another counter
     * >>> c.map['h']                               # four 'h' in which, witch, and watch
     * 4
     */
    fun update(other: Counter<T>): Counter<T> {
        plusAssign(other)
        return this
    }
    /**
     * add counts instead of replacing them.
     *
     * >>> val c = Counter("which".asIterable())
     * >>> c.update("witch".asIterable())           # add elements from another iterable
     * >>> val d = Counter("watch".asIterable())
     * >>> c.update(d)                              # add elements from another counter
     * >>> c.map['h']                               # four 'h' in which, witch, and watch
     * 4
     */
    fun update(other: Iterable<T>): Counter<T> {
        plusAssign(other)
        return this
    }
    /**
     * add counts instead of replacing them.
     *
     * >>> val c = Counter("which".asIterable())
     * >>> c.update("witch".asIterable())           # add elements from another iterable
     * >>> val d = Counter("watch".asIterable())
     * >>> c.update(d)                              # add elements from another counter
     * >>> c.map['h']                               # four 'h' in which, witch, and watch
     * 4
     */
    fun update(other: Map<T, Int>): Counter<T> {
        plusAssign(other)
        return this
    }
    /**
     * Subtract count.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minusAssign(other: Counter<T>) {
        _map = minus(other)._map
    }
    /**
     * Subtract count.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minusAssign(other: Iterable<T>) {
        _map = minus(other)._map
    }
    /**
     * Subtract count.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minusAssign(other: Map<T, Int>) {
        _map = minus(other)._map
    }
    /**
     * Subtract count and return new [Counter] object.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minus(other: Counter<T>): Counter<T> {
        return copy().apply {
            for ((k, v) in other.map) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! - v else -v
            }
        }
    }
    /**
     * Subtract count and return new [Counter] object.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minus(other: Iterable<T>): Counter<T> {
        return copy().apply {
            for (k in other) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! - 1 else -1
            }
        }
    }
    /**
     * Subtract count and return new [Counter] object.
     * Counts can be reduced below zero. Both the inputs and outputs are
     * allowed to contain zero and negative counts.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # subtract elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # subtract elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 0
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * -1
     */
    operator fun minus(other: Map<T, Int>): Counter<T> {
        return copy().apply {
            for ((k, v) in other) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! - v else -v
            }
        }
    }
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plusAssign(other: Counter<T>) {
        _map = plus(other)._map
    }
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plusAssign(other: Iterable<T>) {
        _map = plus(other)._map
    }
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plusAssign(other: Map<T, Int>) {
        _map = plus(other)._map
    }
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plus(other: Counter<T>): Counter<T> {
        return copy().apply {
            for ((k, v) in other.map) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! + v else v
            }
        }
    }
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plus(other: Iterable<T>): Counter<T> {
        return copy().apply {
            for (k in other) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! + 1 else 1
            }
        }
    }
    /**
     * Add count and return new [Counter] object.
     *
     * >>> c = Counter("which".asIterable())
     * >>> c.subtract("witch".asIterable())             # add elements from another iterable
     * >>> c.subtract(Counter("watch".asIterable()))    # add elements from another counter
     * >>> c['h']                                       # 2 in which, minus 1 in witch, minus 1 in watch
     * 4
     * >>> c['w']                                       # 1 in which, minus 1 in witch, minus 1 in watch
     * 3
     */
    operator fun plus(other: Map<T, Int>): Counter<T> {
        return copy().apply {
            for ((k, v) in other) {
                _map[k] = if (_map.containsKey(k)) _map[k]!! + v else v
            }
        }
    }
    /**
     * Copy [Counter] instance
     */
    fun copy(): Counter<T> = Counter(hashMapOf<T, Int>().apply { putAll(map) })
}
```

*   **Full code for Java**

```
import org.jetbrains.annotations.NotNull;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicReference;
public class CounterJava<T> {
    /**
     * Mutable map to store value
     */
    private HashMap<T, Integer> _map;
    public CounterJava(@NotNull Iterable<T> iterable) {
        HashMap<T, Integer> mmap = new HashMap<>();
        for (T t : iterable) mmap.put(t, mmap.containsKey(t) ? mmap.get(t) + 1 : 1);
        _map = mmap;
    }
    public CounterJava(Map<T, Integer> map) {
        _map = new HashMap<>(map);
    }
    /**
     * Get value
     */
    public Map<T, Integer> getMap() {
        return _map;
    }
    /**
     * Sum of the counts
     */
    public Integer total() {
        AtomicReference<Integer> sum = new AtomicReference<>(0);
        _map.forEach((t, integer) -> sum.updateAndGet(v -> v + integer));
        return sum.get();
    }
    public Map<T, Integer> mostCommon(Integer n) {
        HashMap<T, Integer> mmap = new HashMap<>();
        _map.entrySet()
                .stream()
                .sorted((o1, o2) -> o2.getValue().compareTo(o1.getValue()))
                .forEach(tIntegerEntry -> {
                    mmap.put(tIntegerEntry.getKey(), tIntegerEntry.getValue());
                });
        return mmap;
    }
    public CounterJava<T> update(CounterJava<T> other) {
        _map = plus(other)._map;
        return this;
    }
    public CounterJava<T> update(Iterable<T> other) {
        _map = plus(other)._map;
        return this;
    }
    public CounterJava<T> update(Map<T, Integer> other) {
        _map = plus(other)._map;
        return this;
    }
    public CounterJava<T> minus(@NotNull CounterJava<T> other) {
        CounterJava<T> copy = copy();
        other.getMap().forEach((t, integer) -> copy._map.put(t, copy._map.containsKey(t) ? copy._map.get(t) - integer : -integer));
        return copy;
    }
    public CounterJava<T> minus(@NotNull Iterable<T> other) {
        CounterJava<T> copy = copy();
        other.forEach((t) -> copy._map.put(t, copy._map.containsKey(t) ? copy._map.get(t) - 1 : -1));
        return copy;
    }
    public CounterJava<T> minus(@NotNull Map<T, Integer> other) {
        CounterJava<T> copy = copy();
        other.forEach((t, integer) -> copy._map.put(t, copy._map.containsKey(t) ? copy._map.get(t) - integer : -integer));
        return copy;
    }
    public CounterJava<T> plus(@NotNull CounterJava<T> other) {
        CounterJava<T> copy = copy();
        other.getMap().forEach((t, integer) -> copy._map.put(t, copy._map.containsKey(t) ? copy._map.get(t) + integer : integer));
        return copy;
    }
    public CounterJava<T> plus(@NotNull Iterable<T> other) {
        CounterJava<T> copy = copy();
        other.forEach((t) -> copy._map.put(t, copy._map.containsKey(t) ? copy._map.get(t) + 1 : 1));
        return copy;
    }
    public CounterJava<T> plus(@NotNull Map<T, Integer> other) {
        CounterJava<T> copy = copy();
        other.forEach((t, integer) -> copy._map.put(t, copy._map.containsKey(t) ? copy._map.get(t) + integer : integer));
        return copy;
    }
    public CounterJava<T> copy() {
        return new CounterJava<>(new HashMap<>(_map));
    }
}
```

**Thankyou for reading
∧,,,∧
( ̳• · • ̳)
/ づ**❤