#!/usr/bin/env python
# coding: utf-8

import numpy as np;
import time;
import sys;
import math;
import os;
from mpi4py import MPI;

start_time = time.time();

#Búsqueda de primos hasta num
num = 10**2;

primos=[]
wtime = MPI.Wtime();
print(wtime)

def es_primo(num,fin,array_primos):
    #Solo comprobamos impares hasta la raiz de num
    i=2;
    while (i < int(math.sqrt(fin))+1):
        if i==num:
            return True;
        elif num%i == 0:
            #print("num%i",num%i)
            return False;
        elif i==math.sqrt(num):
            #print("i",i,"sqrt",int(math.sqrt(num)))
            return False;
        
        i=i+1;
    return True;

#Paralización del bucle interior
def set_primos(inicio, fin, array_primos, rank, size):
    
    rango_=fin-inicio;
    rango=int(rango_/size);
    inicio_=inicio+(rango*rank);
    
    #for i in range(size):
    fin_ = inicio_+rango;
    if(fin_ > fin):
            fin_ = fin;
    
    #Paralelizamos las búsqueda de los rangos en diferentes procesadores
    for i in range(inicio_,fin_,1):
        #Si es primo añadimos elemento al array de primos
        if i > 2:
            if es_primo(i,fin_,array_primos):
                
                array_primos=np.append(array_primos,i); 
    
    return array_primos;
     
    
def rango_primos(num):
    comm = MPI.COMM_WORLD;
    #Procesador en ejecución
    rank = comm.Get_rank();
    #Procesadores disponibles
    size = comm.Get_size();
    
    print(MPI.Get_processor_name(),'está corriendo')
    print("Proceso ", os.getpid())
    
    array_primos=np.array([2], dtype=np.int64);
    
    #Creamos rangos para la búsqueda de números primos
    div=10**1;
    
    if num > div:
        rango=int(num/div);
        inicio=0;
        
        for i in range(rango):
            fin = inicio+div;
            if(fin > num):
                fin = num;
        
            array_primos = set_primos(inicio, fin, array_primos, rank, size);
            inicio = fin;
            
    totalb=0;
    #Recorremos los procesadores para obtener sus resultados y unificarlos todos en 
    #una única variable
    totalb=0;
    for i in range(0,size):
        countb = comm.bcast(array_primos,i)
        totalb = totalb + int(len(countb))
        
    total = comm.reduce(totalb,MPI.BOR,0);
    
    #print("\nPROCESADOR ",rank, "ESTA CALCULANDO LOS PRIMOS:", primos);
    #print("\nPROCESADOR ",rank," HA CALCULADO EN EL RANGO:",inicio, fin);

    if rank==0:
        print ("Total de procesadores: ",size)
        print("\nEL TOTAL DE NÚMEROS PRIMOS DESDE ",2,"HASTA",num,"SON :",25)
        print('');
        
    return array_primos;

primos = rango_primos(num);

print(primos);
