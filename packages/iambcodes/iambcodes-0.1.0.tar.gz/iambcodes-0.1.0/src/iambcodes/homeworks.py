import ipywidgets as widgets
import random as rd
import numpy as np

##########
##########
##########
#class for homework 3
##########
##########
##########

class homework_three():
#class homework_three_test():
    def __init__(self, stdID):
        # Check if Student-ID is an integer and if the function is to be run in "test-mode"
        
        #'TEst-Mode' is activated by the Std-ID input: 123456789
        # For this to be viable, 123456789 CANNEVER be a viable student-id
        if type(stdID) == int and stdID == 123456789:
            self.stdID = "testing"
        elif type(stdID) == int and stdID != 123456789:
            self.stdID = stdID
        else:
            print("Student ID required to be an integer.\nPlease try again!\n\n")
            pass
        
        # How many rngs are to be created for new/changed parameters
        self.numberofrandomnumbers = 6
        
        # Create RNs on the basis of the studentID
        self.initiate_homework()
        
        # Create variables using the generated RNs
        self.create_question_variables()
        
        # List of self.parameters:
        #self.stID
        #self.listofrndms
        
        #self.newYxs
        #self.newH
        #self.newO
        #self.newN
        
        #self.newRO2
        #self.newRCO2
        
        self.hq1tgl = 0 #help_question_1_toggle
        self.hq2tgl = 0 #help_question_2_toggle
        
        # build widgets for the questions
        self.question_one_display = self.build_question_one()
        self.question_two_display = self.build_question_two()
        
        
    def initiate_homework(self):
    # Parameters:
    # stdID is an integer used to seed the rng
        # IF stdID is given the string "test", it's supposed to return the string "test"
        # This string is then used to thest functions using standard values
    # counter is an integer used to define how many rngs are created.
        #print("Matriculation-Number accepted.\n\nGenerating random numbers..")
        #print("Matriculation-Number accepted.\n\nGenerating personalized homework parameters..")
        if self.stdID == "testing":
            print("#####\n\nTesting functionality\n\n#####")
            print("#####\n\The Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")
            # NOTE: no self.listofrndms is created in test mode
        else:
        #RNG for this homework
        #IMPORTANT: rd.seed() is set GLOBALLY, as far as we observed
        #this means: the solution-codes are ALWAYS IDENTICAL FOR A UNIQUE STid
        #if rd.seed() is not refreshed after generation of listofrndms.
        #In this version, the generated solution-codes are supposed to be random, therefore. rd.seed() gets refreshed
            rd.seed(self.stdID)
            self.listofrndms = [rd.random() for i in range(self.numberofrandomnumbers)] #create new random numbers that can be used to modify parameters
            rd.seed()
        return
    
    def create_question_variables(self):
        #function returns all generated homework parameters and a boolean 
        #thats used to toggls help_question_1_toggle to  0 (helpoption was not used)
        if self.stdID != "testing":
            #print("\nGenerating personalized homework parameters...\n")
            ###PARAMATERS for QUESTION 1
            self.newYxs = 1+round(self.listofrndms[0],1) #range 1.0-2.0
            self.newH = 1.5+round((self.listofrndms[1]*0.5),1) #range 1.5-2.0
            self.newO = 0.3+round((self.listofrndms[2]*0.4),1) #range 0.3-0.7
            self.newN = 0.1+round((self.listofrndms[3]*0.2),1) #range 0.1-0.3

            ###PARAMATERS for QUESTION 2
            self.newRO2 = 3000+round((self.listofrndms[4]*500)) #range 3000-3500)
            self.newRCO2 = 8000+round((self.listofrndms[5]*500)) #range 8000-8500)
        
        elif self.stdID == "testing":
            ###PARAMATERS for QUESTION 1
            self.newYxs = 2
            self.newH = 1.8
            self.newO = 0.5
            self.newN = 0.2
            
            ###PARAMATERS for QUESTION 2
            self.newRO2 = 3300
            self.newRCO2 = 8300
        return
    
    
###############
###############
###############
    def correct_homework_three_question_one(self, RQ):
        #Parameters:
        #RQ: Student solution. Will be comparied with opimal solution and decides if task was done correctly or not
        
        #newYxs, newH, newO, newN: changed parameters based on the seed.
            #are needed to calculate the opimal solution
        #hq1tgl: boolean. Decides if the student used the help-option or not

        #output formula:
        # X-YZ
        # X: was the help used? yes or no
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) <10 OR >= 10:
        #    -> 2x randomint
        if self.stdID == "testing":
            with self.question_one_display.children[0]:
                print('\nTesting solution calculation...\n')
                print("#####\n\nThe Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")

                Yxc = self.newYxs - 1
                print("\nYxc:",Yxc)
                Yxn = self.newN
                Yxw = (self.newYxs*2 + Yxn*3 - self.newH)/2
                print("\nYxw:",Yxw)
                Yxo = (-self.newYxs + Yxw + 2*Yxc + self.newO)/2
                print("\nYxo:",Yxo)

                realRQ = Yxc/Yxo
                print("\nrealRQ:",realRQ)        
        
        
        if type(self.stdID) == int:
            stdIDstr = str(self.stdID)


            #Calculation of the solution:
            with self.question_one_display.children[-1]:

                Yxc = self.newYxs - 1
                #print(Yxc)
                Yxn = self.newN
                Yxw = (self.newYxs*2 + Yxn*3 - self.newH)/2
                #print(Yxw)
                Yxo = (-self.newYxs + Yxw + 2*Yxc + self.newO)/2
                #print(Yxo)

                realRQ = Yxc/Yxo
                #print(realRQ)

                #Check if student solution is correct
                #Assumes aswer was rounded to 2 decimals
                if round(realRQ,2) == RQ:
                    self.question_one_display.children[-3].children[0].disabled = True
                    self.question_one_display.children[-3].children[1].disabled = True
                    print("Solution corect! RQ is {}".format(round(realRQ,2)))

                    solcode = ""
                     #Help-option was not used
                    if self.hq1tgl == 0:
                        solcode+=(str(rd.randrange(0,4)))
                    #Help-option was used
                    elif self.hq1tgl == 1:
                        solcode+=(str(rd.randrange(5,9)))

                    if int(stdIDstr[-1])+int(stdIDstr[-2]) < 10:
                        solcode+=(str(rd.randrange(0,4)))
                        solcode+=(str(rd.randrange(0,4)))
                    elif int(stdIDstr[-1])+int(stdIDstr[-2]) >= 10:
                        solcode+=(str(rd.randrange(5,9)))
                        solcode+=(str(rd.randrange(5,9)))    
                    # PRINT THE CODE
                    print("Here's your code!\n\n"+solcode+"\n\nPlease upload it in the designated Moodle-Task.") 

                #If the solution was not correct, the students can try again
                else:
                    print("Solution WRONG!\nDon't give up and try again!")
                    self.question_one_display.children[-1].clear_output(wait=True)



###############
###############
###############
    def correct_homework_three_question_two(self,Yield_Ethanol, Yield_Substrate):
        #Parameters:
        #Yield_Ethanol, Yield_Substrate: Student solution. Will be comparied with opimal solution and decides if task was done correctly or not
        #ewYxs, newH, newO, newN, newRO2, newRCO2: changed parameters based on the seed.
            #are needed to calculate the opimal solution
        #hq2tgl: boolean. Decides if the student used the help-option or not

        #output formula:
        # X-YZ
        # X: was the help used? yes or no
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) <10 OR >= 10:
        #    -> 2x randomint

        if self.stdID == "testing":
            with self.question_two_display.children[0]:
                print('\nTesting solution calculation...\n')
                print("#####\n\nThe Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")


                #1. Converting biomass concentration from g/l to c-mol
                Xn = (round(46.5/(1*12+self.newH*1+self.newO*16+self.newN*14),2)*10000) 
                print("\nXn:",Xn)
                #Xn = ((50 g/L - 7 % ash)/(masses of C_1+H_newH+O_newO+N_newN) g/mol) * 10000 L = x cmol
                # 12, 1, 16, and 14 are the assumed molecular masses of the specific elements

                #2. Normalizing gas exchange rates
                rO2 = round(self.newRO2/Xn,2)
                rCO2 = round(self.newRCO2/Xn,2)
                print("\nrO2:",rO2)
                print("\nrCO2:",rCO2)

                #3. Calculating Yields, YXO, YXC
                mu = 0.35 #Growthrate = 0.35 1/h
                Yxo = rO2/mu
                Yxc = rCO2/mu
                Yxn = self.newN
                print("\nYxo:",Yxo)
                print("\nYxc:",Yxc)
                Ymatrixvar = np.array([[2,1],[1,-0.5]])
                Ymatrixsolvd = np.array([-1*(self.newH-2-2*Yxc-3*Yxn), -1*(self.newO+1*Yxc-1-2*Yxo)])
                Ymatrix = np.linalg.solve(Ymatrixvar,Ymatrixsolvd)
                Yxw,Yxe = Ymatrix
                Yxs = Yxe+1+Yxc
                print("\nYxe:",Yxe)
                print("\nYxs:",Yxs)

        if type(self.stdID) == int:
            stdIDstr = str(self.stdID)
            
            #Calculation of the solution:
            with self.question_two_display.children[-1]:

                #1. Converting biomass concentration from g/l to c-mol
                Xn = (round(46.5/(1*12+self.newH*1+self.newO*16+self.newN*14),2)*10000) 
                #Xn = ((50 g/L - 7 % ash)/(masses of C_1+H_newH+O_newO+N_newN) g/mol) * 10000 L = x cmol
                # 12, 1, 16, and 14 are the assumed molecular masses of the specific elements

                #2. Normalizing gas exchange rates
                rO2 = round(self.newRO2/Xn,2)
                rCO2 = round(self.newRCO2/Xn,2)

                #3. Calculating Yields, YXO, YXC
                mu = 0.35 #Growthrate = 0.35 1/h
                Yxo = rO2/mu
                Yxc = rCO2/mu
                Yxn = self.newN

                Ymatrixvar = np.array([[2,1],[1,-0.5]])
                Ymatrixsolvd = np.array([-1*(self.newH-2-2*Yxc-3*Yxn), -1*(self.newO+1*Yxc-1-2*Yxo)])
                Ymatrix = np.linalg.solve(Ymatrixvar,Ymatrixsolvd)
                Yxw,Yxe = Ymatrix
                Yxs = Yxe+1+Yxc

                #Check if student solution is correct
                #Assumes aswer was rounded to 2 decimals
                if round(Yxs,2) == Yield_Substrate and round(Yxe,2) == Yield_Ethanol:
                    self.question_two_display.children[-3].children[0].disabled = True
                    self.question_two_display.children[-3].children[1].disabled = True
                    print("Solution corect! Substrate yield is {}\nand Ethanol yield is {}".format(round(Yxs,2),round(Yxe,2)))

                    solcode = ""
                    #Help-option was not used
                    if self.hq2tgl == 0:
                        solcode+=(str(rd.randrange(0,4)))
                    #Help-option was used
                    elif self.hq2tgl == 1:
                        solcode+=(str(rd.randrange(5,9)))

                    if int(stdIDstr[-1])+int(stdIDstr[-2]) < 10:
                        solcode+=(str(rd.randrange(0,4)))
                        solcode+=(str(rd.randrange(0,4)))
                    elif int(stdIDstr[-1])+int(stdIDstr[-2]) >= 10:
                        solcode+=(str(rd.randrange(5,9)))
                        solcode+=(str(rd.randrange(5,9)))    
                    # PRINT THE CODE
                    print("Here's your code!\n\n"+solcode+"\n\nPlease upload it in the designated Moodle-Task.") 

                #If the solution was not correct, the students can try again
                elif round(Yxs,2) == Yield_Substrate and round(Yxe,2) != Yield_Ethanol:
                    print("Ethanol yield WRONG!\nPlease try again!")
                    self.question_two_display.children[-1].clear_output(wait=True)
                elif round(Yxs,2) != Yield_Substrate and round(Yxe,2) == Yield_Ethanol:
                    print("Substrate yield WRONG!\nPlease try again!")
                    self.question_two_display.children[-1].clear_output(wait=True)
                else:
                    #print("Real Yxe={}\nStudent_Ethanol_Yield={}".format(Yxe,Yield_Ethanol))
                    #print("Real Yxs={}\nStudent_Substrate_Yield={}".format(Yxs,Yield_Substrate))
                    print("Solution WRONG!\nDon't give up and try again!")
                    self.question_two_display.children[-1].clear_output(wait=True)

    ######
    # functions that create widgets
    #
    #
    #
    ###
    
    def build_question_one(self):
        listofwidgets = []
        
        # build question label/output (top 0)
        # build answer input (top 1)
        # build 'Check Answer button' (top 2.hbox-0)
        # build 'Get help button' (top 2. hbox-1)
        # build output (for commentsof help button) (top 3)
        # build output (for answer button feedback) (top 4)
        
        listofwidgets.append(widgets.Output(
        ))
        with listofwidgets[0]:
            #print("##########\n\nParameters for Question 1:\n\n"\
            #"Your glucose yield Y_(XS) is {} C-mol glucose/C-mol biomass\n\n"\
            #"Your biomass composition is CH_({})O_({})N_({})\n\n##########".format(self.newYxs,self.newH,self.newO,self.newN))
            print("")
            
        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='RQ:',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))


        
        i = []
        i.append(widgets.Button(
            value=False,
            description='Check RQ',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to check solution',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
                             
        i.append(widgets.Button(
            value=False,
            description='Calculation Help',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to get a tipp',
        #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
                 
        listofwidgets.append(widgets.HBox(i))
        
        listofwidgets.append(widgets.Output())
        listofwidgets.append(widgets.Output())
        
        disp = widgets.VBox(listofwidgets)
        return disp
###############
###############
###############
    def build_question_two(self):
            listofwidgets = []

            # build question label/output (top 0)
            # build answer input for Ethanol Yield (top 1)
            # build answer input for Substrate Yield (top 2)
            # build 'Check Answer button' (top 3.hbox-0)
            # build 'Get help button' (top 3. hbox-1)
            # build output (for commentsof help button) (top 4)
            # build output (for answer button feedback) (top 5)

            listofwidgets.append(widgets.Output(
            ))
            with listofwidgets[0]:
                #print("##########\n\nParameters for Question 2:\n\n"\
                #"Your O_2 Exchange-Rate is {} mol/h\n\n"\
                #"Your CO_2 Exchange-Rate is {} mol/h\n\n##########".format(self.newRO2,self.newRCO2))
                print("")
                
            listofwidgets.append(widgets.FloatText(
                value=0.00,
                description='Ethanol Yield:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='200px', height='40px')
            ))
            
            listofwidgets.append(widgets.FloatText(
                value=0.00,
                description='Substrate Yield:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='200px', height='40px')
            ))


            i = []
            i.append(widgets.Button(
                value=False,
                description='Check Yields',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Click to check solution',
                #     icon='check' # (FontAwesome names without the `fa-` prefix)
            ))

            i.append(widgets.Button(
                value=False,
                description='Calculation Help',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Click to get a tipp',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
            ))

            listofwidgets.append(widgets.HBox(i))

            listofwidgets.append(widgets.Output())
            listofwidgets.append(widgets.Output())

            disp = widgets.VBox(listofwidgets)
            return disp
    
    ######
    # ON-CLICK functions
    # 2 per question
    #
    #
    ###
    def on_question_one_help_button_clicked(self, click):
        self.hq1tgl = 1
        self.question_one_display.children[-3].children[1].disabled = True
        with self.question_one_display.children[-2]:
            txt = "##########\n" \
            "* The RQ is rate of CO_2 production divivided by the rate of O_2 production\n" \
            "  RQ = r(CO_2)/r(O_2)\n\n" \
            "* Yields correlate directly to rates\n" \
            "  RQ = r(CO_2)/r(O_2) = Y(CO_2)/Y(O_2)\n\n" \
            "* By calculating all yields for the known reaction, you will be able to identify the required yields\n" \
            "##########"
            print(txt)
    def on_question_one_answer_button_clicked(self, click):
        student_answer = self.question_one_display.children[1].value
        self.correct_homework_three_question_one(student_answer)
        
    def on_question_two_help_button_clicked(self, click):
        self.hq2tgl = 1
        self.question_two_display.children[-3].children[1].disabled = True
        with self.question_two_display.children[-2]:
            txt = "##########\n" \
            "Don't forget, that for Question 2, Ethanol is an additional product!\nYou also need to subtract the ash from the assumed Biomass.\n\n"\
            "* First, convert the biomass concentration from g/L to c-mol\n" \
            "  and normalize the gas exchange rates\n\n" \
            "* You can use the growth rates and exchange rates t determine\n  the yields of O_2 and CO_2\n\n" \
            "* How to solve the matrix can be seen in 'Example 1' (p. 19/20 of Lecture 4)\n"
            "##########\n"
            print(txt)
    def on_question_two_answer_button_clicked(self, click):
        student_answer_ethanol_yield = self.question_two_display.children[1].value
        student_answer_substrate_yield = self.question_two_display.children[2].value
        self.correct_homework_three_question_two(student_answer_ethanol_yield, student_answer_substrate_yield)

##########
##########
##########
#class for homework 4
##########
##########
##########

class homework_four():
#class homework_four_test():
    def __init__(self, stdID):
        # Check if Student-ID is an integer and if the function is to be run in "test-mode"
        
        #'TEst-Mode' is activated by the Std-ID input: 123456789
        # For this to be viable, 123456789 CAN NEVER be a viable student-id
        if type(stdID) == int and stdID == 123456789:
            self.stdID = "testing"
        elif type(stdID) == int and stdID != 123456789:
            self.stdID = stdID
        else:
            print("Student ID required to be an integer.\nPlease try again!\n\n")
            pass
        
        # How many rngs are to be created for new/changed parameters
        self.numberofrandomnumbers = 8
        
        # Create RNs on the basis of the studentID
        self.initiate_homework()
        
        # Create variables using the generated RNs
        self.create_question_variables()
        
        # List of self.parameters:
        #self.stID
        #self.listofrndms
        
        #self.newCoP (CombustionofProtein)
        #self.newCoC (CombustionofCarbohydrates)
        #self.newCoF (CombustionofFat)
        
        #self.newOCR (OxygenConsumptionrate)
        #self.newCPR (Carbon dioxide production rate)
        #self.newNSR (Nitrogen secretion rate)
        
        self.hq1tgl = 0 #help_question_1_toggle
        self.hq2tgl = 0 #help_question_2_toggle
        self.hq3tgl = 0 #help_question_2_toggle
        
        # build widgets for the questions
        self.question_one_display = self.build_question_one()
        self.question_two_display = self.build_question_two()
        self.question_three_display = self.build_question_three()
        
        
    def initiate_homework(self):
    # Parameters:
    # stdID is an integer used to seed the rng
        # IF stdID is given the string "test", it's supposed to return the string "test"
        # This string is then used to thest functions using standard values
    # counter is an integer used to define how many rngs are created.
        #print("Matriculation-Number accepted.\n\nGenerating random numbers..")
        #print("Matriculation-Number accepted.\n\nGenerating personalized homework parameters..")
        if self.stdID == "testing":
            print("#####\n\nTesting functionality\n\n#####")
            print("#####\n\The Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")
            # NOTE: no self.listofrndms is created in test mode
        else:
        #RNG for this homework
        #IMPORTANT: rd.seed() is set GLOBALLY, as far as we observed
        #this means: the solution-codes are ALWAYS IDENTICAL FOR A UNIQUE STid
        #if rd.seed() is not refreshed after generation of listofrndms.
        #In this version, the generated solution-codes are supposed to be random, therefore. rd.seed() gets refreshed
            rd.seed(self.stdID)
            self.listofrndms = [rd.random() for i in range(self.numberofrandomnumbers)] #create new random numbers that can be used to modify parameters
            rd.seed()
        return
    
    def create_question_variables(self):
        #function returns all generated homework parameters and a boolean 
        #thats used to toggls help_question_1_toggle to  0 (helpoption was not used)
        if self.stdID != "testing":
            #print("\nGenerating personalized homework parameters...\n")
            ###PARAMATERS for QUESTION 1
            self.newCoP = 4.0+round((self.listofrndms[0]*0.2),1) #range 4.0-4.2
            self.newCoC = 4.0+round((self.listofrndms[1]*0.3),1) #range 4.0-4.3
            self.newCoF = 9.0+round((self.listofrndms[2]*0.6),1) #range 9.0-9.6

            ###PARAMATERS for QUESTION 3
            self.newOCR = 0.5+round((self.listofrndms[4]*0.2)) #range 0.5-0.7)
            self.newCPR = 0.4+round((self.listofrndms[5]*0.2)) #range 0.4-0.6)
            self.newNSR = 0.05+round((self.listofrndms[6]*0.2)) #range 0.05-0.25)
            
        elif self.stdID == "testing":
            ###PARAMATERS for QUESTION 1
            self.newCoP = 4.1 #(CombustionofProtein [kcal/g])
            self.newCoC = 4.2 #(CombustionofCarbohydrates [kcal/g])
            self.newCoF = 9.3 #(CombustionofFat [kcal/g])
            
           ###PARAMATERS for QUESTION 3
            self.newOCR = 0.6 #(OxygenConsumptionrate [mol/h])
            self.newCPR = 0.52 #(Carbon dioxide production rate [mol/h])
            self.newNSR = 0.1 #(Nitrogen secretion rate [N/h])

        return
    
    
###############
###############
###############
    def correct_homework_four_question_one(self, YxqP, YxqC, YxqF):
        #Parameters:
        #YxqP, YxqC, YxqF: Student solutions. Will be comparied with opimal solution and decides if task was done correctly or not
        
        #newCoP, newCoC, newCoF: changed parameters based on the seed.
            #are needed to calculate the opimal solution
        #hq1tgl: boolean. Decides if the student used the help-option or not

        #output formula:
        # X-YZ
        # X: was the help used? yes or no
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) <10 OR >= 10:
        #    -> 2x randomint
        if self.stdID == "testing":
            with self.question_one_display.children[0]:
                print('\nTesting solution calculation...\n')
                print("#####\n\nThe Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")

                mp = 12+1.57+16*0.32+14*0.26 #CH_1.57O_0.32N_0.26
                mc = 12+2+16 #CH_2O
                mf = 12+1.92+16*0.12 #CH_1.92O_0.12
                
                print(self.newCoP * mp)
                print(self.newCoC * mc)
                print(self.newCof * mf)
        
        
        if type(self.stdID) == int:
            stdIDstr = str(self.stdID)


            #Calculation of the solution:
            with self.question_one_display.children[-1]:

                mp = 12+1.57+16*0.32+14*0.26 #CH_1.57O_0.32N_0.26
                mc = 12+2+16 #CH_2O
                mf = 12+1.92+16*0.12 #CH_1.92O_0.12
            
                #Check if student solutions are correct
                #Assumes aswer was rounded to 2 decimals
                if round(mp*self.newCoP,2) != YxqP:
                    print("Wrong CoP\nDon't give up and try again!")
                    self.question_one_display.children[-1].clear_output(wait=True)
                elif round(mc*self.newCoC,2) != YxqC:
                    print("Wrong CoC\nDon't give up and try again!")
                    self.question_one_display.children[-1].clear_output(wait=True)
                elif round(mf*self.newCoF,2) != YxqF:
                    print("Wrong CoF\nDon't give up and try again!")
                    self.question_one_display.children[-1].clear_output(wait=True)
                elif round(mp*self.newCoP,2) == YxqP & round(mc*self.newCoC,2) == YxqC & round(mf*self.newCoF,2) == YxqF:
                    self.question_one_display.children[-3].children[0].disabled = True
                    self.question_one_display.children[-3].children[1].disabled = True
                    print("Solution corect!")

                    solcode = ""
                    #Help-option was not used
                    if self.hq1tgl == 0:
                        solcode+=(str(rd.randrange(0,4)))
                    #Help-option was used
                    elif self.hq1tgl == 1:
                        solcode+=(str(rd.randrange(5,9)))

                    if int(stdIDstr[-1])+int(stdIDstr[-2]) < 10:
                        solcode+=(str(rd.randrange(0,4)))
                        solcode+=(str(rd.randrange(0,4)))
                    elif int(stdIDstr[-1])+int(stdIDstr[-2]) >= 10:
                        solcode+=(str(rd.randrange(5,9)))
                        solcode+=(str(rd.randrange(5,9)))    
                    # PRINT THE CODE
                    print("Here's your code!\n\n"+solcode+"\n\nPlease upload it in the designated Moodle-Task.") 



###############
###############
###############
    def correct_homework_four_question_two(self,student_answer_Ycs, student_answer_Ycf, student_answer_Ycp):
        #Parameters:
        #Yield_sugar (student_answer_Ycs), Yield_fat: student_answer_Ycf, Yield_protein student_answer_Ycp
        
        #newCoP, newCoC, newCoF: changed parameters based on the seed.
        #newOCR, newCPR, newNSR: changed parameters based on the seed.
            #are needed to calculate the opimal solution
        #hq2tgl: boolean. Decides if the student used the help-option or not

        #output formula:
        # X-YZ
        # X: was the help used? yes or no
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) <10 OR >= 10:
        #    -> 2x randomint
        
        
        # Hopefully temporary: list of solutions for all three Yields
        # In this HW_4 section, no parameters were changed yet.
        # Thus, the literature solutions arethe correct solutions
        #format: 
        #Y_cs = {A} + {B}*Y_co + {C}*Y_cn"
        #sol_Ycs= [A, B, C]
        sol_Ycs = [3.4,-2.4,-3.5]
        sol_Ycf = [-2.4,-2.4,0.3]
        sol_Ycp = [0.0,0.0,3.8]
        
        
        if self.stdID == "testing":
            with self.question_two_display.children[0]:
                print('\nTesting solution calculation...\n')
                print("#####\n\nThe Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")
                
                print("Yield sugar/carbohydrates: {} + {}*Y_co + {}*Y_c\n\n".format(sol_Ycs[0],sol_Ycs[1],sol_Ycs[2]))
                print("Yield fat: {} + {}*Y_co + {}*Y_c\n\n".format(sol_Ycf[0],sol_Ycf[1],sol_Ycf[2]))
                print("Yield protein: {} + {}*Y_co + {}*Y_c\n\n".format(sol_Ycp[0],sol_Ycp[1],sol_Ycp[2]))

        if type(self.stdID) == int:
            stdIDstr = str(self.stdID)
            
            #Calculation of the solution:
            with self.question_two_display.children[-1]:
                counter = 0
                
                for i in range(len(student_answer_Ycs)):
                    if round(student_answer_Ycs[i],1) != sol_Ycs[i]:
                        counter += 1
                        print('{}. variable of Ycs function is WRONG\n'.format(i))
                for i in range(len(student_answer_Ycf)):
                    if round(student_answer_Ycf[i],1) != sol_Ycf[i]:
                        counter += 1
                        print('{}. variable of Ycf function is WRONG\n'.format(i))
                for i in range(len(student_answer_Ycp)):
                    if round(student_answer_Ycp[i],1) != sol_Ycp[i]:
                        counter += 1
                        print('{}. variable of Ycp function is WRONG\n'.format(i))
                if counter != 0:
                    print('\n##########\nPLEASE TRY AGAIN!\n\n')
                    self.question_two_display.children[-1].clear_output(wait=True)
                elif counter == 0:
                    self.question_two_display.children[-3].children[0].disabled = True
                    self.question_two_display.children[-3].children[1].disabled = True
                    print("Solution correct!")

                    solcode = ""
                    #Help-option was not used
                    if self.hq2tgl == 0:
                        solcode+=(str(rd.randrange(0,4)))
                    #Help-option was used
                    elif self.hq2tgl == 1:
                        solcode+=(str(rd.randrange(5,9)))

                    if int(stdIDstr[-1])+int(stdIDstr[-2]) < 10:
                        solcode+=(str(rd.randrange(0,4)))
                        solcode+=(str(rd.randrange(0,4)))
                    elif int(stdIDstr[-1])+int(stdIDstr[-2]) >= 10:
                        solcode+=(str(rd.randrange(5,9)))
                        solcode+=(str(rd.randrange(5,9)))    
                    # PRINT THE CODE
                    print("Here's your code!\n\n"+solcode+"\n\nPlease upload it in the designated Moodle-Task.")

###############
###############
###############
    def correct_homework_four_question_three(self,student_answer_Yco, student_answer_Ycn, student_answer_Rxq):
        #Parameters:
        #Yield_co (student_answer_Yco) normalized to CO2, Yield_cn: student_answer_Ycn normalized to CO2, metablic rate student_answer_Rxq (kcal/h)
        
        #newCoP, newCoC, newCoF: changed parameters based on the seed.
        #newOCR, newCPR, newNSR: changed parameters based on the seed.
            #are needed to calculate the opimal solution
        #hq3tgl: boolean. Decides if the student used the help-option or not

        #output formula:
        # X-YZ
        # X: was the help used? yes or no
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) <10 OR >= 10:
        #    -> 2x randomint
        
        
        # Hopefully temporary: list of solutions for all three Yields
        # In this HW_4 section, te parameters of the chemical composition parameters were not changed yet.
        # Thus, the literature solutions are the correct solutions of Homework_4_2:
        #format: 
        #Y_cs = {A} + {B}*Y_co + {C}*Y_cn"
        #sol_Ycs= [A, B, C]
        sol_Ycs = [3.4,-2.4,-3.5]
        sol_Ycf = [-2.4,-2.4,0.3]
        sol_Ycp = [0.0,0.0,3.8]
        
        mp = 12+1.57+16*0.32+14*0.26 #CH_1.57O_0.32N_0.26
        mc = 12+2+16 #CH_2O
        mf = 12+1.92+16*0.12 #CH_1.92O_0.12
        
        if self.stdID == "testing":
            with self.question_three_display.children[0]:
                print('\nTesting solution calculation...\n')
                print("#####\n\nThe Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")
                
                Ycc = round(self.newCPR/self.newCPR,2) #(mol/h / mol/h)
                Yco = round(self.newOCR/self.newCPR,2) #(mol/h / mol/h)
                rn = self.newNSR/14 #(Secretion rate NH3 in gN/h / 14 g/mol)
                Ycn = round(rn/self.newCPR,4) #(mol/h / mol/h)
                
                print('Yco: \n',Yco)
                print('Ycn: \n',Ycn)
                
                Ycs = round(sol_Ycs[0]*Ycc+sol_Ycs[1]*Yco+sol_Ycs[2]*Ycn,2) #(mol/cmol)
                Ycf = round(sol_Ycf[0]*Ycc+sol_Ycf[1]*Yco+sol_Ycf[2]*Ycn,2) #(mol/cmol)
                Ycp = round(sol_Ycp[0]*Ycc+sol_Ycp[1]*Yco+sol_Ycp[2]*Ycn,2) #(mol/cmol)
                
                Yxq = Ycs*round(mp*self.newCoP,2)+Ycf*round(mf*self.newCoF,2)+Ycp*round(mp*self.newCoP,2) #(mol/cmol * kcal/cmol) = (kcal/cmol) || units not clear, might need second look
                Rxq = round(Yxq * self.newCPR,2) # kcal/cmol * mol/h = kcal/h || units not clear, might need second look
                
                print('Yxq: \n',Yxq)
                print('Rxq: \n',Rxq)


        if type(self.stdID) == int:
            stdIDstr = str(self.stdID)
            
            #Calculation of the solution:
            with self.question_three_display.children[-1]:
                
                Ycc = round(self.newCPR/self.newCPR,2) #(mol/h / mol/h)
                Yco = round(self.newOCR/self.newCPR,2) #(mol/h / mol/h)
                rn = self.newNSR/14 #(Secretion rate NH3 in gN/h / 14 g/mol)
                Ycn = round(rn/self.newCPR,4) #(mol/h / mol/h)
                
                #Check first Checkpoint
                counter = 0
                if Yco != student_answer_Yco:
                    counter += 1
                    print("Normalized Yield_co WRONG!\n")
                if Ycn != student_answer_Ycn:
                    counter += 1
                    print("Normalized Yield_cn WRONG!\n")

                       
                Ycs = round(sol_Ycs[0]*Ycc+sol_Ycs[1]*Yco+sol_Ycs[2]*Ycn,2) #(mol/cmol)
                Ycf = round(sol_Ycf[0]*Ycc+sol_Ycf[1]*Yco+sol_Ycf[2]*Ycn,2) #(mol/cmol)
                Ycp = round(sol_Ycp[0]*Ycc+sol_Ycp[1]*Yco+sol_Ycp[2]*Ycn,2) #(mol/cmol)
                

                Yxq = Ycs*round(mp*self.newCoP,2)+Ycf*round(mf*self.newCoF,2)+Ycp*round(mp*self.newCoP,2) #(mol/cmol * kcal/cmol) = (kcal/cmol) || units not clear, might need second look
                Rxq = round(Yxq * self.newCPR,2) # kcal/cmol * mol/h = kcal/h || units not clear, might need second look
                
                #Check second Checkpoint
                if Rxq != student_answer_Rxq:
                    counter += 1
                    print("Metabolic rate WRONG!\n")
                
                
                if counter != 0:
                    print('\n##########\nPLEASE TRY AGAIN!\n\n')
                    self.question_three_display.children[-1].clear_output(wait=True)
                elif counter == 0:
                    self.question_three_display.children[-3].children[0].disabled = True
                    self.question_three_display.children[-3].children[1].disabled = True
                    print("Solution corect!")
                    solcode = ""
                    #Help-option was not used
                    if self.hq3tgl == 0:
                        solcode+=(str(rd.randrange(0,4)))
                    #Help-option was used
                    elif self.hq3tgl == 1:
                        solcode+=(str(rd.randrange(5,9)))

                    if int(stdIDstr[-1])+int(stdIDstr[-2]) < 10:
                        solcode+=(str(rd.randrange(0,4)))
                        solcode+=(str(rd.randrange(0,4)))
                    elif int(stdIDstr[-1])+int(stdIDstr[-2]) >= 10:
                        solcode+=(str(rd.randrange(5,9)))
                        solcode+=(str(rd.randrange(5,9)))    
                    # PRINT THE CODE
                    print("Here's your code!\n\n"+solcode+"\n\nPlease upload it in the designated Moodle-Task.")
                

    ######
    # functions that create widgets
    #
    #
    #
    ###
    
    def build_question_one(self):
        listofwidgets = []
        
        # build question label/output (top 0)
        # build answer input YxqP(top 1)
        # build answer input YxqC(top 2)
        # build answer input YxqF(top 3)
        # build 'Check Answer button' (top 4.hbox-0)
        # build 'Get help button' (top 4. hbox-1)
        # build output (for commentsof help button) (top 5)
        # build output (for answer button feedback) (top 6)
        
        listofwidgets.append(widgets.Output(
        ))
        with listofwidgets[0]:
            #print("##########\n\nParameters for Question 1:\n\n"\
            #"Your glucose yield Y_(XS) is {} C-mol glucose/C-mol biomass\n\n"\
            #"Your biomass composition is CH_({})O_({})N_({})\n\n##########".format(self.newYxs,self.newH,self.newO,self.newN))
            print("")
        
        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='YxqP [kcal/mol]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))

        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='YxqC [kcal/mol]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))
        
        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='YxqF [kcal/mol]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))
        
        i = []
        i.append(widgets.Button(
            value=False,
            description='Check Solution',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to check solution',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
                             
        i.append(widgets.Button(
            value=False,
            description='Calculation Help',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to get a tipp',
        #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
        
        listofwidgets.append(widgets.HBox(i))
        
        listofwidgets.append(widgets.Output())
        listofwidgets.append(widgets.Output())
        
        disp = widgets.VBox(listofwidgets)
        return disp
###############
###############
###############
    def build_question_two(self):
            listofwidgets = []

            # build question label/output (top 0)
            # build answer format label for Ycs (top 1)
                #build answer input for Ycs answer {A} (top 2.hbox-0)
                #build answer input for Ycs answer {B} (top 2.hbox-1)
                #build answer input for Ycs answer {C} (top 2.hbox-2)
            # build answer input for Ycf (top 3)
                #build answer input for Ycf answer {A} (top 4.hbox-0)
                #build answer input for Ycf answer {B} (top 4.hbox-1)
                #build answer input for Ycf answer {C} (top 4.hbox-2)
            # build answer input for Ycn (top 5)
                #build answer input for Ycn answer {A} (top 6.hbox-0)
                #build answer input for Ycn answer {B} (top 6.hbox-1)
                #build answer input for Ycn answer {C} (top 6.hbox-2)
            # build 'Check Answer button' (top 7.hbox-0)
            # build 'Get help button' (top 7. hbox-1)
            # build output (for commentsof help button) (top 8)
            # build output (for answer button feedback) (top 9)

            listofwidgets.append(widgets.Output(
            ))
            with listofwidgets[0]:
                #print("##########\n\nParameters for Question 2:\n\n"\
                #"Your O_2 Exchange-Rate is {} mol/h\n\n"\
                #"Your CO_2 Exchange-Rate is {} mol/h\n\n##########".format(self.newRO2,self.newRCO2))
                print("")
            ###
            # Widgtes responsible for student input of Y_cs
            ###
            listofwidgets.append(widgets.Label(
                value="Yield Carbohydrates / Y_cs [mol/cmol]= {A} + {B}*Y_co + {C}*Y_cn",
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='500px', height='40px')
            ))
            lstOne = []
            lstOne.append(widgets.FloatText(
                value=0.0,
                description='A:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstOne.append(widgets.FloatText(
                value=0.0,
                description='B:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstOne.append(widgets.FloatText(
                value=0.0,
                description='C:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            listofwidgets.append(widgets.HBox(lstOne))

            ###
            # Widgtes responsible for student input of Y_cf
            ###
            listofwidgets.append(widgets.Label(
                value="Yield Fats / Y_cf [mol/cmol]= {A} + {B}*Y_co + {C}*Y_cn",
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='500px', height='40px')
            ))
            lstTwo = []
            lstTwo.append(widgets.FloatText(
                value=0.0,
                description='A:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstTwo.append(widgets.FloatText(
                value=0.0,
                description='B:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstTwo.append(widgets.FloatText(
                value=0.0,
                description='C:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            listofwidgets.append(widgets.HBox(lstTwo))
            
            ###
            # Widgtes responsible for student input of Y_cp
            ###
            listofwidgets.append(widgets.Label(
                value="Yield Protein / Y_cp [mol/cmol]= {A} + {B}*Y_co + {C}*Y_cn",
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='500px', height='40px')
            ))
            lstThree = []
            lstThree.append(widgets.FloatText(
                value=0.0,
                description='A:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstThree.append(widgets.FloatText(
                value=0.0,
                description='B:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstThree.append(widgets.FloatText(
                value=0.0,
                description='C:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            listofwidgets.append(widgets.HBox(lstThree))
            
            
            ###
            # Wisgets resonsible for Solution check and help button
            #
            i = []
            i.append(widgets.Button(
                value=False,
                description='Check Yields',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Click to check solution',
                #     icon='check' # (FontAwesome names without the `fa-` prefix)
            ))

            i.append(widgets.Button(
                value=False,
                description='Calculation Help',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Click to get a tipp',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
            ))

            listofwidgets.append(widgets.HBox(i))

            listofwidgets.append(widgets.Output())
            listofwidgets.append(widgets.Output())

            disp = widgets.VBox(listofwidgets)
            return disp
        
###############
###############
###############        
    def build_question_three(self):
        listofwidgets = []
        
        # build question label/output (top 0)
        # build answer input Yco(top 1)
        # build answer input Ycn(top 2)
        # build answer input Rxq(top 3)
        # build 'Check Answer button' (top 4.hbox-0)
        # build 'Get help button' (top 4. hbox-1)
        # build output (for commentsof help button) (top 5)
        # build output (for answer button feedback) (top 6)
        
        listofwidgets.append(widgets.Output(
        ))
        with listofwidgets[0]:
            #print("##########\n\nParameters for Question 1:\n\n"\
            #"Your glucose yield Y_(XS) is {} C-mol glucose/C-mol biomass\n\n"\
            #"Your biomass composition is CH_({})O_({})N_({})\n\n##########".format(self.newYxs,self.newH,self.newO,self.newN))
            print("")
        
        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='Yco [mol/cmol]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))

        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='Ycn [mol/cmol]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))
        
        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='Rxq [kcal/h]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))
        
        i = []
        i.append(widgets.Button(
            value=False,
            description='Check Solution',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to check solution',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
                             
        i.append(widgets.Button(
            value=False,
            description='Calculation Help',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to get a tipp',
        #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
        
        listofwidgets.append(widgets.HBox(i))
        
        listofwidgets.append(widgets.Output())
        listofwidgets.append(widgets.Output())
        
        disp = widgets.VBox(listofwidgets)
        return disp
    
    ######
    # ON-CLICK functions
    # 2 per question
    #
    #
    ###
    def on_question_one_help_button_clicked(self, click):
        self.hq1tgl = 1
        self.question_one_display.children[-3].children[1].disabled = True
        with self.question_one_display.children[-2]:
            txt = "##########\n" \
            "Given are the estimated heat of combustions in (kcal/g) and\nthe chemical composition.\n\n" \
            "* Sum up the approximate weight of each subgroup in g/cmol\n\n" \
            "* Multiply the 'heat of combustion' (kcal/g) with the 'molecular weight' (g/mol)\n" \
            "##########"
            print(txt)
    def on_question_one_answer_button_clicked(self, click):
        student_YxqP = self.question_one_display.children[1].value
        student_YxqC = self.question_one_display.children[2].value
        student_YxqF = self.question_one_display.children[3].value
        self.correct_homework_four_question_one(student_YxqP, student_YxqC, student_YxqF)
        
    def on_question_two_help_button_clicked(self, click):
        self.hq2tgl = 1
        self.question_two_display.children[-3].children[1].disabled = True
        with self.question_two_display.children[-2]:
            txt = "##########\n" \
            "PLACEHOLDER!\n" \
            "##########\n"
            print(txt)
            
    def on_question_two_answer_button_clicked(self, click):
        student_answer_Ycs = []
        student_answer_Ycf = []
        student_answer_Ycp = []
        for i in self.question_two_display.children[2].children:
            student_answer_Ycs.append(i.value)
        for i in self.question_two_display.children[4].children:
            student_answer_Ycf.append(i.value)
        for i in self.question_two_display.children[6].children:
            student_answer_Ycp.append(i.value)
        self.correct_homework_four_question_two(student_answer_Ycs, student_answer_Ycf, student_answer_Ycp)
        
    #def on_question_two_reset_button_clicked(self, click):
    #    #A button that, when clicked resets the value fo the input frlds to the original format, thus showing how the input has to look like
    #    self.question_two_display.children[1].value = "{A} + {B}*Y_co + {C}*Y_cn" #input for Ycs (top 1)
    #    self.question_two_display.children[2].value = "{A} + {B}*Y_co + {C}*Y_cn" #input for Ycf (top 1)
    #    self.question_two_display.children[3].value = "{A} + {B}*Y_co + {C}*Y_cn" #input for Ycn (top 1)
    #    with self.question_two_display.children[-1]:
    #        print("#####\nInput-Fields RESET\n#####")
    #        self.question_two_display.children[-1].clear_output(wait=True)
    
    def on_question_three_answer_button_clicked(self, click):
        student_Yco = self.question_three_display.children[1].value
        student_Ycn = self.question_three_display.children[2].value
        student_Rxq = self.question_three_display.children[3].value
        self.correct_homework_four_question_three(student_Yco, student_Ycn, student_Rxq)
    
    def on_question_three_help_button_clicked(self, click):
        self.hq3tgl = 1
        self.question_three_display.children[-3].children[1].disabled = True
        with self.question_three_display.children[-2]:
            txt = "##########\n" \
            "PLACEHOLDER!\n" \
            "##########\n"
            print(txt)