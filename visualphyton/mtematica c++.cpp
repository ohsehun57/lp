/*#include <iostream>

double raizcuadrada(double n)
{
    if (n < 0) return -1;

    double x = n;
    double y = 1;
    double e = 0.000001; // precisión

    std::cout << "---> " << n << "/" << x << "\t\t\t" << y << " : " << x - y << std::endl;

    while ((x - y) > e)
    {
        x = (x + y) / 2;
        y = n / x;

        std::cout << "---> " << n << " / " << x << "\t\t" << y << " : " << x - y << std::endl;
    }

    return x;
}
double potencia(double base,double exponente)
{
    double respuesta = 1;
    for(int i=0; i < exponente ; i++ )
        respuesta = respuesta * base;
    return respuesta;
}

auto main() -> int
{
    double num;
    std::cout<<"ingrese un numero";
    std::cin>>num;
    double raiz = raizcuadrada(num);
    double potencia1 = potencia(num,2);
    double potencia2 = potencia(num,3);
    std::cout<<"raiz cuadrada :"<<raiz<<std::endl;
    std::cout<<"al cuadrado :"<<potencia1<<std::endl;
    std::cout<<"al cubo :"<<potencia2<<std::endl;
    return 0;
}


*/
#include<iostream>
using namespace std;

// Función para calcular el logaritmo natural usando serie de Taylor
double ln(double x) {
    if (x <= 0) return -1; // Error para valores no positivos
    
    // Usamos la fórmula ln(x) = 2 * suma[ (1/(2*k+1)) * ((x-1)/(x+1))^(2k+1) ]
    double y = (x - 1) / (x + 1);
    double y2 = y * y;
    double sum = y;
    double term = y;
    
    for (int k = 1; k < 100; k++) {
        term = term * y2 * (2*k-1) / (2*k+1);
        double sumAnterior = sum;
        sum += term;
        
        // Verificamos convergencia
        if (sumAnterior == sum) break;
    }
    
    return 2 * sum;
}

// Función para calcular e^x usando suma de Taylor
double exp(double x) {
    double sum = 1.0; // primer término es 1
    double term = 1.0;
    
    for (int i = 1; i < 100; i++) {
        term *= x / i;
        sum += term;
        
        // Verificamos convergencia
        if (term < 0.0000001) break;
    }
    
    return sum;
}

// Función para calcular potencias con exponentes decimales
double PowDecimal(double base, double exponente) {
    // Caso base
    if (exponente == 0)
        return 1;
    
    // Si el exponente es negativo
    if (exponente < 0) {
        return 1.0 / PowDecimal(base, -exponente);
    }
    
    // Si el exponente es entero, usamos método iterativo
    if (exponente == (int)exponente) {
        double resultado = 1;
        for (int i = 0; i < exponente; i++) {
            resultado *= base;
        }
        return resultado;
    }
    
    // Para exponentes decimales separamos la parte entera y decimal
    int parteEntera = (int)exponente;
    double parteDecimal = exponente - parteEntera;
    
    double resultadoParteEntera = 1;
    // Calculamos la parte entera de forma iterativa
    for (int i = 0; i < parteEntera; i++) {
        resultadoParteEntera *= base;
    }
    
    // Para la parte decimal utilizamos la aproximación numérica
    // a^0.n = e^(0.n * ln(a))
    double resultadoParteDecimal = exp(parteDecimal * ln(base));
    
    return resultadoParteEntera * resultadoParteDecimal;
}

auto main() -> int
{
    double base, exponente;
    
    cout << "Ingresa la base: ";
    cin >> base;
    
    cout << "Ingresa el exponente: ";
    cin >> exponente;
    
    double resultado = PowDecimal(base, exponente);
    
    cout << "El resultado de " << base << " elevado a " << exponente << " es: " << resultado << endl;
    
    // Ejemplo como mencionaste: a^2 + a^0.95
    cout << "\nEjemplo adicional:" << endl;
    cout << base << "^2 + " << base << "^0.95 = " 
         << PowDecimal(base, 2) + PowDecimal(base, 0.95) << endl;
    
    return 0;
}