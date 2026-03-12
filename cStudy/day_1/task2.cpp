#include <iostream>
using namespace std;


//컴파일 : ctrl alt c
// 실행 : ctrl alt r

int main(){

    cout << "아스키코드 출력하기 [32~126]\n";
    
    for(char i=32; i<=126; i++){
        cout << i << ((i%16==15)?'\n':' ');
    }


}