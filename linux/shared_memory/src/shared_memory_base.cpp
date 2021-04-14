#include <shared_memory/shared_memory_base.h>

SharedMemoryBase::SharedMemoryBase()
{
    if(InitializeFileDescriptor())
    {
        if (InitializeSemaphore())
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