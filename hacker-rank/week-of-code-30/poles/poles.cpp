#include <bits/stdc++.h>

using namespace std;

long long solve(vector<pair<long long, long long>> &poles,vector<vector<long long>>& dp, int i, int k){
    if(dp[i][k]!=-1)
        return dp[i][k];
    long long cost = 0;
    if (k==1){
        for(int x=i+1; x<poles.size(); x++){
            cost+=poles[x].second*(poles[x].first-poles[i].first);
        }
    } else {
        long long cur = 0;
        long long best=numeric_limits<long long>::max();
        for(int x= i; x< poles.size()-k+1; x++){
            cur+=poles[x].second*(poles[x].first-poles[i].first);
            best=min(best,cur+solve(poles,dp,x+1, k-1));
        }
        cost=best;
    }
    dp[i][k] = cost;
    return cost;
}

int main(){
    int n;
    int k;
    cin >> n >> k;
    vector<pair<long long, long long>> poles(n);
    for(int a0 = 0; a0 < n; a0++){
        cin >> poles[a0].first >> poles[a0].second;
    }
    vector<vector<long long>>dp(n,vector<long long>(k+1,-1));
    cout<<solve(poles,dp,0,k)<<endl;
    return 0;
}