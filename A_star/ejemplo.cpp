#include <iostream>
#include <string>

class Nodo {
  
public:   
  std::pair<int,int> nodo;
  std::string myString;
  
  //calculo de la distancia
  double heuristica(std::pair<int,int>& destino){
    return std::sqrt(std::pow((destino.first - nodo.first), 2) + std::pow((destino.second - nodo.second), 2));
  }
};

int main() {
  
  Nodo myNode;  // Create an object of MyClass
  
  // Access attributes and set values
  myNode.nodo = std::make_pair(1,2);
  
  // Print attribute values
  std::cout << myNode.nodo.first << std::endl;
  std::cout << myNode.nodo.second << std::endl;
    
  return 0;
}
