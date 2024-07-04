#include <iostream>
#include <string>
#include <cmath>
#include <queue>
#include <bits/stdc++.h>

class Nodo {
  
public:
  
  std::pair<int,int> coordenadas;
  int costo;
  
  //calculo de la distancia
  double h(std::pair<int,int>& destino){
    return std::sqrt(std::pow((destino.first - coordenadas.first), 2) + std::pow((destino.second - coordenadas.second), 2));
  }
  
  double f(std::pair<int,int>& destino){
    return costo+h(destino);
  }

  int age;
  std::string name;
  node(int a, std::string b){
    age = a;
    name = b;
  }
  
  int a_star(std::pair<int,int>& destino){
    
    //parte de lo que tenga coordenadas
    double cost_fn = f(destino);
    
    //-------------------------------
    // Buscar solucion
    //-------------------------------
    std::priority_queue<std::pair<int,int>> lista_abierta;
    
    int arr[6] = { 10, 2, 4, 8, 6, 9 };
    
    // defining priority queue
    std::priority_queue<int> pq;
    
    // printing array
    std::cout << "Array: ";

    for (auto i : arr) {
      std::cout << i << ' ';
    }

    std::cout << std::endl;

    // pushing array sequentially one by one
    for (int i = 0; i < 6; i++) {
        pq.push(arr[i]);
    }
 
    // printing priority queue
    std::cout << "Priority Queue: ";

    while (!pq.empty()) {
      std::cout << pq.top() << ' ';
        pq.pop();
    }
 
    //-------------------------------
      
    //no encontre solucion
    return 1;
    
  }
};

int main() {
  
  Nodo myNode;  // Create an object of MyClass
  
  //las coordenadas donde estoy comenzando
  myNode.coordenadas = std::make_pair(1,1);
  
  //el costo hasta ahora
  //se inicializa en 0 cuando sea el inicio del programa
  myNode.costo = 0;
  myNode.node;

  std::cout << myNode.node.age << std::endl;
    
  //coordenadas del destino
  std::pair<int,int> destino = std::make_pair(10,10);

  //calculo de la heuristica
  double h = myNode.h(destino);

  //calculo de la funcion de costo
  double f = myNode.f(destino);
  
  // Print attribute values
  std::cout << "Inicio: " << "x: " << myNode.coordenadas.first << ", y: " << myNode.coordenadas.second << std::endl;
  std::cout << "Final: "  << "x: " << destino.first << ", y: " << destino.second << std::endl;
  std::cout << "Costo inicio" << myNode.costo << std::endl;
  std::cout << "h: " << h << std::endl;
  std::cout << "f: " << f << std::endl;

  myNode.a_star(destino);
  
  return 0;

}
