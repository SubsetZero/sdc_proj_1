#include <stdlib.h>

#define AMOUNT_OF_TEST 1

int kernel_2(int a, int b, int c, int n) {
	a = b * a * 100;
	if ( a < n ) {
		a = a / (n * c);
	}
	else {
		a = b % (a * c);
	}
	c = a ^ (c * b);
	return c;
}


int main(void){
	int a, b, c;
	a = rand()%10;
	b = rand()%10;
	c = rand()%10;

	int i = 0;
	i = rand()%10;
	kernel_2(a, b, c, i);
}

