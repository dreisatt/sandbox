#ifndef MULTI_THREADING_SPIN_LOCK_H
#define MULTI_THREADING_SPIN_LOCK_H
#include <atomic>

namespace utilities
{
// Inspired by https://rigtorp.se/spinlock/
class Spinlock
{
 public:
  void Lock() noexcept;
  void Unlock() noexcept;
  bool TryLock() noexcept;

 private:
  std::atomic<bool> lock_{false};
};
}  // namespace utilities

#endif  // MULTI_THREADING_SPIN_LOCK_H