import numpy as np
import os

ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

# Initialize a 3D array with zeros
size = len(ranks)
marray = np.zeros((size, size, size, size, size, size), dtype=int)

# Fill the array
for i, r1 in enumerate(ranks):
    for j, r2 in enumerate(ranks):
        for k, r3 in enumerate(ranks):
            for l,r4 in enumerate(ranks):
                for m, r5 in enumerate(ranks):
                    for n, r6 in enumerate(ranks):
                        sum = r1 + r2 + r3 + r4 + r5 + r6
                        if(max(i, j, k, l, m, n) == 12):
                            if (sum > 21 and sum <= 31) : 
                                sum = sum - 10
                            elif (sum > 31 and sum <= 41): 
                                sum = sum - 20
                            elif (sum > 41 and sum <= 51): 
                                sum = sum - 30
                            elif (sum > 51 and sum <= 61): 
                                sum = sum - 40
                            elif (sum > 61 and sum <= 71): 
                                sum = sum - 50
                            elif (sum > 71 and sum <= 81) : 
                                sum = sum - 60
                            elif (sum > 81 and sum <= 91): 
                                sum = sum - 70
                            elif (sum > 91 and sum <= 101): 
                                sum = sum - 80
                            elif (sum > 101 and sum <= 111): 
                                sum = sum - 90
                            elif (sum > 111 and sum <= 121): 
                                sum = sum - 100
                            marray[i, j, k, l, m, n] = sum
                        elif(sum <=21):
                            marray[i, j, k, l, m, n] = sum
                
np.save("6_dim_array[13^6]", marray)
#print(marray[11][11][11][11][11][11])

#for i in range(size):
#    for j in range(size):
#        for k in range(size):
#            for l in range(size):
#                print(f"Slice ({i}, {j} {k} {l}):")  # Slice at fixed (i, j), varying (k, l)
#                print(marray[i, j, k, l, :, :])  # Print the 2D matrix at [i, j, :, :]
#                print()

#print(size)
#print(marray[size-1])
