#include "spin_lock.hpp"
#include <immintrin.h>

namespace utilities
{
void Spinlock::Lock() noexcept
{
  for (;;)
  {
    if (!lock_.exchange(true, std::memory_order_acquire))
    {
      return;
    }
    else
    {
      while (lock_.load(std::memory_order_relaxed))
      {
        _mm_pause();
      }
    }
  }
}

void Spinlock::Unlock() noexcept
{
  lock_.exchange(false, std::memory_order_release);
}

bool Spinlock::TryLock() noexcept
{
  if (!lock_.load(std::memory_order_relaxed))
  {
    lock_.exchange(true, std::memory_order_acquire);
    return true;
  }
  else
  {
    return false;
  }
}
}  // namespace utilities