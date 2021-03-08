#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include <vector>

#include "multi_threading/spin_lock.hpp"

namespace {

class SharedResource
{
  public:
    void AddValue(const std::string value)
    {
      lock_.Lock();
      if (!result_.empty())
      {
        result_.append(value);
      }
      std::this_thread::sleep_for(std::chrono::milliseconds(500));
      if (result_.empty())
      {
        result_.append(value);
      }
      lock_.Unlock();
    }

    const std::string& GetResult() {return result_;}

  private:
    std::string result_{""};
    utilities::Spinlock lock_{};
};

TEST(SpinLockSpec, GivenTwoWorkerThreads_LockSharedResource)
{
  std::string first{"first"};
  std::string second{"second"};
  SharedResource sut;
  std::thread first_worker{&SharedResource::AddValue, &sut, first};
  std::this_thread::sleep_for(std::chrono::milliseconds(100));
  std::thread second_worker{&SharedResource::AddValue, &sut, second};

  first_worker.join();
  second_worker.join();
  EXPECT_EQ(first+second, sut.GetResult());
}
} // namespace anonymous