#include <stdlib.h>

#define AMOUNT_OF_TEST 1

int kernel_4(int a, int b, int c, int n) {
	for (int i = 0; i < 100; i ++ ) {
		a = (b + 50) * (100 + n) * (40 + c) * (10 + a);
		a = a / (n + c);
		a = b % (a + c);
		c += (a * n) ^ ((c + b) * b) ;
	}
	return c;
}


int main(void){
	int a, b, c;
	a = rand()%10;
	b = rand()%10;
	c = rand()%10;

	int i = 0;
	i = rand()%10;
	kernel_4(a, b, c, i);
}

