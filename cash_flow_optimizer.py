class CashFlowOptimizer:
    def __init__(self):
        self.overall_cash_flow = 0.0
        self.surplus = {'Cash Receipt': -1, 'Asset Sale': -1, 'Loan Share Issue': -1}
        self.deficit = {'Cash Payment': -1, 'Asset Purchase': -1, 'Loan Repayment': -1}
        self.state = 'q0'  # Initial state

        self.transition_table = {
            'q0': {'Inflow': ['q1'], 'Outflow': ['q2']},
            'q1': {'Inflow': ['q3'], 'Outflow': ['q1', 'q2']}, 
            'q2': {'Inflow': ['q3', 'q5'], 'Outflow': ['q2']},
            'q3': {'Inflow': ['q5'], 'Outflow': ['q3', 'q4']},
            'q4': {'Inflow': ['q1', 'q5'], 'Outflow': ['q4']},
            'q5': {'Inflow': ['q7'], 'Outflow': ['q5', 'q6']},
            'q6': {'Inflow': ['q1', 'q3'], 'Outflow': ['q6']},
            'q7': {'Inflow': ['q7'], 'Outflow': []},
        }

    def fill_surplus(self, item):
        if item == 'Cash Receipt':
            self.surplus['Cash Receipt'] = float(input("Enter Cash Receipt (CFO +): "))
        elif item == 'Asset Sale':
            self.surplus['Asset Sale'] = float(input("Enter Asset Sale (CFI +): "))
        elif item == 'Loan Share Issue':
            self.surplus['Loan Share Issue'] = float(input("Enter Loan Share Issue (CFF +): "))
        self.overall_cash_flow += self.surplus.get(item, 0)

    def fill_deficit(self, item):
        if item == 'Cash Payment':
            self.deficit['Cash Payment'] = float(input("Enter Cash Payment (CFO -): "))
        elif item == 'Asset Purchase':
            self.deficit['Asset Purchase'] = float(input("Enter Asset Purchase (CFI -): "))
        elif item == 'Loan Repayment':
            self.deficit['Loan Repayment'] = float(input("Enter Loan Repayment (CFF -): "))
        self.overall_cash_flow -= self.deficit.get(item, 0)

    def resetting_surplus(self, item):
        self.overall_cash_flow -= self.surplus.get(item, 0)  # Reset surplus
        self.surplus[item] = -1

    def resetting_deficit(self, item):
        self.overall_cash_flow += self.deficit.get(item, 0)  # Reset deficit
        self.deficit[item] = -1

    def cash_flow_loop(self):
        while self.state not in ['q7']:  # Loop until reaching final state
            print(f"\nCurrent State: {self.state}")

            if self.state == 'q0':
                while True:
                    choice = input("Enter 'CR' for Cash Receipt (CFO), 'CP' for Cash Payment (CFO): ").strip().upper()
                    if choice == 'CR':
                        self.fill_surplus('Cash Receipt')

                        if self.overall_cash_flow >= 0:
                            self.state = self.transition_table[self.state]['Inflow'][0]  # Transition to q1
                            if self.deficit['Cash Payment'] == -1:
                                self.fill_deficit('Cash Payment')
                        break
                    elif choice == 'CP':
                        self.fill_deficit('Cash Payment')
                        if self.overall_cash_flow >= 0:
                            self.state = self.transition_table[self.state]['Outflow'][0]  # Transition to q2
                        break
                    else:
                        print("Choices are 'CR' and 'CP' only")

            elif self.state == 'q1':
                if self.deficit['Cash Payment'] == -1:
                    self.fill_deficit('Cash Payment')

                if self.overall_cash_flow >= 0:
                    if self.surplus['Asset Sale'] == -1:
                        self.fill_surplus('Asset Sale')
                    self.state = self.transition_table[self.state]['Inflow'][0]  # Transition to q3
                else:
                    print("An outflow. Do you want to modify Cash Payment?")
                    choice = input("Enter 'Y' for Yes, 'N' for No: ").strip().upper()
                    while True: 
                        if choice == 'Y':
                            # Resetting Cash Payment back to -1, self loop to modify Cash Payment
                            self.resetting_deficit('Cash Payment')
                            self.state = self.transition_table[self.state]['Outflow'][0]  # Transition back to q1
                            break
                        elif choice == 'N':
                            self.state = self.transition_table[self.state]['Outflow'][1]  # Transition to q2
                            break
                        else:
                            print("Choices are Y and N only")  

            elif self.state == 'q2':
                while True: 
                    choice = input("Enter 'A' for Asset Sale (CFI), 'LS' for Loan Share Issue (CFF): ").strip().upper()
                    if choice == 'A':
                        self.fill_surplus('Asset Sale')  
                        if self.overall_cash_flow >= 0:
                            print("Yey! CFO Deficit Recovered with CFI Inflow.")
                            self.state = self.transition_table[self.state]['Inflow'][0]  # Transition to q3
                        else:
                            print("Still in deficit after Asset Sale. Try again")
                            self.resetting_surplus('Asset Sale')
                            self.state = self.transition_table[self.state]['Outflow'][0]  # Transition still at q2 
                        break
                    elif choice == 'LS':
                        self.fill_surplus('Loan Share Issue')
                        if self.overall_cash_flow >= 0:
                            print("Yey! CFO Deficit Recovered with CFF Inflow.")
                            self.state = self.transition_table[self.state]['Inflow'][1]  # Transition to q5
                        else:
                            print("Still in deficit after Loan Share Issue. Try again")
                            self.resetting_surplus('Loan Share Issue')
                            self.state = self.transition_table[self.state]['Outflow'][0]  # Transition still at q2  
                        break
                    else:
                        print("Choices are A and LS only")

            elif self.state == 'q3':
                if self.deficit['Asset Purchase'] == -1:
                    self.fill_deficit('Asset Purchase')

                if self.overall_cash_flow >= 0:
                    if self.surplus['Loan Share Issue'] == -1:
                        self.fill_surplus('Loan Share Issue')
                    self.state = self.transition_table[self.state]['Inflow'][0]  # Transition to q5 
                else:
                    print("An outflow. Do you want to modify Asset Purchase?")
                    choice = input("Enter 'Y' for Yes, 'N' for No: ").strip().upper()
                    while True: 
                        if choice == 'Y':
                            self.resetting_deficit('Asset Purchase')
                            self.state = self.transition_table[self.state]['Outflow'][0]  # Transition back to itself, q3
                            break
                        elif choice == 'N':
                            self.state = self.transition_table[self.state]['Outflow'][1]  # Transition to q4
                            break
                        else:
                            print("Choices are Y and N only")

            elif self.state == 'q4':  # CFI Deficit
                while True: 
                    choice = input("Enter 'CR' for Cash Receipt Modification (CFO), 'LS' for Loan Share Issue (CFF): ").strip().upper()
                    if choice == 'CR':
                        self.resetting_surplus('Cash Receipt')
                        self.fill_surplus('Cash Receipt') 

                        if self.overall_cash_flow >= 0:
                            print("Yey! CFI Deficit Recovered with CFO Inflow.")
                            self.state = self.transition_table[self.state]['Inflow'][0]  # Transition to q1
                        else:
                            print("Still in deficit after modifying Cash Receipt. Try again")
                            self.resetting_surplus('Cash Receipt')
                            self.state = self.transition_table[self.state]['Outflow'][0]  # Transition still at q4 
                        break
                    elif choice == 'LS':
                        if self.surplus['Loan Share Issue']==-1:
                            self.fill_surplus('Loan Share Issue')
                        else:
                            choice2 = input("Want to modify Loan Share? 'Y' for Yes and 'N' for No: ")
                            while True:
                                if choice2 == 'Y':
                                    self.resetting_surplus('Loan Share Issue')
                                    self.fill_surplus('Loan Share Issue') 
                                elif choice2 == 'N':
                                    self.state = self.transition_table[self.state]['Outflow'][0]  # Transition still at q4 
                                    break
                                else:
                                    print("Choices are Y and N only")
                        if self.overall_cash_flow >= 0:
                            print("Yey! CFI Deficit Recovered with CFF Inflow.")
                            self.state = self.transition_table[self.state]['Inflow'][1]  # Transition to q5
                        else:
                            print("Still in deficit after Loan Share Issue. Try again")
                            self.resetting_surplus('Loan Share Issue')
                            self.state = self.transition_table[self.state]['Outflow'][0]  # Transition still at q4
                        break 
                    else:
                        print("Choices are CR and LS only")

            elif self.state == 'q5':  # CFF Surplus
                if self.deficit['Loan Repayment'] == -1:
                    self.fill_deficit('Loan Repayment')

                if self.overall_cash_flow >= 0:
                    print("\nFinal State Reached! Your Cash Flow Statement is ready:")
                    self.state = self.transition_table[self.state]['Inflow'][0]  # Transition to q7
                    return self.overall_cash_flow
                else:
                    print("An outflow. Do you want to modify Loan Repayment?")
                    choice = input("Enter 'Y' for Yes, 'N' for No: ").strip().upper()
                    while True: 
                        if choice == 'Y':
                            self.resetting_deficit('Loan Repayment')
                            self.state = self.transition_table[self.state]['Outflow'][0]  # Transition back to itself q5
                            break
                        elif choice == 'N':
                            self.state = self.transition_table[self.state]['Outflow'][1]  # Transition to q6
                            break
                        else:
                            print("Choices are Y and N only")    

            elif self.state == 'q6':  # CFF Deficit
                while True: 
                    choice = input("Enter 'CR' for Cash Receipt Modification (CFO), 'AS' for Asset Sale (CFI): ").strip().upper()
                    if choice == 'CR':
                        self.resetting_surplus('Cash Receipt')
                        self.fill_surplus('Cash Receipt') 

                        if self.overall_cash_flow >= 0:
                            print("Yey! CFF Deficit Recovered with CFO Inflow.")
                            self.state = self.transition_table[self.state]['Inflow'][0]  # Transition to q1
                        else:
                            print("Still in deficit after modifying Cash Receipt. Try again")
                            self.resetting_surplus('Cash Receipt')
                            self.state = self.transition_table[self.state]['Outflow'][0]  # Transition still at q6
                        break
                    elif choice == 'AS':
                        if self.surplus['Asset Sale']==-1:
                            self.fill_surplus('Asset Sale')
                        else:
                            choice2 = input("Want to modify Asset Sale? 'Y' for Yes and 'N' for No: ")
                            while True:
                                if choice2 == 'Y':
                                    self.resetting_surplus('Asset Sale')
                                    self.fill_surplus('Asset Sale') 
                                elif choice2 == 'N':
                                    self.state = self.transition_table[self.state]['Outflow'][0]  # Transition still at q6
                                    break
                                else:
                                    print("Choices are Y and N only")
                        if self.overall_cash_flow >= 0:
                            print("Yey! CFF Deficit Recovered with CFI Inflow.")
                            self.state = self.transition_table[self.state]['Inflow'][1]  # Transition to q3
                        else:
                            print("Still in deficit after Asset Sale Issue. Try again")
                            self.resetting_surplus('Asset Sale')
                            self.state = self.transition_table[self.state]['Outflow'][0]  # Transition still at q6
                        break 
                    else:
                        print("Choices are CR and LS only")

            elif self.state == 'q7':  # Final State
                print("\nFinal State Reached! Your Cash Flow Statement is ready:")
                return

            else:
                print("State not applicable. Try again")
