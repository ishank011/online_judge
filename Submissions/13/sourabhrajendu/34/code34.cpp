#include <bits/stdc++.h>
#include <cstdio>
#include <vector>
#define lld long long int
#define pi pair<int,int>
#define plpi pair<lld,pi>
#define pb push_back
#define mp make_pair
#define vi vector<int>
#define vl vector <lld>

using namespace std;

struct compare
{
	bool operator()(pair <lld , pair<int, int> > a, pair <lld , pair<int, int> > b){
		return a.first>b.first;
	}
};

int visited[1000000],noOfVisited;
lld ans=0;
vector<int>start,ending;
vector<lld>weights;
void WeightOfMST(vector<int> a[], vector<lld> wt[],int n)
{
	pair <int,int> p1;
	pair <lld, pair<int,int> > p2;
	priority_queue <pair <lld , pair<int,int> > , vector <pair <lld , pair<int,int> > > , compare> pq;
	int i=1,j;
	while(noOfVisited<n){
		for(j=0;j<a[i].size();j++){
			if(visited[a[i][j]]==0){
				p1= make_pair(i,a[i][j]);
				p2=make_pair(wt[i][j],p1);
				pq.push(p2);
			}
		}
		p2 = pq.top();
		pq.pop();
		while(visited[p2.second.second]!=0 ){
			p2 = pq.top();
			pq.pop();
		}
		weights.push_back(p2.first);
		start.push_back(p2.second.first);
		ending.push_back(p2.second.second);
		visited[p2.second.second]=1;
		noOfVisited++;
		ans+=p2.first;
		i=p2.second.second;
	}

}

int main()
{
	int n,e,i,j,x,y;
	lld w;
	cin>>n>>e;
	vector <int> adjlist[n+1];
	vector <lld> weight[n+1];
	visited[1]=1;
	noOfVisited=1;
	while(e--){
		cin>>x>>y>>w;
		adjlist[x].push_back(y);
		adjlist[y].push_back(x);
		weight[x].push_back(w);
		weight[y].push_back(w);
	}
	WeightOfMST(adjlist,weight,n);
	cout<<ans<<endl;
	//cout<<start.size();
	for(i=0;i<start.size();i++)
		cout<<start[i]<<" "<<ending[i]<<" "<<weights[i]<<endl;
	return 0;
}