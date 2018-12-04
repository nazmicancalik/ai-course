; Initializes the multiplication result for each patient and illness
(defrule initialize-probabilities
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

(defrule
        (ps ?symptom_id ?illness_name ?ps)
        =>
        (assert ())
)


; Tries to find the divident parts 
; YES_RESULT = P(S1|H)P(S2|H)P(S3|H)...
; NO_RESULT = P(S1|-H)P(S2|-H)P(S3|-H)...

(defrule get-divident-part
        (illness ?illness_name ?illness_prob)
        ?symptom_fact <- (symptom ?symptom_id ?illness_name ?yes_prob ?no_prob)
        ?patient <- (patient-said ?patient_id ?symptom_id ?answer)
        ?multiplication_divident_result <- (divident-part ?illness_name ?patient_id ?multiplication_result)
        =>
        (assert (divident-part-yes ?illness_name ?patient_id (* ?yes_prob ?multiplication_result)))
        (retract ?multiplication_divident_result)
)

(defrule get-final-prob
        (divident-part ?illness_name ?patient_id ?final_yes_prob)
        =>
        (assert (patient_illness_probability (* ?final_yes_prob ?final_no_prob)))
)

; GETS THE MAX POSSIBLE ILLNESS FOR PATIENTS
;(defrule get-max-prob )