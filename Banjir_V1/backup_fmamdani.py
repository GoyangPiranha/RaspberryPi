import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control.term import Term, WeightedTerm, TermAggregate

# New Antecedent/Consequent objects hold universe variables and membership # functions 
x_ketinggian = ctrl.Antecedent(np.arange(0, 120, 1), 'ketinggian')
x_kecepatan = ctrl.Antecedent(np.arange(0, 100, 1), 'kecepatan') 
x_status = ctrl.Consequent(np.arange(0, 120, 1), 'status')

# Custom membership functions can be built interactively with a familiar, # Pythonic API 
x_ketinggian['rendah'] = fuzz.trapmf(x_ketinggian.universe, [0, 0, 50, 75]) 
x_ketinggian['sedang'] = fuzz.trimf(x_ketinggian.universe, [50, 75, 100]) 
x_ketinggian['tinggi'] = fuzz.trapmf(x_ketinggian.universe, [75, 100, 120, 120])

x_kecepatan['lamban'] = fuzz.trapmf(x_kecepatan.universe, [0, 0, 25, 50]) 
x_kecepatan['sedang'] = fuzz.trimf(x_kecepatan.universe, [25, 50, 75]) 
x_kecepatan['cepat'] = fuzz.trapmf(x_kecepatan.universe, [50, 75, 100, 100])

x_status['aman'] = fuzz.trapmf(x_status.universe, [0, 0, 50, 75]) 
x_status['siaga'] = fuzz.trimf(x_status.universe, [50, 75, 100]) 
x_status['bahaya'] = fuzz.trapmf(x_status.universe, [75, 100, 120, 120])

# You can see how these look with .view()
#x_ketinggian.view()

#x_kecepatan.view()

#x_status.view()

rule1 = ctrl.Rule(x_ketinggian['rendah'] & x_kecepatan['lamban'], x_status['aman'])
rule2 = ctrl.Rule(x_ketinggian['rendah'] & x_kecepatan['sedang'], x_status['aman'])
rule3 = ctrl.Rule(x_ketinggian['rendah'] & x_kecepatan['cepat'], x_status['siaga'])

rule4 = ctrl.Rule(x_ketinggian['sedang'] & x_kecepatan['lamban'], x_status['siaga'])
rule5 = ctrl.Rule(x_ketinggian['sedang'] & x_kecepatan['sedang'], x_status['siaga'])
rule6 = ctrl.Rule(x_ketinggian['sedang'] & x_kecepatan['cepat'], x_status['bahaya'])

rule7 = ctrl.Rule(x_ketinggian['tinggi'] & x_kecepatan['lamban'], x_status['bahaya'])
rule8 = ctrl.Rule(x_ketinggian['tinggi'] & x_kecepatan['sedang'], x_status['bahaya'])
rule9 = ctrl.Rule(x_ketinggian['tinggi'] & x_kecepatan['cepat'], x_status['bahaya'])

status_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

status = ctrl.ControlSystemSimulation(status_ctrl)

status.input['ketinggian'] = 60
status.input['kecepatan'] = 40

# Crunch the numbers
status.compute()
#status.print_state()

a = max(status.output, key=status.output.get)
print("Nilai Status : {0}".format(status.output_status['status']))
print("Status : {0}".format(a))

#x_status.view(sim=status)

