#ifndef ALGORITHMS_SORTING_H
#define ALGORITHMS_SORTING_H
#include <vector>

namespace algorithms
{
std::vector<int> MergeSort(std::vector<int> input);

template <typename T>
std::vector<T> BubbleSort(std::vector<T> input);
}  // namespace algorithms

#endif  // ALGORITHMS_SORTING_H