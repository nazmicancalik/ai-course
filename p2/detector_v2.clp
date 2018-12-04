; Initializes the multiplication result for each patient and illness
(defrule init-result
        (illness ?illness_name ?illness_prob)
        (patient-said ?patient_id ? ? ?)
        =>
        (assert (result ?patient_id ?illness_name -10))
)

; X is the value with P(S1|H)P(S2|H)P(S3|H)P(H)
(defrule init-x
        (illness ?illness_name ?illness_prob)
        (patient-said ?patient_id ? ? ?)
        =>
        (assert (x ?illness_name ?patient_id ?illness_prob))
)

; Y is the value with P(S1|-H)P(S2|-H)P(S3|-H)P(-H)
(defrule init-y
        (illness ?illness_name ?illness_prob)
        (patient-said ?patient_id ? ? ?)
        =>
        (assert (y ?illness_name ?patient_id (- 1 ?illness_prob)))
)

;Calculates the divident part
(defrule calculate
        ?toDeletePatient <- (patient-said ?patient_id ?symptom_id ?answer ?illness_name)
        (symptom ?symptom_id ?illness_name ?ps_yes_when_ill ?ps_yes_when_not_ill)
        ?oldResultX <- (x ?illness_name ?patient_id ?oldValueX) 
        ?oldResultY <- (y ?illness_name ?patient_id ?oldValueY) 
        =>
        (retract ?toDeletePatient)
        (assert (y-value-changed ?person_id ?illness_name))
        (if (eq ?answer yes)
                then 
                        (retract ?oldResultX)
                        (retract ?oldResultY)
                        (assert (x  ?illness_name ?patient_id (* ?oldValueX ?ps_yes_when_ill)))
                        (assert (y  ?illness_name ?patient_id (* ?oldValueY ?ps_yes_when_not_ill)))
                else 
                        (retract ?oldResultX)
                        (retract ?oldResultY)
                        (assert (x  ?illness_name ?patient_id (* ?oldValueX (- 1 ?ps_yes_when_ill))))
                        (assert (y  ?illness_name ?patient_id (* ?oldValueY (- 1 ?ps_yes_when_not_ill))))
        )
)

; Division operation
(defrule divide
        ?toDeleteDivident <- (x ?illness_name ?patient_id ?x_value)
        ?toDeleteY <- (y ?illness_name ?patient_id ?y_value)
        ?toDeleteResult <- (result ?illness_name ?patient_id ?)
        ?toDeleteChanged <- (y-value-changed ?person_id ?illness_name)
        =>
        (retract ?toDeleteChanged)
        (retract ?toDeleteResult)
        (if (> (+ ?x_value ?y_value) 0)
                then 
                (assert (result ?patient_id ?illness_name (/ ?x_value (+ ?x_value ?y_value))))
                else
                (assert (result ?patient_id ?illness_name -1))
        )       
)