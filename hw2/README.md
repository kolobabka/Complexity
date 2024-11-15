# Part 1

Let's consider quicksort algo. It's easy to implement the parallel version with devide and conquer strategy

```c++
int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; ++j) {
        if (arr[j] <= pivot) {
            ++i;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pivot = partition(arr, low, high);
        quickSort(arr, low, pivot - 1);
        quickSort(arr, pivot + 1, high); 
    }
}
```

The parallel version:

```c++
void parallelQuickSort(std::vector<int>& arr, int low, int high, int depth = 1) {
    if (low < high) {
        int pivot = partition(arr, low, high);

        if (depth >= std::thread::hardware_concurrency()) {
            parallelQuickSort(arr, low, pivot - 1, depth + 1);
            parallelQuickSort(arr, pivot + 1, high, depth + 1);
        } else {
            std::future<void> left = std::async(std::launch::async, parallelQuickSort, std::ref(arr), low, pivot - 1, depth + 1);
            std::future<void> right = std::async(std::launch::async, parallelQuickSort, std::ref(arr), pivot + 1, high, depth + 1);
            left.get();
            right.get();
        }
    }
}
```

The complexity for quicksort algorithm 

$$
    \theta \left( n \cdot log \left( n \right) \right) \text{on average}
$$
$$
    \theta \left( n^{2} \right) \text{worst case}
$$


Parallelism can be estimated as the ratio of the total work to the span:

$$
    Parallelism = \frac{Work}{Span}
$$

**Work** is a complexity for non-parallel algorithm

**Span**  is a critical path in a graph of work, so

$$
Span = \theta \left (log \left( n \right) \right)
$$

$$
    Parallelism = \frac{Work}{Span} = \frac{\theta \left( n \cdot log \left( n \right) \right)}{\theta \left (log \left( n \right) \right)} = \theta \left( n \right)
$$

# Part 2

The theoretical parallelism $ \theta \left (n \right) $ suggests that quicksort can achieve near-linear speedup with increasing processors up to about n processors, assuming ideal conditions.
But in practice,  real-life scaling is influenced by several factors that cause deviations from theoretical predictions
* **Threads** : Creating, managing, and synchronizing threads introduces overhead that increases with more threads. Moreover, there is the Amdahl's law blocked the perfomance increasing 
* **Cache and memory bandwidth**: As threads access shared memory, contention for cache and memory bandwidth can slow down the effective speedup.

Let's measure it:

```
50000000
Total thread number : 12
Parallel with 1 threads : 100s
Parallel with 2 threads : 91s
Parallel with 3 threads : 71s
Parallel with 4 threads : 66s
Parallel with 5 threads : 55s
Parallel with 6 threads : 59s
Parallel with 7 threads : 43s
Parallel with 8 threads : 36s
Parallel with 9 threads : 36s
Parallel with 10 threads : 34s
Parallel with 11 threads : 33s
Parallel with 12 threads : 33s
```

We can see that scaling decrease with increasing thread numbers. But there are surgers. I believe it's because of better cache efficiency for certain CPUs with increasing thread numbers. 

To improve the results, I can suggest increase TLB pages size for the OS, enable hyper-threading in BIOS (is it's provided with your CPU) and using vector builtins for vector instruction. The last one is relevant, because with parallel executions compilers doesn't optimizize code as good as it possible. 