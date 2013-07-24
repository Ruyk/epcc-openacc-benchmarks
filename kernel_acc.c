#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
 

int main() {

    double t1, t2;

    // Host input vectors 
    double *h_a;
    double *h_b;
    double *h_c;
    int n = 100000;
    int i = 0;
    // Size, in bytes, of each vector
    long bytes = n*sizeof(double);
 


    // Allocate memory for each vector on host
    h_a = (double*)malloc(bytes);
    h_b = (double*)malloc(bytes);
    h_c = (double*)malloc(bytes);
 

    // Initialize vectors on host
    for( i = 0; i < n; i++ ) {
        h_a[i] = sin(i)*sin(i);
        h_b[i] = cos(i)*cos(i);
    }

    t1 = omp_get_wtime();

    #pragma acc kernels loop copyin(h_a[0:n],h_b[0:n]) copyout(h_c[0:n])
    for( i = 0; i < n; i++) {
	h_c[i] = h_a[i] + h_b[i];
    }

    t2 = omp_get_wtime();

    double sum = 0;
    for(i=0; i<n; i++)
        sum += h_c[i];
    printf("final result: %f\n", sum/n);
 
    printf("Time : %g\n", t2-t1);

	return 0;
}
