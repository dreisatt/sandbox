#ifndef SHARED_MEMORY_CONSUMER_H
#define SHARED_MEMORY_CONSUMER_H

/// Project includes
#include <shared_memory/shared_memory_base.h>

class SharedMemoryConsumer : public SharedMemoryBase
{
public:
    SharedMemoryConsumer();
    ~SharedMemoryConsumer();
    
    bool Open();
    int Read(char** data);

private:
    bool InitializeFileDescriptor() final;
    bool InitializeSemaphore() final;
    void InitializeBuffer();

    char* buffer_{nullptr};
    size_t allocated_size_{0};
    struct stat file_information_;
};

#endif // SHARED_MEMORY_CONSUMER_H