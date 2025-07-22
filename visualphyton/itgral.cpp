#include<iostream>
using namespace std;

double f(double x)
 {
    return x*x;   //x al cuadrado
    //return sin(x) * abs(x);
 }

auto main() -> int
{
    double minx =-10;
    double maxx =10;
    double miny =-10;
    double maxy =10;
    
    cout << "x    |    y"<<endl <<"------------"<<endl;
    for (double x=minx;x<=maxx;x=x + 0.1)
    {
        double y=f(x);
        cout<<x<<"|"<<y<<endl;
    }
    return 0;

}