from scipy import integrate # for numerical integration
import csv # for importing data from csv files
import numpy as np # for general numerical operations
import matplotlib.pyplot as plt # for making plots
import scipy.odr as odr # for curve fitting with multivariate uncertainty
import scipy.stats as stats # for statistical calculations

###############################################################################################################
# define the fit function
# B is an array of the fit parameters, and x is the independent variable
def f(B, x): 
    return np.piecewise(x, 
                        [
                            x < B[0], 
                            (B[0] <= x) & (x <= B[1])
                        ], 
                        [
                            lambda x: B[2], 
                            lambda x: B[2] - B[3]*(x-B[0]), 
                            lambda x: (B[2] - B[3]*(B[1]-B[0]))*np.exp(-(x-B[1])/B[4])
                        ])

 # a model for the field decay

###############################################################################################################
# data for the 17 Ohm shunt resistor
times1 = []
voltages1 = []

with open('ALL0000/F0000CH1.csv', 'r', newline='') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    next(csvReader, None)
    for row in csvReader:
        times1.append(float(row[3]))
        voltages1.append(-1.0*float(row[4]))

offset1 = np.mean(voltages1[1:40]) # find the initial value during the time before the field switches

voltages1adj = [val - offset1 for val in voltages1] # subtract the initial value

fields1 = integrate.cumulative_trapezoid(voltages1adj) # numerically integrate dB/dt
fields1adj = [(val -fields1[-1])/(fields1[1]-fields1[-1]) for val in fields1]

p01 = [0.0000036, 0.000021, 1, 15000, .00009] # initial guess for fit parameters: offset, slope

x_guess = np.linspace(np.min(times1[1:]), np.max(times1[1:]), 1000) # this defines a range from the minimum of our data to the max of our data, and splits it up into 100 evenly-spaced values
y_guess1 = f(p01, x_guess) # this applies our fit function to the entire range defined above

# set up and perform the non-linear regression
myfunc = odr.Model(f) # put our fit function into a special container
mydata1 = odr.RealData(times1[1:], fields1adj) # put all our data into a special container
myodr1 = odr.ODR(mydata1, myfunc, beta0 = p01, sstol = 1e-20, job=00000) # set up a fitting data structure
myoutput1 = myodr1.run() # perform the nonlinear regression to find best-fit parameters

sd1  = myoutput1.sd_beta # the normalized standard deviations
p1   = myoutput1.beta # the best-fit parameters

print(p1) # if the fit converged, we should see a list of two parameters: the offset and the slope
print(sd1) # this gives the SD for the model parameters

x_fit1 = np.linspace(np.min(times1[1:]), np.max(times1[1:]), 1000) # this defines a range from the minimum of our data to the max of our data, and splits it up into 100 evenly-spaced values
y_fit1 = f(p1, x_fit1) # this applies our fit function to the entire range defined above

plt.plot(times1[1:], fields1adj,label='Data')
plt.plot(x_guess, y_guess1,'g',label='Guess')
plt.plot(x_fit1, y_fit1,'r',label='Best Fit')
plt.xlabel('Time since switch (s)')
plt.ylabel('Normalized magnetic field (A.U.)')
plt.legend(loc=1)
plt.title(r'$R_s=17~\Omega$')
plt.show()


###################################################################################################################
# data for the 1.0 Ohm shunt resistor

times2 = []
voltages2 = []

with open('ALL0001/F0001CH1.csv', 'r', newline='') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    next(csvReader, None)
    for row in csvReader:
        times2.append(float(row[3]))
        voltages2.append(-1.0*float(row[4]))


offset2 = np.mean(voltages2[1:40])
voltages2adj = [val - offset2 for val in voltages2]

fields2 = integrate.cumulative_trapezoid(voltages2adj)
fields2adj = [(val -fields2[-1])/(fields2[1]-fields2[-1]) for val in fields2]

p02 = [0.0000046, 0.000021, 1, 15000, .000092]  # initial guess for fit parameters: offset, slope

y_guess2 = f(p02, x_guess) # this applies our fit function to the entire range defined above

# set up and perform the non-linear regression
mydata2 = odr.RealData(times2[1:], fields2adj) # put all our data into a special container
myodr2 = odr.ODR(mydata2, myfunc, beta0 = p02, sstol = 1e-20, job=00000) # set up a fitting data structure
myoutput2 = myodr2.run() # perform the nonlinear regression to find best-fit parameters

sd2  = myoutput2.sd_beta # the normalized standard deviations
p2   = myoutput2.beta # the best-fit parameters

print(p2) # if the fit converged, we should see a list of two parameters: the offset and the slope
print(sd2) # this gives the SD for the model parameters

x_fit2 = np.linspace(np.min(times2[1:]), np.max(times2[1:]), 1000) # this defines a range from the minimum of our data to the max of our data, and splits it up into 100 evenly-spaced values
y_fit2 = f(p2, x_fit2) # this applies our fit function to the entire range defined above

plt.plot(times2[1:], fields2adj,label='Data')
plt.plot(x_guess, y_guess2,'g',label='Guess')
plt.plot(x_fit2, y_fit2,'r',label='Best Fit')
plt.xlabel('Time since switch (s)')
plt.ylabel('Normalized magnetic field (A.U.)')
plt.title(r'$R_s=1.0~\Omega$')
plt.legend(loc=1)
plt.show()

###################################################################################################################
# data for the 0.1 Ohm shunt resistor

times3 = []
voltages3 = []

with open('ALL0002/F0002CH1.csv', 'r', newline='') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    next(csvReader, None)
    for row in csvReader:
        times3.append(float(row[3]))
        voltages3.append(-1.0*float(row[4]))

offset3 = np.mean(voltages3[1:8])
voltages3adj = [val - offset3 for val in voltages3]

fields3 = integrate.cumulative_trapezoid(voltages3adj)
fields3adj = [(val -fields3[-1])/(fields3[1]-fields3[-1]) for val in fields3]

p03 = [0.0000043, 0.000031, 1, 25500, .00002] # initial guess for fit parameters: offset, slope

y_guess3 = f(p03, x_guess) # this applies our fit function to the entire range defined above

# set up and perform the non-linear regression
mydata3 = odr.RealData(times3[1:], fields3adj) # put all our data into a special container
myodr3 = odr.ODR(mydata3, myfunc, beta0 = p03, sstol = 1e-20, job=00000) # set up a fitting data structure
myoutput3 = myodr3.run() # perform the nonlinear regression to find best-fit parameters

sd3  = myoutput3.sd_beta # the normalized standard deviations
p3   = myoutput3.beta # the best-fit parameters

print(p3) # if the fit converged, we should see a list of two parameters: the offset and the slope
print(sd3) # this gives the SD for the model parameters

x_fit3 = np.linspace(np.min(times3[1:]), np.max(times3[1:]), 1000) # this defines a range from the minimum of our data to the max of our data, and splits it up into 100 evenly-spaced values
y_fit3 = f(p3, x_fit3) # this applies our fit function to the entire range defined above

plt.plot(times3[1:], fields3adj,label='Data')
plt.plot(x_guess, y_guess3,'g',label='Guess')
plt.plot(x_fit3, y_fit3,'r',label='Best Fit')
plt.xlabel('Time since switch (s)')
plt.ylabel('Normalized magnetic field (A.U.)')
plt.legend(loc=1)
plt.title(r'$R_s=0.1~\Omega$')
plt.show()

###################################################################################################################
# data for the 200 V Zener diode

times4 = []
voltages4 = []

with open('ALL0003/F0003CH1.csv', 'r', newline='') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    next(csvReader, None)
    for row in csvReader:
        times4.append(float(row[3]))
        voltages4.append(-1.0*float(row[4]))

offset4 = np.mean(voltages4[1:40])
voltages4adj = [val - offset4 for val in voltages4]

#plt.plot(times4, voltages4adj,label='Data')
#plt.show()

fields4 = integrate.cumulative_trapezoid(voltages4adj)
fields4adj = [(val -fields4[-1])/(fields4[1]-fields4[-1]) for val in fields4]
#fields4adj = [(val) for val in fields4]

p04 = [0.0000043, 0.000031, 1, 25500, .00002] # initial guess for fit parameters: offset, slope

y_guess4 = f(p04, x_guess) # this applies our fit function to the entire range defined above

# set up and perform the non-linear regression
mydata4 = odr.RealData(times4[1:], fields4adj) # put all our data into a special container
myodr4 = odr.ODR(mydata4, myfunc, beta0 = p04, sstol = 1e-20, job=00000) # set up a fitting data structure
myoutput4 = myodr4.run() # perform the nonlinear regression to find best-fit parameters

sd4  = myoutput4.sd_beta # the normalized standard deviations
p4   = myoutput4.beta # the best-fit parameters

print(p4) # if the fit converged, we should see a list of two parameters: the offset and the slope
print(sd4) # this gives the SD for the model parameters

x_fit4 = np.linspace(np.min(times4[1:]), np.max(times4[1:]), 1000) # this defines a range from the minimum of our data to the max of our data, and splits it up into 100 evenly-spaced values
y_fit4 = f(p4, x_fit4) # this applies our fit function to the entire range defined above

plt.plot(times4[1:], fields4adj,label='Data')
plt.plot(x_guess, y_guess4,'g',label='Guess')
plt.plot(x_fit4, y_fit4,'r',label='Best Fit')
plt.xlabel('Time since switch (s)')
plt.ylabel('Normalized magnetic field (A.U.)')
plt.legend(loc=1)
plt.title(r'$V_Z=200~V$')
plt.show()

###################################################################################################################
# data for the 200 V Zener diode

times5 = []
voltages5 = []

with open('ALL0006/F0006CH1.csv', 'r', newline='') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    next(csvReader, None)
    for row in csvReader:
        times5.append(float(row[3]))
        voltages5.append(-1.0*float(row[4]))

offset5 = np.mean(voltages5[1:40])
voltages5adj = [val - offset5 for val in voltages5]

#plt.plot(times, voltages5adj,label='Data')
#plt.show()

fields5 = integrate.cumulative_trapezoid(voltages5adj)
fields5adj = [(val -fields5[-1])/(fields5[1]-fields5[-1]) for val in fields5]
#fields4adj = [(val) for val in fields4]

p05 = [0.0000036, 0.0000367, 1, 28300, .00007] # initial guess for fit parameters: offset, slope

y_guess5 = f(p05, x_guess) # this applies our fit function to the entire range defined above

# set up and perform the non-linear regression
mydata5 = odr.RealData(times5[1:], fields4adj) # put all our data into a special container
myodr5 = odr.ODR(mydata5, myfunc, beta0 = p05, sstol = 1e-20, job=00000) # set up a fitting data structure
myoutput5 = myodr5.run() # perform the nonlinear regression to find best-fit parameters

sd5  = myoutput5.sd_beta # the normalized standard deviations
p5   = myoutput5.beta # the best-fit parameters

#print(p4) # if the fit converged, we should see a list of two parameters: the offset and the slope
#print(sd4) # this gives the SD for the model parameters

x_fit5 = np.linspace(np.min(times5[1:]), np.max(times5[1:]), 1000) # this defines a range from the minimum of our data to the max of our data, and splits it up into 100 evenly-spaced values
y_fit5 = f(p5, x_fit5) # this applies our fit function to the entire range defined above

plt.plot(times5[1:], fields5adj,label='Data')
plt.plot(x_guess, y_guess5,'g',label='Guess')
plt.plot(x_fit5, y_fit5,'r',label='Best Fit')
plt.xlabel('Time since switch (s)')
plt.ylabel('Normalized magnetic field (A.U.)')
plt.legend(loc=1)
plt.title(r'$V_Z=200~V$')
plt.show()

###################################################################################################################
# data for the 200 V Zener diode

times6 = []
voltages6 = []

with open('ALL0007/F0007CH1.csv', 'r', newline='') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    next(csvReader, None)
    for row in csvReader:
        times6.append(float(row[3]))
        voltages6.append(-1.0*float(row[4]))

offset6 = np.mean(voltages6[1:40])
voltages6adj = [val - offset6 for val in voltages6]

#plt.plot(times, voltages5adj,label='Data')
#plt.show()

fields6 = integrate.cumulative_trapezoid(voltages6adj)
fields6adj = [(val -fields6[-1])/(fields6[1]-fields6[-1]) for val in fields6]
#fields4adj = [(val) for val in fields4]

p06 =[0.0000036, 0.0000367, 1, 28300, .00007] # initial guess for fit parameters: offset, slope

y_guess6 = f(p06, x_guess) # this applies our fit function to the entire range defined above

# set up and perform the non-linear regression
mydata6 = odr.RealData(times6[1:], fields6adj) # put all our data into a special container
myodr6 = odr.ODR(mydata6, myfunc, beta0 = p06, sstol = 1e-20, job=00000) # set up a fitting data structure
myoutput6 = myodr6.run() # perform the nonlinear regression to find best-fit parameters

sd6  = myoutput6.sd_beta # the normalized standard deviations
p6   = myoutput6.beta # the best-fit parameters

#print(p4) # if the fit converged, we should see a list of two parameters: the offset and the slope
#print(sd4) # this gives the SD for the model parameters

x_fit6 = np.linspace(np.min(times6[1:]), np.max(times6[1:]), 1000) # this defines a range from the minimum of our data to the max of our data, and splits it up into 100 evenly-spaced values
y_fit6 = f(p6, x_fit6) # this applies our fit function to the entire range defined above

plt.plot(times6[1:], fields6adj,label='Data')
plt.plot(x_guess, y_guess6,'g',label='Guess')
plt.plot(x_fit6, y_fit6,'r',label='Best Fit')
plt.xlabel('Time since switch (s)')
plt.ylabel('Normalized magnetic field (A.U.)')
plt.legend(loc=1)
plt.title(r'$V_Z=200~V$')
plt.show()

###################################################################################################################
# data for the 200 V Zener diode
"""
voltages7 = []

with open('ALL0016/F0016CH1.csv', 'r', newline='') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    next(csvReader, None)
    for row in csvReader:
        voltages7.append(-1.0*float(row[4]))

offset7 = np.mean(voltages6[1:4])
voltages7adj = [val - offset7 for val in voltages7]

#plt.plot(times, voltages5adj,label='Data')
#plt.show()

fields7 = integrate.cumulative_trapezoid(voltages7adj)
fields7adj = [(val -fields7[-1])/(fields7[1]-fields7[-1]) for val in fields7]
#fields4adj = [(val) for val in fields4]

#p04 = [0.0000036, 0.0000367, 1, 24000, .00007] # initial guess for fit parameters: offset, slope

#y_guess4 = f(p04, x_guess) # this applies our fit function to the entire range defined above

# set up and perform the non-linear regression
#mydata4 = odr.RealData(times[1:], fields4adj) # put all our data into a special container
#myodr4 = odr.ODR(mydata4, myfunc, beta0 = p04, sstol = 1e-20, job=00000) # set up a fitting data structure
#myoutput4 = myodr4.run() # perform the nonlinear regression to find best-fit parameters

#sd4  = myoutput4.sd_beta # the normalized standard deviations
#p4   = myoutput4.beta # the best-fit parameters

#print(p4) # if the fit converged, we should see a list of two parameters: the offset and the slope
#print(sd4) # this gives the SD for the model parameters

#y_fit4 = f(p4, x_fit) # this applies our fit function to the entire range defined above

plt.plot(times[1:], fields7adj,label='Data')
#plt.plot(x_guess, y_guess4,'g',label='Guess')
#plt.plot(x_fit, y_fit4,'r',label='Best Fit')
plt.xlabel('Time since switch (s)')
plt.ylabel('Normalized magnetic field (A.U.)')
plt.legend(loc=1)
plt.title(r'$V_Z=200~V$')
plt.show() """

###################################################################################################################
# combine all the switching plots together

fig = plt.figure()
plt.plot(times1[1:],fields1adj,'r-',label=r'$0.1~\Omega$ Oven')
plt.plot(times2[1:],fields2adj,'r:',label=r'$0.1~\Omega$ MOT')
plt.plot(times3[1:],fields3adj,'g-',label=r'$1~\Omega$ Oven')
plt.plot(times4[1:],fields4adj,'g:',label=r'$1~\Omega$ MOT')
plt.plot(times5[1:],fields5adj,'b-',label=r'$10~\Omega$ Oven')
plt.plot(times6[1:],fields6adj,'b:',label=r'$10~\Omega$ MOT')
#plt.plot(times[1:],fields7adj,'c-',label=r'$\infty~\Omega$')
plt.xlabel("Time (s)")
plt.ylabel("Field (A.U.)")
plt.suptitle('200 A Field switching')
plt.legend(loc=1)
plt.autoscale(enable=True, axis='x', tight=True)
plt.show()