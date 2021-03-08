#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include <vector>

#include "multi_threading/spin_lock.hpp"

namespace {

class SharedResource
{
  public:
    void AddValueTenTimes(const int value)
    {
      lock_.Lock();
      int counter{0};
      while (counter < 10)
      {
        result_ += value;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        ++counter;
      };
      lock_.Unlock();
    }

    int GetResult() { return result_;}

  private:
    int result_{0};
    utilities::Spinlock lock_{};
};

TEST(SpinLockSpec, GivenTwoWorkerThreads_LockSharedResource)
{
  int first_increment{5};
  int second_increment{10};
  SharedResource sut;
  std::thread first_worker{&SharedResource::AddValueTenTimes, &sut, first_increment};
  std::thread second_worker{&SharedResource::AddValueTenTimes, &sut, second_increment};

  first_worker.join();
  second_worker.join();
  EXPECT_EQ(10*(first_increment+second_increment), sut.GetResult());
}
} // namespace anonymous