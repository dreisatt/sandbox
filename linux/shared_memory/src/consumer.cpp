#include <iostream>
#include <shared_memory/shared_memory_consumer.h>

int main(int argc, char** argv)
{
    std::cout << "Shared memory consumer started and running...." << std::endl;
    SharedMemoryConsumer data_consumer;
    if (!data_consumer.Open())
    {
        return 1;
    }
    char* data_pointer{nullptr};
    int size = data_consumer.Read(&data_pointer);
    std::cout << data_pointer << std::endl;
    size = data_consumer.Read(&data_pointer);
    std::cout << data_pointer << std::endl;
    return 0;
}
