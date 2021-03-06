
# 6.00.2x Problem Set 4

# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics (PS4 In the Bottom)

import numpy
import random
import pylab
import matplotlib.pyplot as plt
x = 3
''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        if self.getClearProb() > random.random():
            return True
        else:
            return False

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

      
        if self.maxBirthProb * (1 - popDensity) > random.random():
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        else:
            raise NoChildException('NoChildException')


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)     


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        alive = []
        for virus in self.viruses:
            if not virus.doesClear():
                alive.append(virus)
        self.viruses = alive[:]
        
        newDensity = len(self.viruses)/float(self.maxPop)
        offspring = []
        for virus in self.viruses:
                try:
                    offspring.append(virus.reproduce(newDensity))    
                except NoChildException:
                    continue
        self.viruses.extend(offspring)
        return len(self.viruses)

#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    listViruses = []
    for instance in range(numViruses):
        virus = SimpleVirus(maxBirthProb, clearProb)
        listViruses.append(virus)
    
    population = []
    for trial in range(numTrials):
        patient = Patient(listViruses, maxPop)
        
        for run in range(300):
            population.append(float(patient.update()))
    pylab.figure('Simulation Graph')
    pylab.plot(range(300 * numTrials), population)
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend()
    pylab.show()


#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        if drug not in self.resistances:
            return False
        if self.resistances[drug] == True:
            return True
        else:
            return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        
        num_resist = 0
        for drug in activeDrugs:
            if self.isResistantTo(drug):
                num_resist +=1
            
        if num_resist == len(activeDrugs):    
            if self.maxBirthProb * (1 - popDensity) > random.random():
                for drug in self.getResistances():
                    if self.isResistantTo(drug) == True: 
                        if 1- self.mutProb > random.random():
                            self.resistances[drug] = True
                        if self.mutProb > random.random():
                            self.resistances[drug] = False
                    elif not self.isResistantTo(drug):
                        if self.mutProb > random.random():
                            self.resistances[drug] = True
                        if 1-self.mutProb > random.random():
                            self.resistances[drug] = False
                return ResistantVirus(self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)
            else:
                raise NoChildException('NoChildException')
        else:
            raise NoChildException('NoChildException')



class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.viruses = viruses
        self.maxPop = maxPop
        self.administered_drugs = []
        

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.administered_drugs:
            self.administered_drugs.append(newDrug)
        

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.administered_drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        num_resist = 0
        num_imun = 0
        for virus in self.viruses:
            for drug in drugResist:
                if virus.isResistantTo(drug):
                    num_resist +=1
            if num_resist != len(drugResist):
                num_resist = 0
            elif num_resist == len(drugResist):
                num_imun +=1
                num_resist = 0    
        return num_imun
    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        alive = []
        for virus in self.viruses:
            if not virus.doesClear():
                alive.append(virus)
        self.viruses = alive[:]
        newDensity = len(self.viruses)/float(self.maxPop)
        offspring = []
        for virus in self.viruses:
            try:
                offspring.append(virus.reproduce(newDensity, self.administered_drugs))
            except NoChildException:
                pass
        self.viruses.extend(offspring)
        return len(self.viruses)

#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    steps = 300
    treatOnStep = 150
    trialResultsTot = [[] for s in range(steps)]
    trialResultsRes = [[] for s in range(steps)]
    for __ in range(numTrials):
        viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)
        for step in range(steps):
            if step == treatOnStep:
                patient.addPrescription("guttagonol")
            patient.update()
            trialResultsTot[step].append(patient.getTotalPop())
            trialResultsRes[step].append(patient.getResistPop(["guttagonol"]))
    resultsSummaryTot = [sum(l) / float(len(l)) for l in trialResultsTot]
    resultsSummaryRes = [sum(l) / float(len(l)) for l in trialResultsRes]
    pylab.plot(resultsSummaryTot, label="Total Virus Population")
    pylab.plot(resultsSummaryRes, label="Resistant Virus Population")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("time step")
    pylab.ylabel("# viruses")
    pylab.legend()
    pylab.show()
    


'''
PS4 
'''
'''
PART A - THE EFFECT OF DELAYING TREATMENT ON PATIENT DISEASE

Problem 1 - Percentage Cured:
delay = 300
0 - 5%

delay = 150
0 - 5%

delay = 75
6 - 15%

delay = 0
 86 - 100%


Problem 2 - Distributions:
  None of the above

Problem 3 - Relationships:
Applying the drug earlier means the patient is more likely to be cured.

Problem 4 - Changing Parameters:
1.Increasing the length of the viruses list decreases the number of patients cured.
True

2.Increasing the maxPop decreases the number of patients cured.
True

3.Increasing the maxBirthProb decreases the number of patients cured.
True

4.Increasing the clearProb decreases the number of patients cured.
False

5.Initializing each virus with resistance to guttagonol means no viruses will be killed.
False
'''



'''
PART B - DESIGNING A TREATMENT PLAN WITH TWO DRUGS

Problem 1 - Percentage Cured:
1.delay of 2nd drug = 300
 0 - 15%

2.delay of 2nd drug = 150
 0 - 30% 

3.delay of 2nd drug = 75
 31 - 65% 

4.delay of 2nd drug = 0
 66 - 100%

 Problem 2 - Relationships:
 Applying the 2nd drug earlier means the patient is more likely to be cured.


Problem 3 - Changing mutProb:
-Increasing mutProb will increase the number of cured patients.
False


Problem 4 - Relationships:
-The relationship between number of cured patients and when the delay occurs is linear.
False

Problem 5 - Variance:
delay of 2nd drug = 0
'''


'''
PART C - PATIENT NON-COMPLIANCE
Problem 1 - Modeling Approaches:
Make a new class called BadPatient that never takes its medication.
Create a small, random number of these and intersperse them
with the regular TreatedPatients. 


Problem 2 - Non-Compliance:
Fewer patients would be cured 
or in remission at the end of the simulations.


'''
# PROBLEM 1
#        

def simulationDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb,numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, {'guttagonol': False}, mutProb, numTrials )
    steps = 525
    steps1 = 300
    steps2 = 150
    steps3 = 75
    steps4 = 1
    treatSteps = 150
    cond75 = []
    cond150 = []
    cond300 = []
    cond0 = []
    for __ in range(numTrials):
        viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)
        for step in range(steps4):
            if step == 0:
                patient.addPrescription("guttagonol")
                for tstep in range(treatSteps):
                        patient.update()
            cond0.append(patient.getTotalPop())
    for __ in range(numTrials):          
        viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)                   
        for step in range(steps3+treatSteps):
            if step == 74:
                patient.addPrescription("guttagonol")
            patient.update()
            cond75.append(patient.getTotalPop())
    for __ in range(numTrials):    
        viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)
        for step in range(steps2+treatSteps):
            if step == 149:
                patient.addPrescription("guttagonol")
            patient.update()
            cond150.append(patient.getTotalPop())
    for __ in range(numTrials):  
        viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)
        for step in range(steps1+treatSteps):
            if step == 299:
                patient.addPrescription("guttagonol")
            patient.update()
            cond300.append(patient.getTotalPop())
    cond0 = pylab.array(cond0)
    cond75 = pylab.array(cond75)
    cond150 = pylab.array(cond150)
    cond300 = pylab.array(cond300)        
    print cond0
    print cond75
    print cond150
    print cond300
    f, axarr = plt.subplots(2, 2)
    axarr[0, 0].hist(cond0, numTrials)
    axarr[0, 0].set_title('Condition 0')
    axarr[0, 1].hist(cond75, numTrials)
    axarr[0, 1].set_title('Condition 75')
    axarr[1, 0].hist(cond150, numTrials ** 2)
    axarr[1, 0].set_title('Condition 150')
    axarr[1, 1].hist(cond300, numTrials ** 2)
    axarr[1, 1].set_title('Condition 300')
    plt.show()
    
            


#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb,numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, {'guttagonol': False}, mutProb, numTrials )
    steps1 = 300
    steps2 = 150
    steps3 = 75
    steps4 = 0
    treatSteps = 150
    cond75 = []
    cond150 = []
    cond300 = []
    cond0 = []
    for __ in range(numTrials):
        viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)
        for step in range(steps4+treatSteps+treatSteps):
            if step == treatSteps:
                patient.addPrescription("guttagonol")
            if step == steps4+treatSteps:
                patient.addPrescription("grimpex")
            patient.update()
            cond0.append(patient.getTotalPop())
    for __ in range(numTrials):          
        viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)                   
        for step in range(steps3+treatSteps+treatSteps):
            if step == treatSteps:
                patient.addPrescription("guttagonol")
            if step == steps3+treatSteps:
                patient.addPrescription("grimpex")
            patient.update()
            cond75.append(patient.getTotalPop())
    for __ in range(numTrials):    
        viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)
        for step in range(steps2+treatSteps+treatSteps):
            if step == treatSteps:
                patient.addPrescription("guttagonol")
            if step == steps2+treatSteps:
                patient.addPrescription("grimpex")
            patient.update()
            cond150.append(patient.getTotalPop())
    for __ in range(numTrials):  
        viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)
        for step in range(steps1+treatSteps+treatSteps):
            if step == treatSteps:
                patient.addPrescription("guttagonol")
            if step == steps1+treatSteps:
                patient.addPrescription("grimpex")
            patient.update()      
            cond300.append(patient.getTotalPop())
    cond0 = pylab.array(cond0)
    cond75 = pylab.array(cond75)
    cond150 = pylab.array(cond150)
    cond300 = pylab.array(cond300)        
    print cond0
    print cond75
    print cond150
    print cond300
    f, axarr = plt.subplots(2, 2)
    axarr[0, 0].hist(cond0, numTrials)
    axarr[0, 0].set_title('Condition 0')
    axarr[0, 1].hist(cond75, numTrials)
    axarr[0, 1].set_title('Condition 75')
    axarr[1, 0].hist(cond150, numTrials ** 2)
    axarr[1, 0].set_title('Condition 150')
    axarr[1, 1].hist(cond300, numTrials ** 2)
    axarr[1, 1].set_title('Condition 300')
    plt.show()
    
#simulationTwoDrugsDelayedTreatment(100, 1000, 0.1, 0.05, {'guttagonol': False, 'grimpex':False}, 0.005, 100)
           