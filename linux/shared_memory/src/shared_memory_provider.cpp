#include <shared_memory/shared_memory_provider.h>
#include <iostream>
#include <cerrno>
#include <cstring>

SharedMemoryProvider::SharedMemoryProvider() : SharedMemoryBase()
{
}

SharedMemoryProvider::SharedMemoryProvider(size_t size) : SharedMemoryBase(), allocated_size_(size), free_size_(size)
{
    InitializeFileDescriptor();
    if (InitializeSemaphore())
    {
        if (Create(size))
        {
            ready_ = true;
        }
        else
        {
            ready_ = false;
        }
    }
    else
    {
        ready_ = false;
    }
}

SharedMemoryProvider::~SharedMemoryProvider()
{
    if (memory_)
    {
        if (munmap(memory_, allocated_size_) == -1)
        {
            std::cout << "Unmapping the shared memory segment failed: " << strerror(errno) << std::endl;
        }
    }
    if (fd_ != -1)
    {
        if (close(fd_) == -1)
        {
            std::cout << "Closing shared memory descriptor failed: " << strerror(errno) << std::endl;
        }
    }
}

bool SharedMemoryProvider::Create(size_t size)
{
    if (size <= memory_page_size_)
    {
        std::cout << "Requested size: " << size << "smaller than page size." << std::endl;
        allocated_size_ = memory_page_size_;
    }
    else
    {
        allocated_size_ = ((size + (memory_page_size_ - 1)) & ~(memory_page_size_ - 1));
    }
    free_size_ = allocated_size_;
    if (ftruncate(fd_, allocated_size_) == -1)
    {
        std::cout << "Enlarging the size of the file handle to " << size << " Bytes failed." << std::endl;
        return false;
    }
    else
    {
        memory_ = mmap(nullptr, allocated_size_, (PROT_READ | PROT_WRITE), MAP_SHARED, fd_, 0);
        if (memory_ == MAP_FAILED)
        {
            return false;
        }
        else
        {
            data_ = (char*) memory_;
            ready_ = true;
            return true;
        }
    }
}

bool SharedMemoryProvider::Write(char* data, size_t size)
{
    if (ready_)
    {
        if (size <= (allocated_size_ - sizeof(SharedDataHeader)))
        {
            /// Create and fill message header
            SharedDataHeader* header = new (data_) SharedDataHeader();
            header->id = message_id_;
            header->payload = size;
            header->changed = true;
            data_ += sizeof(SharedDataHeader);
            /// Copy payload to shared memory
            std::copy(data, data+size, data_);
            data_ += size;
            free_size_ -= (size + sizeof(SharedDataHeader));
            ++message_id_;
            return true;
        }
        else
        {
            std::cout << "Not enough memory allocated. Please increase size. " << std::endl;
            return false;
        }
    }
    else
    {
        std::cout << "Shared memory not initialized properly. Please call Create(size) before." << std::endl;
        return false;
    }
}

bool SharedMemoryProvider::Resize(size_t size)
{
    size_t old_allocated_size = allocated_size_;
    if (size <= memory_page_size_)
    {
        std::cout << "Requested size: " << size << "smaller than page size." << std::endl;
        allocated_size_ += memory_page_size_;
    }
    else
    {
        // Align to next bigger page size e.g. 5000 Bytes -> 8192 Bytes
        size_t page_aligned_size = ((size + (memory_page_size_ - 1)) & ~(memory_page_size_ - 1));
        allocated_size_ += page_aligned_size;
    }

    if (ftruncate(fd_, allocated_size_) == -1)
    {
        std::cout << "Enlarging the size of the file handle to " << size << " Bytes failed." << std::endl;
        return false;
    }
    else
    {
        memory_ = mremap(memory_, old_allocated_size, allocated_size_, MREMAP_MAYMOVE);
        if (memory_ == MAP_FAILED)
        {
            return false;
        }
        else
        {
            data_ = (char*) memory_;
            return true;
        }
    }
}

/////////////////////////
/// Private Functions ///
/////////////////////////
bool SharedMemoryProvider::InitializeFileDescriptor()
{
    memory_page_size_ = getpagesize();
    fd_ = shm_open(shared_fd_name_.c_str(), (O_RDWR | O_CREAT), S_IRWXU);

    if (fd_ == -1)
    {
        std::cout << "Opening and/or creating the file handle to the shared memory segment failed. " << strerror(errno) << std::endl;
        return false;
    }
    else
    {
        return true;
    }
}

bool SharedMemoryProvider::InitializeSemaphore()
{
    producer_consumer_semaphore_= sem_open(semaphore_name_.c_str(), (O_CREAT | O_RDWR), S_IRWXU);
    if (producer_consumer_semaphore_ == SEM_FAILED)
    {
        std::cout << "Create/Open shared semaphore failed: " << strerror(errno) << std::endl;
        return false;
    }
    else
    {
        return true;
    }
}