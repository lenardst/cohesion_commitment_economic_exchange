# Date 14-05-2023
# Name: Lenard Strahringer
# This file creates the descriptive tables on the actor and the dyad round level

# Descriptives table at the dyad level
summ.table = st(data=actor_df, title='Descriptive statistics at the dyad level (n = 840)',
   summ = c('mean(x)', 'sd(x)', 'min(x)', 'max(x)'), digits = 2,
   vars = c('number_of_trades',
            'deviation_total_other', 'gift', 'scq_total'),
   group = 'rs',
   out='latex',
   labels = c('number of exchanges', 'total deviation (other)', 'social cohesion (gift)',
              'social cohesion (questionnaire)'))

# Descriptives table at the dyad-round level
# exclude third exchange
dyad_trades12 = dyad_trades[dyad_trades$exchange_number != '3',]

summ.dr.table = st(data=dyad_trades12, title='Descriptive statistics at the dyad-round level (n = 9,380)',
                   summ = c('mean(x)', 'sd(x)', 'min(x)', 'max(x)'), digits = 2,
                   vars = c('trade', 'new_partner', 'change_partner', 'prev_deviation', 'prev_number_of_exchanges',
                            'rep_distance', 'priv_rep_distance'),
                   group = 'rs',
                   out='latex',
                   labels = c('trade', 'new partner', 'change partner', 'previous total deviation',
                              'previous number of exchanges', 'distance in public reputation rank',
                              'distance in dyadic reputation rank'))
