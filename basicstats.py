import math
import matplotlib.pyplot as plt     
import numpy as np
import csvfile as f


def main():

    data_file = input("Input file : ")
    C0_freq, C1_freq, C0_ampl, C1_ampl, C0_phase, C1_phase, phdiff= f.readCSV(data_file)
    

    #limiting value
    first = C0_freq[0]
    #limiting index
    limit = [0]
    
    #find on which index value changes
    for i, element in enumerate(C0_freq):
        if (element-0.3) > first:
            print(element)
            first = C0_freq[i]
            limit.append(i)
            
    limit_2 = limit[1:]
    
    print(limit_2)
    
    #copies of arrays
    C0_freq_copy = C0_freq
    C0_freq = []
    C1_freq_copy = C1_freq
    C1_freq = []
    
    C0_ampl_copy = C0_ampl
    C0_ampl = []
    C1_ampl_copy = C1_ampl
    C1_ampl = []
    
    C0_phase_copy = C0_phase
    C0_phase = []
    C1_phase_copy = C1_phase
    C1_phase = []
    phdiff_copy = phdiff
    phdiff = []
    
    
    print(limit_2[0])
    start = 0
   
    #delete arrays smaller than specific length
    for i, element in enumerate(limit_2):
        if len(C0_freq_copy[start:element])>=5:
            C0_freq.append(C0_freq_copy[start:element])
            C1_freq.append(C1_freq_copy[start:element])
            C0_ampl.append(C0_ampl_copy[start:element])
            C1_ampl.append(C1_ampl_copy[start:element])
            C0_phase.append(C0_phase_copy[start:element])
            C1_phase.append(C1_phase_copy[start:element])
            phdiff.append(phdiff_copy[start:element])
            
        start = element
           
        
    #Check how many elements maximum and minimum arrays have
    longest_array_length = max(len(C0_freq[i]) for i in range(0,len(C0_freq)))
    shortest_array_length = min(len(C0_freq[i]) for i in range(0,len(C0_freq)))
    print("Longest array: " + str(longest_array_length))
    print("Shortest array: " + str(shortest_array_length))
    print("Length of C0_array: " +str(len(C0_freq)))

    #slice arrays to make them all of the same length
    for i,el in enumerate(C0_freq):
        length=len(C0_freq[i])
        
        if length > shortest_array_length:
            diff = length-shortest_array_length
            if diff == 1:
                C0_freq[i] = C0_freq[i][1:]
                C1_freq[i] = C1_freq[i][1:]
                C0_ampl[i] = C0_ampl[i][1:]
                C1_ampl[i] = C1_ampl[i][1:]
                C0_phase[i] = C0_phase[i][1:]
                C1_phase[i] = C1_phase[i][1:]
                phdiff[i] = phdiff[i][1:]
            else:
                C0_freq[i] = C0_freq[i][diff-1:-1]
                C1_freq[i] = C1_freq[i][diff-1:-1]
                C0_ampl[i] = C0_ampl[i][diff-1:-1]
                C1_ampl[i] = C1_ampl[i][diff-1:-1]
                C0_phase[i] = C0_phase[i][diff-1:-1]
                C1_phase[i] = C1_phase[i][diff-1:-1]
                phdiff[i] = phdiff[i][diff-1:-1]
    

    #copies of arrays
    R = 10 #resistance

    C0_freq_copy = C0_freq
    C0_freq = [[] for i in C0_freq_copy]
    C1_freq_copy = C1_freq
    C1_freq = [[] for i in C0_freq_copy]
    
    C0_ampl_copy = C0_ampl
    C0_ampl = [[] for i in C0_freq_copy]
    C1_ampl_copy = C1_ampl
    C1_ampl = [[] for i in C0_freq_copy]
    
    C0_phase_copy = C0_phase
    C0_phase = [[] for i in C0_freq_copy]
    C1_phase_copy = C1_phase
    C1_phase = [[] for i in C0_freq_copy]
    
    phdiff_copy = np.sin(np.radians(np.array(phdiff)*(-1))) 
    phdiff = [[] for i in C0_freq_copy]
    print("AAAAa" + str(phdiff_copy))
    
    Z_copy = [C1_ampl_copy[i] / C0_ampl_copy[i] * R for i in range(0, len(C0_ampl_copy))]
    Z = [[] for i in C0_freq_copy]
    
    data_copy = [C0_freq_copy,C1_freq_copy,C0_ampl_copy,C1_ampl_copy,
                 C0_phase_copy,C1_phase_copy,phdiff_copy, Z_copy]
    data = [C0_freq, C1_freq, C0_ampl, C1_ampl, C0_phase, C1_phase, phdiff,Z]
    
    names = ["Mean","Standard Dev","Standard Err","Variance","Max","Min",
             "Median","Skewness","Kurtosis"]
    
    def skewness(mean, std, array):
        x = np.sum([(((i-mean)/std)**3) for i in array])
        result = (1/len(array))* x
        return result
    
    def kurtosis(mean, std, array):
        x = np.sum([(((i-mean)/std)**4) for i in array])
        result = (1/len(array))* x -3   #excess kurtosis
        return result
    
    print(np.matrix(data_copy[0]))
    for i, el in enumerate(data_copy):
        for j, el2 in enumerate(data_copy[i]):
            data[i][j].append(np.mean(data_copy[i][j]))
            data[i][j].append(np.std(data_copy[i][j],ddof = 1))
            data[i][j].append(np.std(data_copy[i][j],ddof = 1)/math.sqrt(data_copy[i][j].size))
            data[i][j].append((np.std(data_copy[i][j], ddof = 1))**2)
            data[i][j].append(np.max(data_copy[i][j]))
            data[i][j].append(np.min(data_copy[i][j]))
            data[i][j].append(np.median(data_copy[i][j]))
            data[i][j].append(skewness(np.mean(data_copy[i][j]),np.std(data_copy[i][j],ddof = 1),data_copy[i][j]))
            data[i][j].append(kurtosis(np.mean(data_copy[i][j]),np.std(data_copy[i][j],ddof = 1),data_copy[i][j]))
            
    print(data[6][0])
    print("Z vertes: " + str(data[-1][0]))
    #calculating impedence:
    R = 10 #resistance ohm
    
    Z = [data[3][i][0]*R/data[2][i][0] for i in range(0,len(data[3]))]
    print("!!!!: " +str(len(Z)))
    
    freq = np.array(data[1])
    print("nu ziurim cia: " + str(names))
    
    #save data to csv file: 
    np.savetxt("sin with mass.csv", data[6], delimiter=",")
    
    frequencies = freq[:,0]
    print("-----")
    print("frequencies " + str(frequencies))
    print("standard error on frequency " + str(freq[:,2]))

    
main()
