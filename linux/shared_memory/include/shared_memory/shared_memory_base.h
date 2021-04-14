#ifndef SHARED_MEMORY_BASE_H
#define SHARED_MEMORY_BASE_H

/// System includes
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <semaphore.h>
#include <unistd.h>
#include <fcntl.h>
#include <string>

struct SharedDataHeader
{
    int id{-1};
    int payload{-1};
    bool changed{false};
    bool observed{false};
};

class SharedMemoryBase
{
public:
    SharedMemoryBase();
    virtual ~SharedMemoryBase() = default;

protected:
    /// Pointer to origin of shared memory segment
    void* memory_{nullptr};
    /// Pointer to current data in shared memory segment
    char* data_{nullptr};
    /// Message counter
    int message_id_{0};
    /// File name of shared memory segment
    std::string shared_fd_name_{"/shared_memory"};
    /// Shared memory file handle
    int fd_{-1};
    /// Shared memory segment opened and initialized
    bool ready_{false};

    /// Sync semaphore
    sem_t* producer_consumer_semaphore_{nullptr};
    std::string semaphore_name_{"/producer_consumer_semaphore"};

private:
    virtual bool InitializeFileDescriptor() = 0;
    virtual bool InitializeSemaphore() = 0;
};


#endif // SHARED_MEMORY_BASE_H
