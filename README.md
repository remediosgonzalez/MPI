# MPI

Paralelización de búsqueda de números primos con MPI en Python mediante la división de búsqueda en diferentes procesadores.
Se muestra la búsqueda para diferentes bucles:

- Paralelización del bucle externo para dividir en rangos la búsqueda (MPI_numPrimes.py).
- Paralelización del bucle interno para dividiendo los rangos en subrangos de búsqueda en cada procesador (MPI_numPrimes.py).

Para ejecutarlo simplemente hay que lanzar el comando, donde n es el número de procesadores queremos usar:

mpirun -np n python MPI_numPrimes.py
