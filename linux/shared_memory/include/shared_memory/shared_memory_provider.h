#ifndef SHARED_MEMORY_PROVIDER_H
#define SHARED_MEMORY_PROVIDER_H

/// Project includes
#include <shared_memory/shared_memory_base.h>

class SharedMemoryProvider : public SharedMemoryBase
{
public:
    SharedMemoryProvider();
    SharedMemoryProvider(size_t size);

    ~SharedMemoryProvider();

    /**
     * Create file with page aligned size and map it to memory
     *
     * @param[in] size Size of allocated memory
     * @return True, if successful
     */
    bool Create(size_t size);
    /**
    * Copy data to shared memory segment
    *
    * @param[in] data Pointer to data written to shared memory
    * @param[in] size Size of data to written to shared memory
    * @return True, if successful
    */
    bool Write(char* data, size_t size);

    bool Resize(size_t size);
private:
    bool InitializeFileDescriptor() final;

    bool InitializeSemaphore() final;

    int memory_page_size_{0};
    /// Total size of shared memory segment - page aligned
    size_t allocated_size_{0};
    size_t free_size_{0};
};

#endif // SHARED_MEMORY_PROVIDER_H