
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Instance file automatically generated by the Tarski FSTRIPS writer
;;; 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (problem instance1)
    (:domain test_domain)

    (:objects
        
    )

    (:init
        (= (total-cost ) 0)
        (has_police_car_number_substation )
        (has_police_car_number_courtstation )
        (has_police_car_number_apachestation )
        (has_ambulances_number_joseph )
        (has_ambulances_number_lukes )
        (has_rescuers_number_phxfire )
        (has_helicopters_number_phxfire )
        (has_bulldozers_number_phxfire )
        (has_ladders_number_phxfire )
        (has_rescuers_number_scottsfire )
        (has_bulldozers_number_scottsfire )
        (has_ladders_number_scottsfire )
        (has_small_engines_number_scottsfire )
        (has_rescuers_number_mesafire )
        (has_ladders_number_mesafire )
        (has_big_engines_number_mesafire )
        (has_rescuers_number_adminfire )
        (has_helicopters_number_adminfire )
        (has_bulldozers_number_adminfire )
        (has_ladders_number_adminfire )
        (has_small_engines_number_adminfire )
        (not_needed_address_media )
        (not_needed_active_local_alert_transportchief )
        (not_needed_active_local_alert_firechief )
        (not_needed_diverted_traffic_byeng_byeng )
        (not_needed_diverted_traffic_byeng_rural )
        (not_needed_diverted_traffic_byeng_marketplace )
        (not_needed_diverted_traffic_byeng_mill )
        (not_needed_diverted_traffic_byeng_lake )
        (not_needed_attend_casualties_byeng )
        (not_needed_search_casualties_byeng )
        (not_needed_diverted_traffic_rural_byeng )
        (not_needed_diverted_traffic_rural_rural )
        (not_needed_diverted_traffic_rural_marketplace )
        (not_needed_diverted_traffic_rural_mill )
        (not_needed_diverted_traffic_rural_lake )
        (not_needed_diverted_traffic_marketplace_byeng )
        (not_needed_diverted_traffic_marketplace_rural )
        (not_needed_diverted_traffic_marketplace_marketplace )
        (not_needed_diverted_traffic_marketplace_mill )
        (not_needed_diverted_traffic_marketplace_lake )
        (not_needed_diverted_traffic_mill_byeng )
        (not_needed_diverted_traffic_mill_rural )
        (not_needed_diverted_traffic_mill_marketplace )
        (not_needed_diverted_traffic_mill_mill )
        (not_needed_diverted_traffic_mill_lake )
        (not_needed_diverted_traffic_lake_byeng )
        (not_needed_diverted_traffic_lake_rural )
        (not_needed_diverted_traffic_lake_marketplace )
        (not_needed_diverted_traffic_lake_mill )
        (not_needed_diverted_traffic_lake_lake )
        (fire_at_byeng )
    )

    (:goal
        (and (addressed_media ) (extinguished_fire_byeng ))
    )

    
    (:bounds
        (number - int[-2147483647..2147483647]))
    (:metric minimize (total-cost ))
)

