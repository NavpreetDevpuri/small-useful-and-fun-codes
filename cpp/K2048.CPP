#include<iostream.h>
#include<conio.h>
#include<iomanip.h>
#include<string.h>
#include<process.h>
#include<stdlib.h>
#include<math.h>

int r[]={ 2,2,2,2,2,2,2,2,2,2,
	2,2,2,2,2,2,2,2,2,2,
	2,2,2,2,2,2,2,2,2,2,
	2,2,2,2,2,2,2,2,2,2,
	2,2,2,2,2,2,2,2,2,2,2,2,4,4,4 };

class kaplu {
    public: int i, j, k, m[16], mm[16];
    char c;
    kaplu() {
        for (i = 0; i < 16; ++i) {
            m[i] = 0;
        }
    }
    void rndom() {
        k = 0;
        for (i = 0; i < 16; ++i) {
            if (m[i] == 0) {
                mm[k] = i;
                ++k;
            }
        }
        m[mm[random(k)]] = r[random(45)];
    }
    void display() {
        int a = 4;
        cout << "\n";
        while (--a) {
            for (i = 0; i < 34; ++i) {
                cout << " ";
            }
            if (a == 2) {
                c = 219;
                cout << c << "2048  GAME" << c << endl;
            } else if (a == 1) {
                c = 223;
                for (i = 0; i < 12; ++i) {
                    cout << c;
                }
                cout << endl;
            } else {
                c = 220;
                for (i = 0; i < 12; ++i) {
                    cout << c;
                }
                cout << endl;
            }
        }
        cout << "\n\n";
        k = 0;
        int u = 15;
        for (i = 0; i < 4; ++i) {
            cout << setw(6);
            for (j = 0; j < 4; ++j) {
                if (m[k]) {
					//u = log(m[k]) / log(2) + 1;
                    // textcolor(u);
					//cout << u << "@";
                    cout << m[k] << setw(12);
                } else {
                    cout << " _ " << setw(12);
                }
                ++k;
            }
            cout << "\n\n\n\n";
        }
    }
    void cotrol() {
        char c = getch();
        if (c == 72 || c == 119) {
            logic(4, 4, 1);
            rndom();
        } else if (c == 97 || c == 75) {
            logic(1, 1, 4);
            rndom();
        } else if (c == 80 || c == 115) {
            logic(11, -4, -1);
            rndom();
        } else if (c == 77 || c == 100) {
            logic(14, -1, -4);
            rndom();
        } else if (c == 'p') {
            exit(1);
            exit(1);
        }
    }
    void logic(int a, int b, int c) {
        int e, ee, t, tt[16] = {
            0
        };
        while (t) {
            t = 0;
            e = 3;
            for (i = a; e > 0; i += b) {
                ee = 4;
                for (j = i; ee > 0; j += c) {
                    if (m[j] != 0) {
                        if (m[j - b] == 0) {
                            if (m[j] == 3) {
                                tt[j - b] = tt[j];
                                tt[j] = 0;
                            } else {
                                m[j - b] = m[j];
                                m[j] = 0;
                            }
                            ++t;
                        } else if (m[j - b] == m[j] && m[j] != 3) {
                            tt[j - b] = 2 * m[j];
                            m[j - b] = 3;
                            m[j] = 0;
                            ++t;
                        }
                    }
                    --ee;
                }
                --e;
            }
            for (i = 0; i < 16; ++i) {
                if (tt[i] != 0) {
                    m[i] = tt[i];
                }
            }
        }
    }
};

void main() {
    clrscr();
    randomize();
    kaplu k;
    k.rndom();
    while (1) {
        k.display();
        k.cotrol();
        clrscr();
    }
    getch();
}