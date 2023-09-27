#include <iostream>
#include <queue>
#include <vector>
#include <map>
#include <unistd.h>
#include <string>

//Programa BFS con uso directo de la representacion de la matriz

std::vector<std::pair<int, int>> get_neighbors(int i, int j, int rows, int cols){
  
  std::vector<std::pair<int,int>> neighbors;
  
  if (i > 0) neighbors.push_back(std::make_pair(i-1, j));
  if (i < rows-1) neighbors.push_back(std::make_pair(i+1, j));
  if (j > 0) neighbors.push_back(std::make_pair(i, j-1));
  if (j < cols-1) neighbors.push_back(std::make_pair(i, j+1));
  
  return neighbors;
  
}

//IMPRIMIR el arreglo para ver la animacion
void print_dist(int rows, int cols, std::vector<int>& distance){
  usleep(1000);
  system("clear");
  for (int i = 0; i < rows; i++){
    for (int j = 0; j < cols; j++){
      int u = i*cols + j;
      if (distance[u] == -1){
	std::cout << "  # ";
      } else {
	//poner distancias fancy
	if(std::to_string(distance[u]).length() == 1){
	  std::cout << " " << distance[u] << " ";
	}else {
	  std::cout << " " << distance[u] << " ";
	}
      }
    }
    std::cout << std::endl;
  }
}

void bfs(std::pair<int,int>& inicio, std::pair<int,int>& fin,int rows,int cols, std::vector<std::vector<char>> grid){
  
  //indices de la celda en la matriz
  std::queue<std::pair<int,int>> q;
  q.push(inicio);

  bool primera = true;
  
  while(!q.empty()){

    std::pair<int,int> node = q.front();

    int x = node.first;
    int y = node.second;

    std::cout << "-NODO-VALUE-" << std::endl;
    std::cout <<   grid[x][y]   << " " << std::endl;
    std::cout << "------------" << std::endl;
    
    q.pop();

    //obtener posiciones
    //obtener vecinos a partir de x,y dados
    std::vector<std::pair<int, int>> neighbors = get_neighbors(x, y, rows, cols);
    
    // imprimir los vecinos
    for (const auto& pair : neighbors) {
      std::cout << "(" << pair.first << ", " << pair.second << ")";
      std::cout << " -> " << grid[pair.first][pair.second] << std::endl;
      
      //si el valor no es una pared # hacer
      if(grid[pair.first][pair.second] == '#'){
	
	//imprimir y salir
	for(int i=0;i<grid.size();i++){
	  for(int j = 0; j<grid[i].size();j++){
	    std::cout << grid[i][j];
	  }
	  std::cout<<std::endl;
	}
	
	exit(1);
	
      }else{
	if(grid[pair.first][pair.second] == '0'){
	  //respecto al pasado sumarle uno
	  grid[pair.first][pair.second] = int(grid[x][y] + 1);
	  q.push(pair);
	}
      }
      primera = false;
    }
    
  }
}


int main(){
  
  //bool PRINT = false;

  int rows;
  int cols;
  int inicio_x,inicio_y;
  int fin_x,fin_y;
  
  std::pair<int,int> inicio;
  std::pair<int,int> fin;
    
  std::cin >> rows >> cols;

  //Hacer la matriz del mapa
  std::vector<std::vector<char>> grid(rows, std::vector<char>(cols));

  //construir la matriz
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
  
  //print_dist(rows,cols);

  std::cin >> inicio_x >> inicio_y;
  std::cin >> fin_x >> fin_y;
  
  inicio = std::make_pair(inicio_x,inicio_y);
  fin    = std::make_pair(fin_x,fin_y);
  
  std::cout << inicio.first << "," << inicio.second << std::endl;
  std::cout << fin.first << "," << fin.second << std::endl;
  
  bfs(inicio,fin,rows,cols,grid);

}
