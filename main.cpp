#include <iostream>
class myClass
{
public:
    myClass() = default;
    void leak()
    {
        int * a = new int(5);
    }
    int uninit()
    {
        int * b;
        return *b;
    }
};

int main()
{
    myClass a;
    a.leak();
    int i=a.uninit();
    (void)i;
    std::cout << " hola" << std::endl;
    return 0;
}
