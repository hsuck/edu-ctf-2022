#include <iostream>
#include <vector>

#define LEN(a) (sizeof(a)/sizeof(a[0]))

using namespace std;

int result[] = {1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1};

class LFSR{
	public:
		unsigned long long state, tap, size;
		LFSR( unsigned long long state, unsigned long long tap, unsigned long long size ):
			state{state}, tap{tap}, size{size} {}
		int getbit(){
			int f = __builtin_popcountll( state & tap ) & 1;
			int ret = state & 1;
			state >>= 1;
			state |= f << (size - 1);
			return ret;
		}
};

double cal_acc( int a[], int b[] ){
    int match = 0;
    for( int i = 0; i < 200; i++ ){
        if( a[i] == b[i] ){
            match++;
        }
    }

    return (double)match / 200;
}

vector<unsigned long long> get_state(unsigned long long tap, unsigned long long size){
	int output[432];
	vector<unsigned long long> v;
	for (unsigned long long state = 0; state < (1ll << size); state++){
		LFSR lfsr = LFSR(state, tap, size);
		for (int i = 0; i < 432; i++)
		    output[i] = lfsr.getbit();
         
        //cout << LEN( output ) << endl;
		double acc = cal_acc( &output[232], &result[ LEN( result ) - 200 ] );
        if( acc >= 0.7 ){
            cout << acc << endl;
            v.push_back( state );
        }
	}

    return v;
}

int main(){
	unsigned char flag[30] = {0};
	int output[432];
	unsigned long long origin_states[3], taps[3], sizes[3] = {27, 23, 25};
	vector<vector<unsigned long long>> states;
	taps[0] = (1 << 26) | (1 << 16) | (1 << 13) | 1;
	taps[1] = (1 << 22) | (1 << 7) | (1 << 5) | 1;
	taps[2] = (1 << 24) | (1 << 19) | (1 << 17) | 1;

	for (int i = 1; i < 3; i++){
		states.push_back( get_state( taps[i], sizes[i] ) );
	}
    
    for( unsigned long long state: states[0] ){
        cout << state << endl;
    }
    for( unsigned long long state: states[1] ){
        cout << state << endl;
    }

    for( unsigned long long state1: states[0] ){
        for( unsigned long long state2: states[1] ){
            for( unsigned long long state0 = 0; state0 < 1ll << sizes[0]; state0++ ){
                LFSR l0 = LFSR( state0, taps[0], sizes[0] );
                LFSR l1 = LFSR( state1, taps[1], sizes[1] );
                LFSR l2 = LFSR( state2, taps[2], sizes[2] );

                for( int i = 0; i < 432; i++ ){
                    int x0 = l0.getbit();
                    int x1 = l1.getbit();
                    int x2 = l2.getbit();

                    output[i] = x0 ? x1 : x2;
                }

                double acc = cal_acc( &output[232], &result[ LEN( result ) - 200 ] );
                if( acc >= 1.0 ){
                    LFSR _l0 = LFSR( state0, taps[0], sizes[0] );
                    LFSR _l1 = LFSR( state1, taps[1], sizes[1] );
                    LFSR _l2 = LFSR( state2, taps[2], sizes[2] );
                    for( int i = 0; i < 29; i++ ){
                        for( int j = 0; j < 8; j++ ){
                            int _x0 = _l0.getbit();
                            int _x1 = _l1.getbit();
                            int _x2 = _l2.getbit();
                            int res = _x0 ? _x1 : _x2;

                            flag[i] |= ( result[ i * 8 + j ] ^ res ) << ( 7 - j );
                        }
                    }

                    cout << flag << endl;
                }
            }
        }
    }
}
