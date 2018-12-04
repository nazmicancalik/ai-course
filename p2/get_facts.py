ILLNESS_FILENAME = "ILLNESS.txt"
SYMPTOMPS_FILENAME = "SYMPTOMPS.txt"
INPUT_FILENAME = "INPUTS.txt"

class Illness:
    def __init__(self,name,prob):
        self.name = name
        self.prob = prob
        self.symptoms = []

    def __str__(self):
        return str(self.name)

class Symptom:
    def __init__(self,index,probTrue,probFalse):
        self.index = index
        self.probTrue = probTrue
        self.probFalse = probFalse


def main():
    illnesses = [line.rstrip('\n') for line in open(ILLNESS_FILENAME)]
     
   
    splitted_lines = []
    for line in illnesses:
        splitted_lines.append(line.split(','))

    final_illnesses = []
    for illness in splitted_lines:
        new_illness = Illness(illness[0],illness[1])
        # Add the symptoms to the illness.
        i = 2
        print illness[0]
        while (True):
            index = illness[i]
            if index == str(999):
                break
            new_illness.symptoms.append(Symptom(index,illness[i+1],illness[i+2]))
            i = i+3
        final_illnesses.append(new_illness)

    # Now print to the file.
    kb_file = open('./kb.clp', 'w+')
    for el in final_illnesses:
        kb_file.write('(assert (illness "' + str(el.name) + '" ' + str(el.prob) + '))\n')
        for s in el.symptoms:
            kb_file.write('(assert (symptom ' + str(s.index) + ' "' + str(el.name) + '" ' + str(s.probTrue) + ' ' + str(s.probFalse) +'))\n')
    
    '''
    # INPUTS
    inputs = [line.rstrip('\n') for line in open(INPUT_FILENAME)]
    splitted_inputs = []
    for line in inputs:
        splitted_inputs.append(line.split(','))

    # Write to the knowledge base now.
    for el in splitted_inputs:
        kb_file.write('(assert (patient ' + str(el[0]) + ' ')
        for i,item in enumerate(el):
            if i == 0:
                continue
            kb_file.write(item + ' ')
        kb_file.write('))\n')
    kb_file.close()
    '''

    inputs = [line.rstrip('\n') for line in open(INPUT_FILENAME)]
    splitted_inputs = []
    for line in inputs:
        splitted_inputs.append(line.split(','))

    # Write to the knowledge base now.
    for el in splitted_inputs:
        for i,item in enumerate(el):
            if i == 0:
                continue
            for illness in splitted_lines:
                kb_file.write('(assert (patient-said ' + str(el[0]) + ' ' + str(i) + ' ' + str(item) + ' "' + illness[0] +'"))\n')
    kb_file.close()

if __name__ == "__main__":
    main()