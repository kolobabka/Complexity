#include <iostream>
#include <vector>
#include <future>
#include <algorithm>
#include <random>
#include <thread>
#include <chrono>

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

int main() {
    unsigned N;
    std::cin >> N;
    if (!std::cin) {
      std::cerr << "Please, provide positive integer number" << std::endl;
      return -1;
    }

    std::vector<int> arr(N);
    std::iota(arr.begin(), arr.end(), N);
    
    std::mt19937 g(123);
    
    std::shuffle(arr.begin(), arr.end(), g);

     
    auto TotalNumThreads = std::thread::hardware_concurrency();
    std::cout << "Total thread number : " << TotalNumThreads << std::endl; 

    for (auto NumThreads = 1u; NumThreads <= TotalNumThreads; ++NumThreads) { 
      std::vector<int> toSort(arr.begin(), arr.end());

      auto start = std::chrono::high_resolution_clock::now();
      
      parallelQuickSort(toSort, 0, toSort.size() - 1, std::thread::hardware_concurrency() - NumThreads);
 
      auto stop = std::chrono::high_resolution_clock::now();

      if (!std::is_sorted(toSort.begin(), toSort.end())) {
        std::cerr << "Sorting algo is broken" << std::endl; 
        return -1;
      }
      
      auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
      std::cout << "Parallel with " << NumThreads << " threads : " << duration.count() << "s" << std::endl; 
    }
    
    return 0;
}

