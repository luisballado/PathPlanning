#include <iostream>
#include <queue>
#include <vector>
#include <map>
#include <unistd.h>

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

void bfs(){

  int inicio_xy = (1,2);
  int fin_xy = (1,2);

  std::queue<std::pair<int,int>> q;
  q.push(inicio_xy);

  
  
  while(!q.empty()){
    std::pair<int,int> node = q.front();
    q.pop();

    for(int neighbor : neighbors){
      if (){
	q.push();
      }

      if(print){
	print_dist(rows,cols,distance_bfs);
      }
      
    }
    
  }
  
}

int main(){

  //bool PRINT = false;
  
  int rows;
  int cols;
  
  //int robot_inicio;
  //int robot_fin;
  
  std::cin >> rows >> cols;

  std::cout << "Filas:    " << rows << std::endl;
  std::cout << "Columnas: " << cols << std::endl;

  //Hacer la matriz del mapa
  std::vector<std::vector<char>> grid(rows, std::vector<char>(cols));

  for(int i=0;i<rows;i++){
    std::string line;
    std::cin >> line;

    for(int j=0; j<cols;j++){
      grid[i][j] = line[j];
      //std::cout << line[j] << std::endl;
    }  
  }
  
  //obtener posiciones
  std::vector<std::pair<int, int>> neighbors = get_neighbors(1, 2, 10, 10);

  // Print the vector of pairs
  for (const auto& pair : neighbors) {
    std::cout << "(" << pair.first << ", " << pair.second << ")" << std::endl;
    std::cout << grid[pair.first][pair.second] << std::endl;
  }
  
}
