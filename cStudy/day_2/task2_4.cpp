#include <iostream>
using namespace std;

void print(){
    int value = 10;
    cout << "print 함수 내의 value 값 : " << value << endl;
}
int value1 = 1;

int main(){
    int value = 5;
    cout << "main 함수 내의 value 값 : " << value << endl;
    print();
    cout << "다시 main 함수 내의 value 값 : " << value << endl;

    int value1 = -1;

    cout << value1 << endl;
    cout << ::value1 << endl;
    
    return 0;
}
