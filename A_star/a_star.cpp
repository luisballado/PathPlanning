#include <iostream>
#include <string>
#include <cmath>
#include <queue>
#include <unistd.h>

// Definicion de la clase Nodo
class Nodo {

private:
  std::pair<int,int> inicio;
  int costo;
  std::pair<int,int> destino;
  
public:

  Nodo(const std::pair<int,int>& inicio, const std::pair<int,int> destino, int costo) : inicio(inicio), destino(destino), costo(costo) {}
  
  // obtener el costo
  int getCosto() const {
    return costo;
  }
  
  std::pair<int,int> getInicio() const{
    return inicio;
  }
  
  //calculo de la distancia
  double h() const{
    //manhatan
    return fabs(destino.first-inicio.first)+fabs(destino.second-inicio.second);
    
    //return 0;
    //euclideano;
    //return std::sqrt(std::pow((destino.first - inicio.first), 2) + std::pow((destino.second - inicio.second), 2));
  }
  
  double f() const{
    return costo+h();
  }

  // Sobrecarga del operador < para que la priority_queue ordene por costo menor
  bool operator<(const Nodo& nodo) const {
    return f() > nodo.f();
  }  
};

//cuatro conectividad
std::vector<std::pair<int, int>> get_neighbors(int i, int j, int rows, int cols){
  
  std::vector<std::pair<int,int>> neighbors;
  
  if (i > 0) neighbors.push_back(std::make_pair(i-1, j));
  if (i < rows-1) neighbors.push_back(std::make_pair(i+1, j));
  if (j > 0) neighbors.push_back(std::make_pair(i, j-1));
  if (j < cols-1) neighbors.push_back(std::make_pair(i, j+1));
  
  return neighbors;
  
}

//IMPRIMIR el arreglo para ver la animacion
void print_dist(std::vector<std::vector<char>> grid, bool ruta){
  
  usleep(50000);
  system("clear");
  
  int val;
  
  //imprimir y salir
  for(int i=0;i<grid.size();i++){
    for(int j = 0; j<grid[i].size();j++){
      val = grid[i][j] - '0';
      if (val == -13){
	std::cout << "  # ";
      }else{

	if(ruta){
	  if(std::to_string(val).length()==1){
	    if(val == 0){
	      std::cout << "  " << "*" << " ";
	    }else{
	      std::cout << "  " << val << " ";
	    }
	  }else{
	    if(val == 0){
	      std::cout << "  " << "*" << " ";
	    }else{
	      std::cout << " " << val << " ";
	    }
	  }
	}else{
	  if(std::to_string(val).length()==1){
	    std::cout << "  " << val << " ";
	  }else{
	    std::cout << " " << val << " ";
	  }
	}
      }
    }
    
    std::cout<<std::endl;
  }
}


int main() {

  int rows;
  int cols;
  int inicio_x,inicio_y;
  int fin_x,fin_y;

  std::cin >> rows >> cols;

  //Hacer la matriz del mapa
  std::vector<std::vector<char>> grid(rows, std::vector<char>(cols));

  //------------------------------------------------------------
  //construir la matriz
  //------------------------------------------------------------
  for(int i=0;i<rows;i++){
    std::string line;
    std::cin >> line;
    
    for(int j=0; j<cols;j++){
      grid[i][j] = line[j];
    }
  }
  for(int i=0;i<grid.size();i++){
    for(int j = 0; j<grid[i].size();j++){
      std::cout << grid[i][j];
    }
    std::cout<<std::endl;
  }
  
  std::cin >> inicio_x >> inicio_y;
  std::cin >> fin_x >> fin_y;

  std::pair<int, int> inicio = std::make_pair(inicio_x,inicio_y);
  std::pair<int, int> destino = std::make_pair(fin_x,fin_y);
  
  inicio = std::make_pair(inicio_x,inicio_y);
  destino    = std::make_pair(fin_x,fin_y);
  //------------------------------------------------------------
  
  std::priority_queue<Nodo> abiertos;
  std::queue<Nodo> cerrados;

  int costo = 0; //primer nodo
  
  Nodo nodo_inicio(inicio,destino,costo);
  
  abiertos.push(nodo_inicio);

  grid[inicio.first][inicio.second] = '1';
  
  // Extraer las personas en orden de prioridad
  while (!abiertos.empty()) {

    Nodo nodo_analizar = abiertos.top();

    //la lista abiertos asegura obtener el valor mas bajo
    //quitar de la lista de abiertos
    abiertos.pop();
    
    //agregar a cerrados
    cerrados.push(nodo_analizar);

    //si es el objetivo, parar
    if(nodo_analizar.getInicio() == destino){
      std::cout << "Es el destino" << std::endl;

      exit(1);
      
      std::vector<std::pair<int, int>> neighbors;
      
      //manejar un queue
      std::queue<std::pair<int,int>> q_grad;
      std::queue<std::pair<int,int>> _q_;
      
      q_grad.push(destino);
      _q_.push(destino);
      
      int _max_ = 10000;
      std::pair<int,int> max_pair;
      max_pair = destino;
      
      while(!q_grad.empty()){
	
	q_grad.pop();
	
	// imprimir los vecinos
	neighbors = get_neighbors(max_pair.first, max_pair.second, rows, cols);
	
	for (const auto& pair : neighbors) {
	  if(_max_ > grid[pair.first][pair.second] - '0' && grid[pair.first][pair.second] - '0' > -13){
	    _max_ = grid[pair.first][pair.second] - '0';
	    
	    max_pair = pair;
	  }	
	}
	
	//std::cout << "(" << max_pair.first << ", " << max_pair.second << ")";
	//std::cout << " -> " << grid[max_pair.first][max_pair.second]-'0' << std::endl;
	
	if (grid[max_pair.first][max_pair.second]-'0' == 1){
	  _q_.push(max_pair);
	  continue;
	  //print_dist(grid);
	  //exit(0);
	}else{
	  q_grad.push(max_pair); //puede ser un aux
	  _q_.push(max_pair); 
	}  
      }
      
      std::pair<int,int> ask;
      while(!_q_.empty()){
	ask = _q_.front();
	grid[ask.first][ask.second] = '0';
	print_dist(grid,true);
	_q_.pop();
      }
      
      return 1;
    }
    
    //obtener vecinos
    int x = nodo_analizar.getInicio().first;
    int y = nodo_analizar.getInicio().second;

    std::vector<std::pair<int, int>> neighbors = get_neighbors(x, y, rows, cols);
    
    // imprimir los vecinos
    for (const auto& pair : neighbors) {

      if(grid[pair.first][pair.second] == '0'){
	//std::cout << "(" << pair.first << ", " << pair.second << ")";
	//std::cout << " -> " << grid[pair.first][pair.second] << std::endl;
	int costo = 1;
	Nodo nodo_vecino(pair,destino,costo);
	
	grid[pair.first][pair.second] = static_cast<char>(int(grid[x][y]) + 1);
	abiertos.push(nodo_vecino);
      }
      
    }

    print_dist(grid,false);
    
  }

  std::cout << "NO SOLUCION" << std::endl;
    
  return -1;
}
