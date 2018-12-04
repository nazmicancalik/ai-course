; Initializes the multiplication result for each patient and illness
(defrule initialize-divident
        (illness ?illness_name ?illness_prob)
        (patient-said ?patient_id ? ?)
        =>
        (assert(divident-part ?illness_name ?patient_id ?illness_prob))
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
        (retract ?toDeletePatient ?toDeletePs ?toDeleteInversePs)
        (assert (patient ?patient_id ?symptom_id ?answer) (ps_1 ?symptom_id ?illness_name ?ps_yes) (inverse-ps_1 ?symptom_id ?illness_name ?ps_no))
        (printout t ?patient_id crlf)
        (if (eq ?answer yes)
                then 
                        (retract ?oldResult)
                        (printout t "yes" crlf)
                        (assert (divisor ?patient_id (* ?oldValue ?ps_yes)))
                else 
                        (retract ?oldResult)
                        (printout t "no" crlf)
                        (assert (divisor ?patient_id (* ?oldValue ?ps_no)))
        )
)