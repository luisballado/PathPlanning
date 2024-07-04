#include <iostream>
#include <string>
#include <cmath>

class Nodo {
  
public:
  
  std::pair<int,int> coordenadas;
  int costo;
  
  //calculo de la distancia
  double h(std::pair<int,int>& destino){
    return std::sqrt(std::pow((destino.first - coordenadas.first), 2) + std::pow((destino.second - coordenadas.second), 2));
  }
  
  double f(std::pair<int,int>& destino){
    return costo+heuristica(destino);
  }
  
  void a_star(std::pair<int,int>& destino){

    //parte de lo que tenga coordenadas
    double cost_fn = f(destino);

    
    
  }
  
};



int main() {
  
  Nodo myNode;  // Create an object of MyClass
  
  // Access attributes and set values
  myNode.coordenadas = std::make_pair(1,1);
  myNode.costo = 3;

  std::pair<int,int> destino = std::make_pair(10,10);
  
  double h = myNode.h(destino);
  double f = myNode.f(destino);
  
  // Print attribute values
  std::cout << myNode.costo << std::endl;
  std::cout << h << std::endl;
    
  return 0;

}
