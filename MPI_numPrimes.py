#!/usr/bin/env python
# coding: utf-8

#jupyter nbconvert --to python  Untitled2.ipynb 

import numpy as np;
import time;
import sys;
import math;
import os;
from mpi4py import MPI;

comm = MPI.COMM_WORLD;
#Procesador en ejecución
rank = comm.Get_rank();
#Procesadores activos
size = comm.Get_size();

start_time = time.time();
#Elementos primos hasta num
num = 10**2;

primos=[]
wtime = MPI.Wtime();
print(wtime)

def es_primo(num,fin,array_primos):
    #Solo comprobamos impares hasta la raiz de num
    i=2;
    while (i < math.sqrt(fin)+1):
        if num%i == 0:
            #print("num%i",num%i)
            return False;
        elif i==math.sqrt(num):
            return False;
     
        i=i+1;
    return True;


def set_primos(inicio, fin, array_primos, rank, size):
    #Búsqueda paralelizada
    for i in range(inicio,fin,1):
        #Si es primo añadimos elemento al array de primos
        if i > 2:
            if es_primo(i,fin,array_primos):
                array_primos=np.append(array_primos,i);
          
    return array_primos;

    
def rango_primos(num, rank, size):
    #Inicializamos el array según que procesador es el que lo lanza
    if rank==2:
        rank_=[2];
    elif rank%2==0:
        rank_=[];
    else:
        rank_=[rank+2];
        
    array_primos=np.array(rank_, dtype=np.int64);
    
    if num > size:
        rango=int(num/div);
        inicio=rango*rank;
        fin = inicio+rango;
        if(fin > num):
            fin = fin -1;

        #Paralelizamos las llamadas en los diferentes procesadores
        array_primos = set_primos(inicio, fin, array_primos, rank, size);
        
    return array_primos, inicio, fin;


print(MPI.Get_processor_name(),'está corriendo')
print("Proceso ", os.getpid())

primos,inicio,fin=rango_primos(num, rank, size);

totalb=0;
demanda_mem1=0;

#Recorremos los diferentes procesadores para extraer los datos obtenidos
for i in range(0,size):
    countb = comm.bcast(primos,i)
    totalb = totalb + int(len(countb))
   
total = comm.reduce(totalb,MPI.BOR,0);
    
print("\nPROCESADOR ",rank, "ESTA CALCULANDO LOS PRIMOS:", primos);
print("\nPROCESADOR ",rank," HA CALCULADO EN EL RANGO:",inicio, fin);

if (rank == 0):
    print ("Total de procesadores: ",size);
    print("\nEL TOTAL DE NÚMEROS PRIMOS DESDE ",2,"HASTA",num,"SON :",total);

print('');
