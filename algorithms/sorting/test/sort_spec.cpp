#include "sorting/sort.h"

#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include <thread>

template <typename T>
void Print(const std::vector<T>& vector)
{
  for (size_t i = 0; i < vector.size(); ++i)
  {
    if (i < vector.size() - 1)
    {
      std::cout << vector[i] << ", ";
    }
    else
    {
      std::cout << vector[i];
    }
  }
  std::cout << std::endl;
}

TEST(MergeSortSpec, GivenUnsortedIntegerVector_CheckOutputOrder)
{
  std::vector<int> numbers{340, 10, 4, 23, 5, 7, -9, 90};
  std::vector<int> expected_numbers{-9, 4, 5, 7, 10, 23, 90, 340};
  const auto sorted_numbers = algorithms::MergeSort(numbers);
  EXPECT_THAT(sorted_numbers, ::testing::ElementsAreArray(expected_numbers));
}

TEST(BubbleSortSpec, GivenUnsortedIntegerVector_CheckOutputOrder)
{
  std::vector<int> numbers{340, 10, 4, 23, 5, 7, -9, 90};
  std::vector<int> expected_numbers{-9, 4, 5, 7, 10, 23, 90, 340};
  const auto sorted_numbers = algorithms::BubbleSort(numbers);
  EXPECT_THAT(sorted_numbers, ::testing::ElementsAreArray(expected_numbers));
}

TEST(BubbleSortSpec, GivenUnsortedFloatVector_CheckOutputOrder)
{
  std::vector<float> numbers{40.0, -10.25, 4.5, 2.3, 235.1, 7.0, -9.9, 90.0};
  std::vector<float> expected_numbers{-10.25, -9.9, 2.3, 4.5, 7.0, 40.0, 90.0, 235.1};
  const auto sorted_numbers = algorithms::BubbleSort(numbers);
  EXPECT_THAT(sorted_numbers, ::testing::ElementsAreArray(expected_numbers));
}