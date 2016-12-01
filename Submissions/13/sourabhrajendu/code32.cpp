#include <bits/stdc++.h>

using namespace std;

struct edge
{
    int s,d;
    int w;
}a[100000001];
vector<edge>mst;
bool acom(edge lhs,edge rhs)
{
    return lhs.w<rhs.w;
}

int par[10001];

int root(int i)
{
    if(par[i]==i)
        return i;
    return par[i]=root(par[i]);
}

long long int kruskal(int j,int n)
{
    int i,k=0;
    long long int ans=0;
    for(i=0;i<j&&k<n-1;i++){
        if(root(a[i].s)!=root(a[i].d)){
            k++;
            ans+=1ll*a[i].w;
            par[par[a[i].s]]=root(a[i].d);
            edge temp;
            temp.s=a[i].s;
            temp.d=a[i].d;
            temp.w=a[i].w;
            mst.push_back(temp);
        }
    }
    return ans;
}


int main()
{
    int t,n,i,j,e;
    long long int ans;
    cin>>t;
    while(t--){
        cin>>n;j=0;
        for(i=1;i<=n;i++){
            par[i]=i;    
        }
        cin>>e;
        while(e--){
            cin>>a[j].s>>a[j].d>>a[j].w;
            j++;
        }
        sort(a,a+j,acom);
        ans=kruskal(j,n);
        cout<<ans<<endl;
        for(i=0;i<mst.size();i++)
        	cout<<mst[i].s<<" "<<mst[i].d<<" "<<mst[i].w<<endl;
    }
}
