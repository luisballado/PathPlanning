#include <iostream>
#include <queue>
#include <vector>
#include <unistd.h>
#include <string>

//Programa BFS con uso directo de la representacion de la matriz

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
  usleep(8000);
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

void bfs(std::pair<int,int>& inicio, std::pair<int,int>& fin,int rows,int cols, std::vector<std::vector<char>> &grid){
  
  //indices de la celda en la matriz
  std::queue<std::pair<int,int>> q;
  q.push(inicio);

  //no se maneja una lista de visitados,
  //se marca con el valor que le cuesta llegar a ese nodo
  grid[inicio.first][inicio.second] = '1';
    
  while(!q.empty()){
    
    //tomamos el primer elemento de la cola
    std::pair<int,int> node = q.front();

    //conocer los elementos que componen el nodo
    int x = node.first;
    int y = node.second;

    //quitar el nodo de la cola
    q.pop();

    //obtener vecinos a partir de x,y dados
    std::vector<std::pair<int, int>> neighbors = get_neighbors(x, y, rows, cols);
    
    // imprimir los vecinos
    for (const auto& pair : neighbors) {

      //std::cout << "(" << pair.first << ", " << pair.second << ")";
      //std::cout << " -> " << grid[pair.first][pair.second] << std::endl;

      //si no esta visitado
      if(grid[pair.first][pair.second] == '0'){
	//marcar como visitado, respecto al pasado sumarle uno
	grid[pair.first][pair.second] = int((grid[x][y]) + 1);
	//agregar a la cola
	q.push(pair);
      }
    }
    
    //imprimir avance en cada paso
    print_dist(grid,false);
    
  }
}


int main(){
  
  int rows;
  int cols;

  int inicio_x,inicio_y;
  int fin_x,fin_y;
  
  std::pair<int,int> inicio;
  std::pair<int,int> fin;
    
  std::cin >> rows >> cols;

  //Hacer la matriz del mapa
  std::vector<std::vector<char>> grid(rows, std::vector<char>(cols));
  int num;
    
  //construir la matriz
  for(int i=0;i<rows;i++){
    std::string line;
    std::cin >> line;
    
    for(int j=0; j<cols;j++){
      grid[i][j] = line[j];
    }
  }

  //imprimir matriz cargada
  /**
  for(int i=0;i<grid.size();i++){
    for(int j = 0; j<grid[i].size();j++){
      std::cout << grid[i][j];
    }
    std::cout<<std::endl;
  }
  **/

  //guardar las coordenadas de inicio
  std::cin >> inicio_x >> inicio_y;
  inicio = std::make_pair(inicio_x,inicio_y);
  
  //guardar las coordenadas de fin
  std::cin >> fin_x >> fin_y;
  fin    = std::make_pair(fin_x,fin_y);

  //impresion para ver visualizar los datos
  //std::cout << inicio.first << "," << inicio.second << std::endl;
  //std::cout << fin.first << "," << fin.second << std::endl;
  
  bfs(inicio,fin,rows,cols,grid);

  //buscar el camino mas corto
  //revisar con los vecinos
  if(grid[fin_x][fin_y]-'0' == 0 ){
    std::cout << "no solucion" << std::endl;
  }else{
    std::cout << "(" << fin_x <<  ", " << fin_y << ") -> ";
    std::cout << grid[fin_x][fin_y]-'0' << std::endl;
    
    //buscar el camino con los vecinos
    std::vector<std::pair<int, int>> neighbors;

    //manejar un queue
    std::queue<std::pair<int,int>> q_grad;
    std::queue<std::pair<int,int>> _q_;
    
    q_grad.push(std::make_pair(fin_x,fin_y));
    _q_.push(std::make_pair(fin_x,fin_y));

    int _max_ = 10000;
    std::pair<int,int> max_pair;
    max_pair = std::make_pair(fin_x,fin_y);
    
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
    
  }
}
