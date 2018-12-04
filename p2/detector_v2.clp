; Initializes the multiplication result for each patient and illness
; X is the value with P(S1|H)P(S2|H)P(S3|H)P(H)
(defrule init-x
        (illness ?illness_name ?illness_prob)
        (patient-said ?patient_id ? ?)
        =>
        (assert(x ?illness_name ?patient_id ?illness_prob))
)

; X is the value with P(S1|-H)P(S2|-H)P(S3|-H)P(-H)
(defrule init-y
        (illness ?illness_name ?illness_prob)
        (patient-said ?patient_id ? ?)
        =>
        (assert (y ?illness_name ?patient_id (- 1 ?illness_prob)))
)

;Calculates the divident part
(defrule calculate-x
        ?toDeletePatient <- (patient-said ?patient_id ?symptom_id ?answer)
        ?toDeleteSymptomp <-(symptom ?symptom_id ?illness_name ?ps_yes_when_ill ?ps_yes_when_not_ill)
        ?oldResult <- (x ?illness_name ?patient_id ?oldValue) 
        =>
        (retract ?toDeletePatient)
        (retract ?toDeleteSymptomp) 
        (assert (patient-said_1 ?patient_id ?symptom_id ?answer))
        (assert (symptom_1 ?symptom_id ?illness_name ?ps_yes_when_ill ?ps_yes_when_not_ill))
        (if (eq ?answer yes)
                then 
                        (retract ?oldResult)
                        (assert (x  ?illness_name ?patient_id (* ?oldValue ?ps_yes_when_ill)))
                else 
                        (retract ?oldResult)
                        (assert (x  ?illness_name ?patient_id (* ?oldValue (- 1 ?ps_yes_when_ill))))
        )
)

;Calculates the divident part
(defrule calculate-y
        ?toDeletePatient_1 <- (patient-said_1 ?patient_id ?symptom_id ?answer)
        ?toDeleteSymptomp_1 <-(symptom_1 ?symptom_id ?illness_name ?ps_yes_when_ill ?ps_yes_when_not_ill)
        ?oldResult <- (x ?illness_name ?patient_id ?oldValue) 
        =>
        (retract ?toDeletePatient_1)
        (retract ?toDeleteSymptomp_1) 
        (assert (patient-said_2 ?patient_id ?symptom_id ?answer))
        (assert (symptom_2 ?symptom_id ?illness_name ?ps_yes_when_ill ?ps_yes_when_not_ill))
        (if (eq ?answer yes)
                then 
                        (retract ?oldResult)
                        (assert (y  ?illness_name ?patient_id (* ?oldValue ?ps_yes_when_not_ill)))
                else 
                        (retract ?oldResult)
                        (assert (y  ?illness_name ?patient_id (* ?oldValue (- 1 ?ps_yes_when_not_ill))))
        )
)

; Init the divisor value
(defrule init-divisor
        (x ?illness_name ?patient_id ?probx)
        (y ?illness_name ?patient_id ?proby)
        =>
        (assert (divisor ?illness_name ?patient_id (+ ?probx ?proby)))
)

; Division operation
(defrule divide
        ?toDeleteDivident <- (x ?illness_name ?patient_id ?divident_value)
        ?toDeleteDivisor <- (y ?illness_name ?patient_id ?divisor_value)
        =>
        (retract ?toDeleteDivident ?toDeleteDivisor)
        (if (eq ?divisor 0)
                then 
                (assert (result ?patient_id ?illness_name (/ ?divident_value ?divisor_value)))
                else
                (assert (result ?patient_id ?illness_name -1))
        )       
)