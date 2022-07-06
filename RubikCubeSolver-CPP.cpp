#include <iostream>
#include <vector>
#include <fstream>
#include <queue>
#include <stack>

using namespace std;

class RubikCube
{
	char** side_f;
	char** side_b;
	char** side_u;
	char** side_d;
	char** side_l;
	char** side_r;
public:
	RubikCube()
	{	
		side_f = new char* [3];
		side_b = new char* [3];
		side_u = new char* [3];
		side_d = new char* [3];
		side_l = new char* [3];
		side_r = new char*[3];
	
		for (int i = 0; i < 3; i++)
		{
			side_f[i]=  new char[3];
			side_b[i] = new char[3];
			side_u[i] = new char[3];
			side_d[i] = new char[3];
			side_l[i] = new char[3];
			side_r[i] = new char[3];
    	}
	
	}
	RubikCube(const RubikCube&c)
	{
		side_f = new char* [3];
		side_b = new char* [3];
		side_u = new char* [3];
		side_d = new char* [3];
		side_l = new char* [3];
		side_r = new char* [3];

		for (int i = 0; i < 3; i++)
		{
			side_f[i] = new char[3];
			side_b[i] = new char[3];
			side_u[i] = new char[3];
			side_d[i] = new char[3];
			side_l[i] = new char[3];
			side_r[i] = new char[3];
		}
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				side_f[i][j] = c.side_f[i][j];
				side_b[i][j] = c.side_b[i][j];
				side_u[i][j] = c.side_u[i][j];
				side_d[i][j] = c.side_d[i][j];
				side_l[i][j] = c.side_l[i][j];
				side_r[i][j]= c.side_r[i][j];
			}
		}

	}
	static void ReadCube(RubikCube&c)
	{
		ifstream fin("Cube.txt");
		if (fin.is_open())
		{
			char Junk[100];
			fin.getline(Junk, 50);

			char w;
			for (int i = 0; i < 3; i++)
			{
				for (int j = 0; j < 3; j++) 
				{
					fin >> w;
					c.side_f[i][j]=w;
				}
			}
			char J; fin >> J;
			fin.getline(Junk, 50);

			for (int i = 0; i < 3; i++)
			{
				for (int j = 0; j < 3; j++)
				{
					fin >> w;
					c.side_b[i][j] = w;
				}
			}
			fin >> J;
			fin.getline(Junk, 50);

			for (int i = 0; i < 3; i++)
			{
				for (int j = 0; j < 3; j++)
				{
					fin >> w;
					c.side_l[i][j] = w;
				}
			}
			fin >> J;
			fin.getline(Junk, 50);

			for (int i = 0; i < 3; i++)
			{
				for (int j = 0; j < 3; j++)
				{
					fin >> w;
					c.side_r[i][j] = w;
				}
			}
			fin >> J;
			fin.getline(Junk, 50);

			for (int i = 0; i < 3; i++)
			{
				for (int j = 0; j < 3; j++)
				{
					fin >> w;
					c.side_u[i][j] = w;
				}
			}
			fin >> J;
			fin.getline(Junk, 50);

			for (int i = 0; i < 3; i++)
			{
				for (int j = 0; j < 3; j++)
				{
					fin >> w;
					c.side_d[i][j] = w;
				}
			}
		}

	}
	
	static bool CheckGoalState(const RubikCube& c)
	{
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				if (c.side_f[0][0] != c.side_f[i][j]) return false;
				if (c.side_b[0][0] != c.side_b[i][j]) return false;
				if (c.side_u[0][0] != c.side_u[i][j]) return false;
				if (c.side_d[0][0] != c.side_d[i][j]) return false;
				if (c.side_l[0][0] != c.side_l[i][j]) return false;
				if (c.side_r[0][0] != c.side_r[i][j]) return false;
			}
		}

		return true;
	}

	RubikCube* facec()
	{
		RubikCube *c= new RubikCube();
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0,k=2; j < 3&&k>=0;j++,k--) 
			{
				c->side_f[i][j] = side_f[k][i];
			}
		}

		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
//				c->side_f[i][j] = side_f[i][j];
				c->side_b[i][j] = side_b[i][j];
				c->side_u[i][j] = side_u[i][j];
				c->side_d[i][j] = side_d[i][j];
				c->side_l[i][j] = side_l[i][j];
				c->side_r[i][j] = side_r[i][j];
			}
		}
		for (int i = 0; i < 3; i++)
		{
			c->side_r[2][i] = side_u[2][i];
		}

		for (int i = 0; i < 3; i++)
		{
			c->side_d[2][i] = side_r[2][i];
		}
		for (int i = 0; i < 3; i++)
		{
			c->side_l[2][i] = side_d[2][i];
		}
		for (int i = 0; i < 3; i++)
		{
			c->side_u[2][i] = side_l[2][i];
		}

		return c;
	}


	RubikCube* backc()
	{
		RubikCube* c = new RubikCube();
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0, k = 2; j < 3 && k >= 0; j++, k--)
			{
				c->side_b[i][j] = side_b[k][i];
			}
		}

		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				c->side_f[i][j] = side_f[i][j];
				//c->side_b[i][j] = side_b[i][j];
				c->side_u[i][j] = side_u[i][j];
				c->side_d[i][j] = side_d[i][j];
				c->side_l[i][j] = side_l[i][j];
				c->side_r[i][j] = side_r[i][j];
			}
		}
		for (int i = 0; i < 3; i++)
		{
			c->side_l[0][i] = side_u[0][i];
		}

		for (int i = 0; i < 3; i++)
		{
			c->side_d[0][i] = side_l[0][i];
		}
		for (int i = 0; i < 3; i++)
		{
			c->side_r[0][i] = side_d[0][i];
		}
		for (int i = 0; i < 3; i++)
		{
			c->side_u[0][i] = side_r[0][i];
		}

		return c;
	}

	RubikCube* rightc()
	{
		RubikCube* c = new RubikCube();
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0, k = 2; j < 3 && k >= 0; j++, k--)
			{
				c->side_r[i][j] = side_r[k][i];
			}
		}

		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				c->side_f[i][j] = side_f[i][j];
				c->side_b[i][j] = side_b[i][j];
				c->side_u[i][j] = side_u[i][j];
				c->side_d[i][j] = side_d[i][j];
				c->side_l[i][j] = side_l[i][j];
				//c->side_r[i][j] = side_r[i][j];
			}
		}
		for (int i = 0; i < 3; i++)
		{
			c->side_u[i][2] = side_f[i][2];
		}
		
		for (int i = 0,j=2; i < 3&&j>=0; i++,j--)
		{
			c->side_b[i][0] = side_u[j][2];
		}
	
		for (int i = 0; i < 3; i++)
		{
			c->side_d[i][0] = side_b[i][0];
		}
		for (int i = 0, j = 2; i < 3 && j >= 0; i++, j--)
		{
			c->side_f[i][2] = side_d[j][0];//changed j
		}

		return c;
	}

	RubikCube* leftc()
	{
		RubikCube* c = new RubikCube();
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0, k = 2; j < 3 && k >= 0; j++, k--)
			{
				c->side_l[i][j] = side_l[k][i];
			}
		}

		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				c->side_f[i][j] = side_f[i][j];
				c->side_b[i][j] = side_b[i][j];
				c->side_u[i][j] = side_u[i][j];
				c->side_d[i][j] = side_d[i][j];
				//c->side_l[i][j] = side_l[i][j];
				c->side_r[i][j] = side_r[i][j];
			}
		}
		//
		for (int i = 0, j = 2; i < 3 && j >= 0; i++, j--)
		{
			c->side_u[i][0] = side_b[j] [2];
		}

		for (int i = 0; i < 3; i++)
		{
			c->side_b[i][2] = side_d[i][2];
		}
		//
		for (int i = 0, j = 2; i < 3 && j >= 0; i++, j--)
		{
			c->side_d[j][2] = side_f[i][0];
		}
		for (int i = 0, j = 2; i < 3 && j >= 0; i++, j--)
		{
			c->side_f[i][0] = side_u[i][0];//removed j from u
		}

		return c;
	}

	RubikCube* upc()
	{
		RubikCube* c = new RubikCube();
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0, k = 2; j < 3 && k >= 0; j++, k--)
			{
				c->side_u[i][j] = side_u[k][i];
			}
		}

		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				c->side_f[i][j] = side_f[i][j];
				c->side_b[i][j] = side_b[i][j];
				//c->side_u[i][j] = side_u[i][j];
				c->side_d[i][j] = side_d[i][j];
				c->side_l[i][j] = side_l[i][j];
				c->side_r[i][j] = side_r[i][j];
			}
		}
		for (int i = 0; i < 3; i++)
		{
			c->side_l[i][2] = side_f[0][i];
		}

		for (int i = 0; i < 3; i++)
		{
			c->side_b[0][i] = side_l[i][2];
		}
		for (int i = 0, j = 2; i < 3 && j >= 0; i++, j--)
		{
			c->side_r[j][0] = side_b[0][i];
		}
		
		for (int i = 0, j = 2; i < 3 && j >= 0; i++, j--)
		{
			c->side_f[0][i] = side_r[j][0];
		}

		return c;
	}

	RubikCube* downc()
	{
		RubikCube* c = new RubikCube();
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0, k = 2; j < 3 && k >= 0; j++, k--)
			{
				c->side_d[i][j] = side_d[k][i];
			}
		}

		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				c->side_f[i][j] = side_f[i][j];
				c->side_b[i][j] = side_b[i][j];
				c->side_u[i][j] = side_u[i][j];
				
				c->side_l[i][j] = side_l[i][j];
				c->side_r[i][j] = side_r[i][j];
			}
		}
		for (int i = 0; i < 3; i++)
		{
			c->side_l[i][0] = side_b[2][i];
		}

		for (int i = 0, j = 2; i < 3 && j >= 0; i++, j--)
		{
			c->side_b[2][i] = side_r[j][2];
		}
		for (int i = 0, j = 2; i < 3 && j >= 0; i++, j--)
		{
			c->side_r[j][2] = side_f[2][i];
		}

		for (int i = 0; i < 3; i++)
		{
			c->side_f[2][i] = side_l[i][0];
		}

		return c;
	}

	void Print()
	{
		cout << "---Face--- "<<endl;
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				cout << side_f[i][j]<<"  ";
			}
			cout << endl;
		}
		cout << "---Back--- " << endl;
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				cout << side_b[i][j] << "  ";
			}
			cout << endl;
		}
		cout << "---Left--- " << endl;
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				cout << side_l[i][j] << "  ";
			}
			cout << endl;
		}
		cout << "---Right--- " << endl;
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				cout << side_r[i][j] << "  ";
			}
			cout << endl;
		}
		cout << "---Top--- " << endl;
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				cout << side_u[i][j] << "  ";
			}
			cout << endl;
		}
		cout << "---Down--- " << endl;
		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				cout << side_d[i][j] << "  ";
			}
			cout << endl;
		}
	}

	~RubikCube()
	{
		for (int i = 0; i < 3; i++)
		{
			delete side_f[i];
			delete side_b[i];
			delete side_u[i];
			delete side_d[i];
			delete side_l[i];
			delete side_r[i];
		}
		delete side_f;
		delete side_b;
		delete side_u;
		delete side_d;
		delete side_l;
		delete side_r;
	}
};

//For the BFS Search
class Node
{
public:
	Node* Parent;
	char move;//That took to get to this Node for BackTracking
	RubikCube* cube;
	Node(RubikCube* c=0, char m='-', Node* P=0)
	{
		move = m;
		Parent = P;
		cube = c;
	}
	~Node()
	{
		delete cube;
	}
};

int main()
{
	RubikCube *c=new RubikCube();
	RubikCube::ReadCube(*c);

	cout << "First Scramlbe The Cube (Every Move here is Inverse Move ) ,Press S to stop Scrambling" << endl;
	while (1) 
	{
		RubikCube* r=0;
		char w='-';
		cout << "Enter the Move' :  ";
		cin >> w;
		if (w == 'U' || w == 'u')
		{
			for (int i = 0; i < 3; i++) {
				r = c->upc();
				delete c;
				c = r;
			}
		}
		else if (w == 'L' || w == 'l')
		{
			for (int i = 0; i < 3; i++) {
				r = c->leftc();
				delete c;
				c = r;

			}
		}
		else if (w == 'R' || w == 'r')
		{
			for (int i = 0; i < 3; i++) {

				r = c->rightc();
				delete c;
				c = r;
			}
		}
		else if (w == 'D' || w == 'd')
		{
			for (int i = 0; i < 3; i++) {

				r = c->downc();
				delete c;
				c = r;
			}
		}
		else if (w == 'F' || w == 'f')
		{
			for (int i = 0; i < 3; i++) {
				r = c->facec();
				delete c;
				c = r;
			}
		}
		else if (w == 'B' || w == 'b')
		{
			for (int i = 0; i < 3; i++) {
				r = c->backc();
				delete c;
				c = r;
			}
		}
		else if (w == 's'|| w == 'S')
		{
			break;
		}

		cout << " After " << w << " ' Move :" << endl;
		c->Print();
	}


	cout << "Scrambling Done , now we solve via BFS" << endl;
	queue<Node*> que;
	Node* node = new Node(c);
	que.push(node);
	vector<Node*> visited;
	Node* goal=0;
	while (que.empty() == false)
	{
		Node* n = que.front();
		que.pop();
		RubikCube* c = n->cube;
		if (RubikCube::CheckGoalState(*c) == true)
		{
			goal = n;
			break;
		}
		else
		{
			que.push(new Node(c->facec(),'F',n));
			que.push(new Node(c->backc(), 'B', n));
			que.push(new Node(c->leftc(), 'L', n));
			que.push(new Node(c->rightc(), 'R', n));
			que.push(new Node(c->upc(), 'U', n));
			que.push(new Node(c->downc(), 'D', n));
		}

	}
	stack<char> s;
	cout << "We have found the Solution" << endl;
	RubikCube* res = 0; 
	res = goal->cube;
	while (goal->move != '-'|| goal->Parent!=0)
	{
		s.push(goal->move);
		goal = goal->Parent;
	}
	while (!s.empty())
	{
		cout << " --> " << s.top() ;
		s.pop();
	}
	cout<<endl;
	cout << "The Goal State is As Such" << endl;
	res->Print();
}