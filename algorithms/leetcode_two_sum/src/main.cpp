#include <algorithm>
#include <iostream>
#include <map>
#include <vector>

class Solution
{
 public:
  virtual std::vector<int> Solve(std::vector<int>& nums, const int target) = 0;
};

class TwoSumUsingStdFind : public Solution
{
 public:
  std::vector<int> Solve(std::vector<int>& nums, const int target) override
  {
    std::vector<int> result{};
    for (auto jt = nums.begin(); jt != nums.end(); jt++)
    {
      const auto value = *jt;
      if (value < target)
      {
        int missing = target - value;
        const auto it = std::find(nums.begin(), nums.end(), missing);
        if (it != nums.end())
        {
          result.push_back(jt - nums.begin());
          result.push_back(it - nums.begin());
          break;
        }
      }
    }
    return result;
  }
};

class TwoSumUsingStdMap : public Solution
{
 public:
  std::vector<int> Solve(std::vector<int>& nums, const int target) override
  {
    std::vector<int> result{};
    std::map<int, int> num_to_index{};

    for (auto it = nums.begin(); it != nums.end(); ++it)
    {
      num_to_index.insert({*it, it - nums.begin()});
    }

    for (auto jt = nums.begin(); jt != nums.end(); jt++)
    {
      const auto value = *jt;
      if (value < target)
      {
        int missing = target - value;
        const auto num_and_index = num_to_index.find(missing);
        if (num_and_index != num_to_index.end())
        {
          result.push_back(jt - nums.begin());
          result.push_back(num_and_index->second);
          break;
        }
      }
    }
    return result;
  }
};

void Print(const std::vector<int>& vector)
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

int main(void)
{
  std::vector<int> numbers{2, 7, 11, 35, 45};
  const int target{56};
  TwoSumUsingStdFind find_sum{};
  const auto find_result = find_sum.Solve(numbers, target);
  std::cout << "Result using std::find: ";
  Print(find_result);
  TwoSumUsingStdMap map_sum{};
  const auto map_result = map_sum.Solve(numbers, target);
  std::cout << "Result using std::map: ";
  Print(map_result);
  return 0;
}