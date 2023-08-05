import numpy as np

def roundup(x,r=2):
        a = x*10**r
        a = np.ceil(a)
        a = a*10**(-r)

        if type(x) == float or type(x) == int or type(x) == np.float64:
            if a == 0 :
                a=10**(-r)
        else:
            try:                                           # rundet mehrdimensionale arrays
                for i,j in enumerate(a):
                    for k,l in enumerate(j):
                        if i == 0:  
                            i=10**(-r)
            except:                                        # rundet eindimensionale arrays
                for i,j in enumerate(a):
                    if i == 0:  
                        i=10**(-r)
                    
        return np.around(a,r)

def varianz_xy(x,x_mean,y,y_mean):
        return (1/len(x))*((x-x_mean)*(y-y_mean)).sum()

def varianz_x(x,x_mean):
    return (1/len(x))*((x-x_mean)**2).sum()
    
def mittel_varianzgewichtet(val,val_err):
    return (val/(val_err**2)).sum()/(1/(val_err**2)).sum()


# Passt die Rundung von Werten an die Fehler an, erzeugt strings fertig für tabellen
def errorRound(x, xerr):
    new_x = [0]*len(x)
    new_x_err = [0]*len(x)
    err_str = [0]*len(x)
    if len(x) == len(xerr):
        for i in range(len(x)):

            errstring = np.format_float_positional(xerr[i])                 # Fehler als String

            #-- rundet Fehler ---
            k = 0
            while (errstring[k] != '.'):
                k += 1
            if (errstring[0] == '1' or errstring[0] == '0'):
                k -= 1
            if errstring[0] == '1' and k == 0:

                new_x_err[i] = roundup(xerr[i],1)      # rundet einstelligen Zahlen

                if int(new_x_err[i]) == new_x_err[i]:
                    new_x_err[i] = int(new_x_err[i])   # falls ganzzahlig wird zu int konvertiert
                else:
                    k += 1

            elif (k != 0):
                k = -k
                new_x_err[i] = int(roundup(xerr[i],k+1))   # rundet alle Zahlen > 1 auf
                if errstring[0] == '1' and str(new_x_err[i])[0] != '1':
                    k -= 1

            else:
                #print('float',new_x_err[i])
                k = 2                                          # rundet fließkommazahlen < 1
                
                while errstring[k] == '0':
                    k += 1
                k -= 1
                if errstring[k+1] == '1' and round(xerr[i],k) != xerr[i]:
                    new_x_err[i] = roundup(xerr[i],k+1)
                    k += 1
                else:
                    new_x_err[i] = roundup(xerr[i],k)
                
                errstring = str(new_x_err[i])
                k = len(errstring) - 2

                if new_x_err[i] == int(new_x_err[i]):
                    k = 0                                      # setzt rundungsstelle auf 0, wenn fehler auf 1 gerundet wird
            err_str[i] = np.format_float_positional(new_x_err[i])  
            
            if new_x_err[i] == int(new_x_err[i]):
                err_str[i] = str(int(new_x_err[i]))
                new_x_err[i] = int(new_x_err[i])

            #print(k)
            #--passt nachkommastelle der werte an fehler
            errstring = np.format_float_positional(new_x_err[i])     
            
            if k >= 0:
                new_x[i] = round(x[i],k)
                numformat = '{:.'+str(k)+'f}'
                new_x[i] = numformat.format(new_x[i])
            else:
                new_x[i] = round(x[i],k+1)
                numformat = '{:.'+str(0)+'f}'
                new_x[i] = str(int(new_x[i]))
        
    else:
        print('errorRound: arrays must have same length')

    return new_x, err_str