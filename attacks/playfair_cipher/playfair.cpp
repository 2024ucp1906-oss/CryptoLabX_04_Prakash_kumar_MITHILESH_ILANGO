#include<bits/stdc++.h>
#include<fstream>
using namespace std;

string prepare_plaintext(string pltext) {
    string s = "";

    for (char c : pltext) {
        if (isalpha(c)) {
            s += toupper(c);
        }
    }

    string ans = "";

    for (int i = 0; i < s.size(); ) {
        char a = s[i];

        if (i + 1 >= s.size()) {
            ans += a;
            ans += 'X';
            i++;
        }
        else if (s[i] == s[i + 1]) {
            ans += a;
            ans += 'X';
            i++;
        }
        else {
            ans += a;
            ans += s[i + 1];
            i += 2;
        }
    }

    return ans;
}


int main(){
    string plaintext;
    ifstream plain("plaintex.txt");
    string line;

    while(getline(plain,line)){
        plaintext+=line;
    }

    plaintext = prepare_plaintext(plaintext);
    cout<<plaintext;

    return 0;
}