#ifndef OPISINGLETON
#define OPISINGLETON

#ifndef NULL
#define NULL 0
#endif

namespace opi2d
{
    template<class T>
    class Singleton
    {
    public:
        inline static T* GetInstance()
        {
            return instance;
        }
        static void Init()
        {
            instance = new T();
        }
        static void Destroy()
        {
            if (instance != NULL)
            {
                delete instance;
                instance = NULL;
            }
        }
    
    protected:
        static T* instance;
    };
    
    template<class T>
    T* Singleton<T>::instance = NULL;
}

#endif

