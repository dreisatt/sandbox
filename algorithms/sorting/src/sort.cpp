#include "sorting/sort.h"
#include <iostream>

namespace algorithms
{
namespace detail
{
void MergeSortImpl(std::vector<int>& input, size_t left, size_t right)
{
    if (left == right)
    {
        return;
    }
    size_t center = (right + left)/2;
    MergeSortImpl(input, left, center);
    MergeSortImpl(input, center + 1, right);
    size_t j = left;
    size_t k = center + 1;
    std::vector<int> output{};
    for (size_t i = 0; i <= right-left; ++i)
    {
        if (j > center)
        {
            output.push_back(input[k]);
            k++;
        }
        else
        {
            if (k > right)
            {
                output.push_back(input[j]);
                ++j;
            }
            else
            {
                if (input[j] <= input[k])
                {
                    output.push_back(input[j]);
                    ++j;
                }
                else
                {
                    output.push_back(input[k]);
                    ++k;
                }
            }
        } 
    }
    for (size_t i = 0; i <= right-left; ++i)
    {
        input[left+i] = output[i]; 
    }
}
}  // namespace detail

std::vector<int> MergeSort(const std::vector<int> input) 
{
    std::vector<int> result{};
    if (!input.empty())
    {
        const size_t only_one_element{1};
        const size_t input_size = input.size();
        if (input.size() == only_one_element)
        {
            return input;
        }
        else
        {
            result = input;
            detail::MergeSortImpl(result, 0, input_size-1);
        }
    }
    return result;
}

template <typename T>
std::vector<T> BubbleSort(const std::vector<T> input)
{
    std::vector<T> result{input};
    if (!result.empty())
    {
        for (size_t j = 1; j < result.size(); ++j)
        {
            for (size_t i = result.size(); (i--) > j;)
            {
                if (result[i] < result[i-1])
                {
                    const T tmp = result[i];
                    result[i] = result[i-1];
                    result[i-1] = tmp;
                }
            }
        }
    }
    return result;
}

template std::vector<int> BubbleSort(std::vector<int> input);
template std::vector<float> BubbleSort(std::vector<float> input);
template std::vector<double> BubbleSort(std::vector<double> input);
}  // namespace algorithms