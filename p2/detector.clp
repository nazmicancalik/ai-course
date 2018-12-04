; Initializes the multiplication result for each patient and illness
(defrule init-divident
        (illness ?illness_name ?illness_prob)
        (patient-said ?patient_id ? ?)
        =>
        (assert(divident ?illness_name ?patient_id ?illness_prob))
)

; For all (symptomp,illness) combination get the values P(S) = P(S|H)P(H) + P(S|-H)P(-H)
(defrule init-ps
        (illness ?illness_name ?illness_prob)
        (symptom ?symptom_id ?illness_name ?yes_prob ?no_prob)
        =>
        (assert (ps ?symptom_id ?illness_name (+ (* ?yes_prob ?illness_prob) (* ?no_prob (- 1 ?illness_prob)))))
)

; Finds inverse ps. 
(defrule not-ps
        (ps ?symptom_id ?illness_name ?ps)
        =>
        (assert (inverse-ps ?symptom_id ?illness_name (- 1 ?ps)))
)

;Initializes person list
(defrule init-person
        (patient-said ?patient_id ? ?)
        =>
        (assert (person ?patient_id))
)

; Finds s's for each person
(defrule init-divisor
        (patient-said ?patient_id ? ?)
        =>
        (assert (divisor ?patient_id 1))
)

;Calculates the divisor part
(defrule calculate-divisor
        ?toDeletePatient <- (patient-said ?patient_id ?symptom_id ?answer)
        ?toDeletePs <-(ps ?symptom_id ?illness_name ?ps_yes)
        ?toDeleteInversePs <-(inverse-ps ?symptom_id ?illness_name ?ps_no)
        ?oldResult <- (divisor ?patient_id ?oldValue) 
        =>
        (retract ?toDeletePatient)
        (retract ?toDeletePs) 
        (retract ?toDeleteInversePs)
        (assert (patient ?patient_id ?symptom_id ?answer) (ps_1 ?symptom_id ?illness_name ?ps_yes) (inverse-ps_1 ?symptom_id ?illness_name ?ps_no))
        (if (eq ?answer yes)
                then 
                        (retract ?oldResult)
                        (assert (divisor  ?patient_id (* ?oldValue ?ps_yes)))
                else 
                        (retract ?oldResult)
                        (assert (divisor ?patient_id (* ?oldValue ?ps_no)))
        )
)

;Calculates the divident part
(defrule calculate-divident
        ?toDeletePatient <- (patient ?patient_id ?symptom_id ?answer)
        ?toDeletePs <-(ps_1 ?symptom_id ?illness_name ?ps_yes)
        ?toDeleteInversePs <-(inverse-ps_1 ?symptom_id ?illness_name ?ps_no)
        ?oldResult <- (divident ?illness_name ?patient_id ?oldValue) 
        =>
        (retract ?toDeletePatient)
        (retract ?toDeletePs) 
        (retract ?toDeleteInversePs)
        (assert (patient-said_1 ?patient_id ?symptom_id ?answer))
        (if (eq ?answer yes)
                then 
                        (retract ?oldResult)
                        (assert (divident  ?illness_name ?patient_id (* ?oldValue ?ps_yes)))
                else 
                        (retract ?oldResult)
                        (assert (divident  ?illness_name ?patient_id (* ?oldValue ?ps_no)))
        )
)

; Division operation
(defrule divide
        ?toDeleteDivident <- (divident ?illness_name ?patient_id ?divident_value)
        ?toDeleteDivisor <- (divisor  ?patient_id ?divisor_value)
        =>
        (assert (result ?patient_id ?illness_name (/ ?divident_value ?divisor_value)))
)

; Init the values that are going to hold the max probable illness for all patients
(defrule init-most-probable
        (person ?patient_id)
        =>
        (assert (most-probable-illness-for-patient ?patient_id null 0))
)

; Find the maximum result for each patient.
(defrule calculate
        ?toDeleteResult <- (result ?patient_id ?illness_name ?prob)
        ?toDeleteMostProbable <- (most-probable-illness-for-patient ?patient_id ?illness_name ?oldProb)
        =>
        (retract ?toDeleteResult)
        (if (< ?oldProb ?prob)
                then 
                        (retract ?toDeleteMostProbable)
                        (assert (most-probable-illness-for-patient ?patient_id ?illness_name ?prob))
        )
)