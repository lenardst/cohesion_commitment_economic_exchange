# Date 14-05-2023
# Name: Lenard Strahringer
# This file transforms the initial data sets into the data sets actor_df and dyad_trades, which will be used for the analysis

all_apps_wide_2023.03.03 = read.csv("Analysis/Analysis_MA/all_apps_wide_2023-03-03.csv", row.names=NULL)
all_apps_wide.only_25_session = read.csv("Analysis/Analysis_MA/all_apps_wide-only_25_session.csv", row.names=NULL)

# Session Data
session.code = c('o4jicxdf', '0f9hv0gn', 'wb6ybjy8', 'd5k4bihu', '9775dioj',
                 '52i9wx44', 'u6vjttdd', 'c92fp11i', 'nuw3zb83', 'wfzdptdi', '8fo3prj2')
rs = c(1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1)
groups = c(1, 1, 1, 2, 1, 2, 3, 4, 5, 4, 4)
rounds = c(25, 25, 25, 25, 26, 26, 26, 24, 25, 25, 24)
negotiation_app = c('negotiation', 'negotiation', 'negotiation25', 'negotiation', 'negotiation26', 'negotiation', 'negotiation', 'negotiation', 'negotiation', 'negotiation', 'negotiation')
sessions_table = data.frame(session.code, rs, groups, rounds, negotiation_app)

# Filter sessions
raw_dataset = all_apps_wide_2023.03.03
raw_dataset = raw_dataset[raw_dataset$session.code %in% sessions_table$session.code, ]

# Normalize different app names
different_names_26 = raw_dataset[(raw_dataset$session.code == '9775dioj'), ]
different_names_25 = all_apps_wide.only_25_session
different_names_26 = different_names_26 %>% select(-(starts_with('negotiation.') | starts_with('negotiation25.')))
different_names_25 = different_names_25 %>% select(-((starts_with('negotiation.') | starts_with('negotiation26.')) & !starts_with('negotiation.26.')))
colnames(different_names_25) = lapply(colnames(different_names_25),function(x) gsub("negotiation25.", "negotiation.", x))
colnames(different_names_26) = lapply(colnames(different_names_26),function(x) gsub("negotiation26.", "negotiation.", x))

raw_dataset = raw_dataset[raw_dataset$session.code %in% sessions_table[sessions_table$negotiation_app == 'negotiation', ]$session.code, ]
raw_dataset = raw_dataset %>% select(-(starts_with('negotiation') & !starts_with('negotiation.')))
raw_dataset = raw_dataset %>% select(-(starts_with('negotiation.28.')))
raw_dataset = raw_dataset %>% select(-(starts_with('negotiation.27.')))

different_names_25 = different_names_25[,c(1:507, 557:575, 508:556)]
different_names_26 = different_names_26[,c(1:32, 82:575, 33:81)]
raw_dataset = rbind(raw_dataset, different_names_25)
raw_dataset = rbind(raw_dataset, different_names_26)

# Calculate number of rounds
number_of_rounds = apply(raw_dataset[, c('negotiation.21.subsession.round_number', 'negotiation.22.subsession.round_number', 'negotiation.23.subsession.round_number', 'negotiation.24.subsession.round_number', 'negotiation.25.subsession.round_number', 'negotiation.26.subsession.round_number')],1,function(x) max(x[!is.na(x)]))
raw_dataset = cbind(raw_dataset, number_of_rounds)

# Remove variables not needed
raw_dataset = raw_dataset %>% select(-c('participant._is_bot', 'participant._index_in_pages', 'participant._max_page_index', 'participant._current_app_name', 'participant._current_page_name', 'participant.time_started_utc', 'participant.visited', 'participant.mturk_worker_id', 'participant.mturk_assignment_id', 'participant.exchange_list', 'session.label', 'session.mturk_HITId', 'session.mturk_HITGroupId', 'session.comment', 'session.is_demo', 'session.config.participation_fee', 'session.config.name', 'session.config.real_world_currency_per_point'))
raw_dataset = raw_dataset %>% select(-starts_with('instruction.1.'))
raw_dataset = raw_dataset %>% select(-(contains('quiz') & !contains('negotiation.1.')))
raw_dataset = raw_dataset %>% select(-ends_with('role'))
raw_dataset = raw_dataset %>% select(-ends_with('color_order') & -ends_with('player_order'))
raw_dataset = raw_dataset %>% select(-(ends_with('id_in_group') & !(contains('negotiation.1.') | contains('negotiation.2.'))))
raw_dataset = raw_dataset %>% select(-c('scmeasure.1.group.id_in_subsession','scmeasure.1.subsession.round_number'))
raw_dataset = raw_dataset %>% select(-(contains('group.id_in_subsession') & !contains('negotiation.2.')))
raw_dataset = raw_dataset %>% select(-ends_with('subsession.round_number'))
raw_dataset = raw_dataset %>% select(-(starts_with('negotiation.1.') & !(contains('quiz'))))

# First measure calculation
total_gifted = rowSums(raw_dataset[, c('scmeasure.1.player.gift1', 'scmeasure.1.player.gift2', 'scmeasure.1.player.gift3', 'scmeasure.1.player.gift4', 'scmeasure.1.player.gift5', 'scmeasure.1.player.gift6')])
earnings_per_round = raw_dataset$scmeasure.1.player.trading_earnings / raw_dataset$number_of_rounds
raw_dataset = cbind(raw_dataset, total_gifted)
raw_dataset = cbind(raw_dataset, earnings_per_round)

# Transform data into dyad trades format
dyad_trades <- data.frame(matrix(ncol = 44, nrow = 0))
x <- c('session.code','rounds_total', 'rs', 'group.number', 'id_a1', 'id_a2', 'round.number',
       'trade', 'sent_a1', 'sent_a2', 'deviation_a1', 'deviation_a2', 'exchange_number',
       'number_exchanges_in_group', 'gift_a1', 'gift_a2', 'close_a1', 'close_a2', 'cohesive_a1',
       'cohesive_a2', 'team_a1', 'team_a2', 'partners_a1', 'partners_a2', 'harmonious_a1',
       'harmonious_a2', 'age_a1', 'age_a2', 'sex_a1', 'sex_a2', 'major_a1', 'major_a2',
       'priv_reputation_a1', 'priv_reputation_a2', 'publ_reputation_a1', 'publ_reputation_a2',
       'prev_units_agreed', 'prev_deviation', 'prev_number_of_exchanges', 'prev_number_exchange',
       'new_partner', 'change_partner', 'change_partner_next', 'perfect_trade')
colnames(dyad_trades) <- x

# Add measures on dyad-round level
for (s in 1:length(sessions_table$session.code)) {
  session.code = sessions_table[s,1]
  rs = sessions_table[s,2]
  rounds_total = sessions_table[s,4]
  for (g in 1:sessions_table[s,3]){
    group.number = g
    for (r in 2:sessions_table[s,4]){
      round.number = r
      for (a1 in 1:5){
        id_a1 = a1
        for (a2 in (a1+1):6){
          id_a2 = a2
          # look up trade
          select_row = raw_dataset[raw_dataset$session.code == session.code & raw_dataset$negotiation.2.group.id_in_subsession == group.number &
                                     raw_dataset$negotiation.2.player.id_in_group == a1, ] %>% select(
                                       c(paste('negotiation.',toString(r), '.player.agreed', sep = ""), paste('negotiation.',toString(r), '.player.exchange_partner', sep = ""),
                                         paste('negotiation.',toString(r), '.player.send', sep = ""), paste('negotiation.',toString(r), '.player.receive', sep = ""),
                                         paste('negotiation.',toString(r), '.player.deviation', sep = ""), paste('negotiation.',toString(r), '.player.deviation_partner', sep = ""),
                                         paste('negotiation.',toString(r), '.player.exchange_number', sep = ""), paste('negotiation.',toString(r), '.group.number_exchanges', sep = "")))
          if (select_row[1,1] & select_row[1,2] == a2){
            c(trade, sent_a1, sent_a2, deviation_a1, deviation_a2, exchange_number, number_exchanges_in_group) %<-% c(1, select_row[1, 3:8])
          } else {
            c(trade, sent_a1, sent_a2, deviation_a1, deviation_a2, exchange_number, number_exchanges_in_group) %<-% rep(0, 7)
          }
          # social cohesion measures a1
          sc_row_a1 = raw_dataset[raw_dataset$session.code == session.code & raw_dataset$negotiation.2.group.id_in_subsession == group.number &
                                    raw_dataset$negotiation.2.player.id_in_group == a1, ]%>% select(c(
                                      paste('scmeasure.1.player.gift', toString(a2), sep = ""), paste('scmeasure.1.player.close', toString(a2), sep = ""), paste('scmeasure.1.player.cohesive', toString(a2), sep = ""),
                                      paste('scmeasure.1.player.team', toString(a2), sep = ""), paste('scmeasure.1.player.partners', toString(a2), sep = ""), paste('scmeasure.1.player.harmonious', toString(a2), sep = ""), 
                                      'scmeasure.1.player.age', 'scmeasure.1.player.sex', 'scmeasure.1.player.major'))
          c(gift_a1, close_a1, cohesive_a1, team_a1, partners_a1, harmonious_a1, age_a1, sex_a1, major_a1) %<-% c(sc_row_a1[1,1:9])
          # social cohesion measures a2
          sc_row_a2 = raw_dataset[raw_dataset$session.code == session.code & raw_dataset$negotiation.2.group.id_in_subsession == group.number &
                                    raw_dataset$negotiation.2.player.id_in_group == a2, ]%>% select(c(
                                      paste('scmeasure.1.player.gift', toString(a1), sep = ""), paste('scmeasure.1.player.close', toString(a1), sep = ""), paste('scmeasure.1.player.cohesive', toString(a1), sep = ""),
                                      paste('scmeasure.1.player.team', toString(a1), sep = ""), paste('scmeasure.1.player.partners', toString(a1), sep = ""), paste('scmeasure.1.player.harmonious', toString(a1), sep = ""), 
                                      'scmeasure.1.player.age', 'scmeasure.1.player.sex', 'scmeasure.1.player.major'))
          c(gift_a2, close_a2, cohesive_a2, team_a2, partners_a2, harmonious_a2, age_a2, sex_a2, major_a2) %<-% c(sc_row_a2[1,1:9])
          exchange_number = (7 - 2 * exchange_number) * I(exchange_number != 0)
          dyad_trades[nrow(dyad_trades) + 1,] = c(session.code, as.numeric(rounds_total), rs, group.number, id_a1, id_a2, round.number,
                                                  trade, sent_a1, sent_a2, deviation_a1, deviation_a2, exchange_number,
                                                  number_exchanges_in_group, gift_a1, gift_a2, close_a1, close_a2, cohesive_a1,
                                                  cohesive_a2, team_a1, team_a2, partners_a1, partners_a2, harmonious_a1,
                                                  harmonious_a2, age_a1, age_a2, sex_a1, sex_a2, major_a1, major_a2, rep(0,8), trade, trade,0, 0)
          # Add dyad-trade measures
          if (round.number > 2){
            dyad_prev_round = dyad_trades[dyad_trades$session.code == session.code & dyad_trades$group.number == group.number & dyad_trades$id_a1 == id_a1 & dyad_trades$id_a2 == id_a2 & dyad_trades$round.number == round.number-1, ]
            if (as.numeric(dyad_prev_round$trade)) {
              dyad_trades[nrow(dyad_trades),]$priv_reputation_a1 = as.numeric(dyad_prev_round$priv_reputation_a1) + as.numeric(dyad_prev_round$deviation_a1)
              dyad_trades[nrow(dyad_trades),]$priv_reputation_a2 = as.numeric(dyad_prev_round$priv_reputation_a2) + as.numeric(dyad_prev_round$deviation_a2)
              dyad_trades[nrow(dyad_trades),]$prev_units_agreed = as.numeric(dyad_prev_round$prev_units_agreed) + as.numeric(dyad_prev_round$sent_a1) + as.numeric(dyad_prev_round$sent_a2)
              dyad_trades[nrow(dyad_trades),]$prev_deviation = as.numeric(dyad_prev_round$prev_deviation) + as.numeric(dyad_prev_round$deviation_a1) + as.numeric(dyad_prev_round$deviation_a2) 
              dyad_trades[nrow(dyad_trades),]$prev_number_of_exchanges = as.numeric(dyad_prev_round$prev_number_of_exchanges) + 1
              dyad_trades[nrow(dyad_trades),]$prev_number_exchange = as.numeric(dyad_prev_round$prev_number_exchange) + as.numeric(dyad_prev_round$exchange_number)
              dyad_trades[nrow(dyad_trades),]$new_partner = 0
              dyad_trades[nrow(dyad_trades),]$change_partner = 0
              dyad_trades[nrow(dyad_trades),]$perfect_trade = (as.numeric(dyad_prev_round$sent_a1) + as.numeric(dyad_prev_round$sent_a2) + as.numeric(dyad_prev_round$deviation_a1) + as.numeric(dyad_prev_round$deviation_a2)) == 40
              dyad_trades[dyad_trades$session.code == session.code & dyad_trades$group.number == group.number & dyad_trades$id_a1 == id_a1 & dyad_trades$id_a2 == id_a2 & dyad_trades$round.number == round.number-1, ]$change_partner_next = !as.numeric(dyad_trades[nrow(dyad_trades),]$trade)
            } else {
              dyad_trades[nrow(dyad_trades),]$priv_reputation_a1 = dyad_prev_round$priv_reputation_a1
              dyad_trades[nrow(dyad_trades),]$priv_reputation_a2 = dyad_prev_round$priv_reputation_a2
              dyad_trades[nrow(dyad_trades),]$prev_units_agreed = dyad_prev_round$prev_units_agreed
              dyad_trades[nrow(dyad_trades),]$prev_deviation = dyad_prev_round$prev_deviation
              dyad_trades[nrow(dyad_trades),]$prev_number_of_exchanges = dyad_prev_round$prev_number_of_exchanges
              dyad_trades[nrow(dyad_trades),]$prev_number_exchange = dyad_prev_round$prev_number_exchange
              dyad_trades[nrow(dyad_trades),]$change_partner = trade
              dyad_trades[dyad_trades$session.code == session.code & dyad_trades$group.number == group.number & dyad_trades$id_a1 == id_a1 & dyad_trades$id_a2 == id_a2 & dyad_trades$round.number == round.number-1, ]$change_partner_next = as.logical(dyad_trades[nrow(dyad_trades),]$trade)
              if (dyad_trades[nrow(dyad_trades),]$prev_number_of_exchanges == 0){
                dyad_trades[nrow(dyad_trades),]$new_partner = trade
              } else {
                dyad_trades[nrow(dyad_trades),]$new_partner = 0
              }
            }
            dyad_trades[nrow(dyad_trades),]$publ_reputation_a1 = mean(c(as.numeric(dyad_trades[dyad_trades$session.code == session.code & dyad_trades$group.number == group.number & dyad_trades$id_a1 == a1 & dyad_trades$round.number < round.number & as.numeric(dyad_trades$trade), ]$deviation_a1), as.numeric(dyad_trades[dyad_trades$session.code == session.code & dyad_trades$group.number == group.number & dyad_trades$id_a2 == a1 & dyad_trades$round.number < as.numeric(round.number), ]$deviation_a2)))
            dyad_trades[nrow(dyad_trades),]$publ_reputation_a2 = mean(c(as.numeric(dyad_trades[dyad_trades$session.code == session.code & dyad_trades$group.number == group.number & dyad_trades$id_a1 == a2 & dyad_trades$round.number < round.number & as.numeric(dyad_trades$trade), ]$deviation_a1), as.numeric(dyad_trades[dyad_trades$session.code == session.code & dyad_trades$group.number == group.number & dyad_trades$id_a2 == a2 & dyad_trades$round.number < as.numeric(round.number), ]$deviation_a2)))
          }
        }
      }
    }
  }
}

# Calculate means for round-dyad variables
dyad_trades$prev_number_of_exchanges = as.numeric(dyad_trades$prev_number_of_exchanges)
dyad_trades$priv_reputation_a1 = as.numeric(dyad_trades$priv_reputation_a1) / dyad_trades$prev_number_of_exchanges
dyad_trades[is.na(dyad_trades$priv_reputation_a1), ]$priv_reputation_a1 = 0
dyad_trades$priv_reputation_a2 = as.numeric(dyad_trades$priv_reputation_a2) / dyad_trades$prev_number_of_exchanges
dyad_trades[is.na(dyad_trades$priv_reputation_a2), ]$priv_reputation_a2 = 0
dyad_trades$prev_units_agreed = as.numeric(dyad_trades$prev_units_agreed)
dyad_trades$prev_deviation = as.numeric(dyad_trades$prev_deviation)
dyad_trades$prev_number_exchange = as.numeric(dyad_trades$prev_number_exchange) / dyad_trades$prev_number_of_exchanges
dyad_trades[dyad_trades$prev_number_exchange == 'NaN', ]$prev_number_exchange = 0
dyad_trades[dyad_trades$publ_reputation_a1 == 'NaN', ]$publ_reputation_a1 = 0
dyad_trades[dyad_trades$publ_reputation_a2 == 'NaN', ]$publ_reputation_a2 = 0

# Add group_id
group_id = paste(dyad_trades$session.code, dyad_trades$group.number, sep = "")
dyad_trades = cbind(dyad_trades, group_id)
dyad_trades$round.number = as.numeric(dyad_trades$round.number)
dyad_trades$rs = as.numeric(dyad_trades$rs)
dyad_trades$trade = as.numeric(dyad_trades$trade)
dyad_trades$change_partner = as.numeric(dyad_trades$change_partner)
dyad_trades$new_partner = as.numeric(dyad_trades$new_partner)
dyad_trades[is.na(dyad_trades$change_partner_next),]$change_partner_next = FALSE

# Aggregate rounds
dyad_list = aggregate(cbind(as.numeric(trade), as.numeric(sent_a1), as.numeric(sent_a2), as.numeric(deviation_a1), as.numeric(deviation_a2), as.numeric(exchange_number))
                      ~ group_id + rs+ rounds_total+ id_a1+ id_a2+ gift_a1+ gift_a2+ close_a1+ close_a2+ cohesive_a1+ cohesive_a2+ team_a1+ team_a2+ partners_a1+ partners_a2+ harmonious_a1+ harmonious_a2+ age_a1+ age_a2+ sex_a1+ sex_a2+ major_a1+ major_a2 ,
                      FUN = sum, data=dyad_trades, na.action=na.pass)

dyad_list = dyad_list %>% rename(
  number_of_trades = V1,
  sent_total_a1 = V2,
  sent_total_a2 = V3,
  deviation_total_a1 = V4,
  deviation_total_a2 = V5,
  mean_exchange_number = V6
)

# Calculate mean exchange number
dyad_list$mean_exchange_number = dyad_list$mean_exchange_number / dyad_list$number_of_trades 
dyad_list[is.na(dyad_list$mean_exchange_number),]$mean_exchange_number = 0

# Add social cohesion measures
dyad_list$close_a1 = 6 - as.numeric(dyad_list$close_a1)
dyad_list$close_a2 = 6 - as.numeric(dyad_list$close_a2)

scq_total_a1 = dyad_list$close_a1 + as.numeric(dyad_list$cohesive_a1) +
  as.numeric(dyad_list$team_a1) + as.numeric(dyad_list$partners_a1) +
  as.numeric(dyad_list$harmonious_a1) 
scq_total_a2 = dyad_list$close_a2 + as.numeric(dyad_list$cohesive_a2) +
  as.numeric(dyad_list$team_a2) + as.numeric(dyad_list$partners_a2) + 
  as.numeric(dyad_list$harmonious_a2)
dyad_list = cbind(dyad_list, scq_total_a1, scq_total_a2)
dyad_list$scq_total_a1 = max(dyad_list$scq_total_a1) - dyad_list$scq_total_a1
dyad_list$scq_total_a2 = max(dyad_list$scq_total_a2) - dyad_list$scq_total_a2

# Transform to actor level data
actor_df <- dyad_list %>%
  select(group_id, rs, gift_a1, scq_total_a1, id_a1, id_a2, sex_a1, age_a1, deviation_total_a2, close_a1, cohesive_a1, team_a1, partners_a1, harmonious_a1, number_of_trades, mean_exchange_number, rounds_total) %>%
  rename(id = id_a1, id_other = id_a2, gift = gift_a1, scq_total = scq_total_a1, deviation_total_other = deviation_total_a2,
         sex = sex_a1, age = age_a1, close = close_a1, cohesive = cohesive_a1, team = team_a1, partners = partners_a1, harmonious = harmonious_a1) %>%
  bind_rows(dyad_list %>%
              select(group_id, rs, gift_a2, scq_total_a2, id_a1, id_a2, close_a2, cohesive_a2, team_a2, partners_a2, harmonious_a2, sex_a2, age_a2, deviation_total_a1, number_of_trades, mean_exchange_number, rounds_total) %>%
              rename(id = id_a2, id_other = id_a1, gift = gift_a2, scq_total = scq_total_a2, deviation_total_other = deviation_total_a1,
                     sex = sex_a2, age = age_a2, close = close_a2, cohesive = cohesive_a2, team = team_a2, partners = partners_a2, harmonious = harmonious_a2)) %>%
  mutate(actor_id = paste0(group_id, "_", id), actor_id_other = paste0(group_id, "_", id_other))

# rescale
actor_df$scq_total = actor_df$scq_total/max(actor_df$scq_total)
actor_df$close <- as.numeric(as.character(actor_df$close))
actor_df$cohesive <- as.numeric(as.character(actor_df$cohesive))
actor_df$team <- as.numeric(as.character(actor_df$team))
actor_df$partners <- as.numeric(as.character(actor_df$partners))
actor_df$harmonious <- as.numeric(as.character(actor_df$harmonious))
actor_df$gift <- as.numeric(as.character(actor_df$gift))
actor_df$scq_total <- as.numeric(as.character(actor_df$scq_total))
actor_df$rounds_total <- as.numeric(as.character(actor_df$rounds_total))
dyad_trades$deviation_a1 = as.numeric(dyad_trades$deviation_a1)
dyad_trades$deviation_a2 = as.numeric(dyad_trades$deviation_a2)
dyad_trades$trade = as.numeric(dyad_trades$trade)

# caculate reputation rank
# Group the data by round.number and group_id
grouped_data_a1 <- dyad_trades %>% group_by(round.number, group_id, id_a1)
grouped_data_a2 <- dyad_trades %>% group_by(round.number, group_id, id_a2)

# Calculate the reputation rank of each actor within their group in each round.number
ranked_data_a2 <- grouped_data_a1 %>% 
  mutate(publ_reputation_rank_a2 = rank(-as.numeric(publ_reputation_a2)),
         priv_reputation_rank_a2 = rank(-as.numeric(priv_reputation_a2))) %>%
  ungroup() # remove grouping
ranked_data_a1 <- grouped_data_a2 %>% 
  mutate(publ_reputation_rank_a1 = rank(-as.numeric(publ_reputation_a1)),
         priv_reputation_rank_a1 = rank(-as.numeric(priv_reputation_a1))) %>%
  ungroup() # remove grouping

# Join the ranked data back to the original data by dyad ID to update the reputation rank columns
dyad_trades <- dyad_trades %>%
  left_join(ranked_data_a2[,c("id_a1", "id_a2", "round.number", 'group_id', "publ_reputation_rank_a2", 'priv_reputation_rank_a2')], 
            by = c("id_a1", "id_a2", "round.number", 'group_id'))
dyad_trades <- dyad_trades %>%
  left_join(ranked_data_a1[,c("id_a1", "id_a2", "round.number", 'group_id', "publ_reputation_rank_a1", 'priv_reputation_rank_a1')], 
            by = c("id_a1", "id_a2", "round.number", 'group_id'))

# reputation distance
rep_distance = abs(dyad_trades$publ_reputation_rank_a1 - dyad_trades$publ_reputation_rank_a2)
priv_rep_distance = abs(dyad_trades$priv_reputation_rank_a1 - dyad_trades$priv_reputation_rank_a2)
dyad_trades = cbind(dyad_trades, rep_distance)
dyad_trades = cbind(dyad_trades, priv_rep_distance)

# Create ids for actors and dyads
dyad_trades$player_id_a1 <- paste(dyad_trades$group_id, dyad_trades$id_a1, sep = "_")
dyad_trades$player_id_a2 <- paste(dyad_trades$group_id, dyad_trades$id_a2, sep = "_")
dyad_trades$dyad_id <- factor(paste(dyad_trades$player_id_a1, dyad_trades$player_id_a2, sep = "_"))

save(dyad_trades, file='dyad_trades.Rda')
save(actor_df, file='actor_df.Rda')
