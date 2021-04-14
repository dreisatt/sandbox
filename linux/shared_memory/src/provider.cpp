#include <shared_memory/shared_memory_provider.h>
#include <iostream>
#include <thread>

int main(int argc, char** argv)
{
    std::cout << "Shared memory provider started and running...." << std::endl;
    SharedMemoryProvider data_provider;
    char hello_niko[] = "Hello Niko";
    char bye_altran[] = "Bye Altran";
    data_provider.Create(6000);
    data_provider.Write(hello_niko, 11);
    std::this_thread::sleep_for(std::chrono::seconds(6));
    data_provider.Write(bye_altran, 11);
    std::cout << "Done writing data to shared memory, shutting done...." << std::endl;
    return 0;
}