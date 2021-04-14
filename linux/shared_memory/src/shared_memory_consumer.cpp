#include <shared_memory/shared_memory_consumer.h>
#include <iostream>
#include <cerrno>
#include <cstring>

SharedMemoryConsumer::SharedMemoryConsumer()
{
    InitializeFileDescriptor();
}

SharedMemoryConsumer::~SharedMemoryConsumer()
{
    if (munmap(memory_, allocated_size_) == -1)
    {
        std::cout << "Unmapping the shared memory segment failed: " << strerror(errno) << std::endl;
    }
    if (close(fd_) == -1)
    {
        std::cout << "Closing the shared memory descriptor failed: " << strerror(errno) << std::endl;
    }
    if(shm_unlink(shared_fd_name_.c_str()))
    {
        std::cout << "Destroying the shared memory descriptor failed: " << strerror(errno) << std::endl;
    }
    delete [] buffer_;
}

bool SharedMemoryConsumer::Open()
{
    if (!ready_)
    {
        memory_ = mmap(nullptr, allocated_size_, PROT_READ, MAP_SHARED, fd_, 0);
        data_ = (char*) memory_;
        InitializeBuffer();
        ready_  = true;
        return true;
    }
    else
    {
        //TODO: Does the else condition make any sense?
        return false;
    }
}

int SharedMemoryConsumer::Read(char** data)
{
    SharedDataHeader* header = (SharedDataHeader* ) data_;
    std::copy(data_, data_ + header->payload, buffer_);
    header->observed = true;
    header->changed = false;
    data_ += header->payload + sizeof(SharedDataHeader);
    *data = buffer_;
    return header->payload;
}

/////////////////////////
/// Private Functions ///
/////////////////////////
bool SharedMemoryConsumer::InitializeFileDescriptor()
{
    fd_ = shm_open(shared_fd_name_.c_str(), O_RDONLY, S_IRWXU);

    if (fd_ == -1)
    {
        std::cout << "Opening and/or creating the file handle to the shared memory segment failed: " << strerror(errno) << std::endl;
        return false;
    }
    else
    {
        if(fstat(fd_, &file_information_) == -1)
        {
            std::cout << "Can't read file information: " << strerror(errno) << std::endl;
            return false;
        }
        else
        {
            allocated_size_ = file_information_.st_size;
            return true;
        }
    }
}

void SharedMemoryConsumer::InitializeBuffer()
{
    buffer_ = new char[allocated_size_];
}

bool SharedMemoryConsumer::InitializeSemaphore()
{
    producer_consumer_semaphore_= sem_open(semaphore_name_.c_str(), O_CREAT, S_IRWXU);
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