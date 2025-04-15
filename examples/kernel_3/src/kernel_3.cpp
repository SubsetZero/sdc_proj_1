#include <stdlib.h>

int kernel_3 (int a[], int b[], int c[], int d[]) {
	int acc = 0;
	int tmp = 0;
	for (int i = 0; i < 100; ++i) {
		tmp = a[i] * b[i] - c[i];
		acc += tmp + d[i];
	}
	return acc;
}

int main(void){
	int a[100], b[100], c[100], d[100];
	for (int i = 0; i < 100; ++i) {
		a[i] = rand() % 10;
		b[i] = rand() % 10;
		c[i] = rand() % 10;
		d[i] = rand() % 10;
	}
	kernel_3 (a, b, c, d);
}

