# Date 14-05-2023
# Name: Lenard Strahringer
# This file runs the analysis on partner change and new partner choice at the dyad-round level
load("dyad_trades.Rda")
# Join dyad_trades with dyad_trades
dyad_trades_pep <- dyad_trades # Make a copy of the original data frame

# Add the '_pep' suffix to variable names that do not match specified names
names(dyad_trades_pep) <- ifelse(names(dyad_trades) %in% c("round.number", "group_id"), 
                                 names(dyad_trades), paste0(names(dyad_trades), "_pep"))

dyad_trades_joint <- dyad_trades %>%
  full_join(dyad_trades_pep[,c('id_a1_pep', 'id_a2_pep', 'round.number', 'group_id', 'trade_pep','rep_distance_pep',
                               'priv_rep_distance_pep', 'prev_units_agreed_pep',
                               'prev_deviation_pep', 'prev_number_of_exchanges_pep', 'prev_number_exchange_pep', 'dyad_id_pep', 'player_id_a1_pep', 'player_id_a2_pep')], 
            by = c('round.number', 'group_id'), multiple = "all")

# Look up trade in last round
dyad_trades_round_inc = dyad_trades
dyad_trades_round_inc$round.number = dyad_trades_round_inc$round.number + 1
dyad_trades_round_inc = rename(dyad_trades_round_inc, trade_prev = trade)
dyad_trades_round_inc = rename(dyad_trades_round_inc, exchange_number_prev = exchange_number)
dyad_trades_round_inc = rename(dyad_trades_round_inc, perfect_trade_prev = perfect_trade)
dyad_trades_round_inc = rename(dyad_trades_round_inc, id_a1_pep = id_a1)
dyad_trades_round_inc = rename(dyad_trades_round_inc, id_a2_pep = id_a2)

dyad_trades_joint <- dyad_trades_joint %>%
  left_join(dyad_trades_round_inc[,c('id_a1_pep', 'id_a2_pep', 'round.number', 'group_id', 'trade_prev', 'exchange_number_prev', 'perfect_trade_prev')], 
            by = c('id_a1_pep', 'id_a2_pep', 'round.number', 'group_id'))

# only keep when trade_prev == 1
dyad_trades_joint = dyad_trades_joint[dyad_trades_joint$trade_prev == 1 & dyad_trades_joint$round.number>2,]
# drop same dyads
dyad_trades_joint = dyad_trades_joint[xor(xor(xor(dyad_trades_joint$id_a2 == dyad_trades_joint$id_a1_pep,
                                                  dyad_trades_joint$id_a1 == dyad_trades_joint$id_a2_pep),
                                              dyad_trades_joint$id_a1 == dyad_trades_joint$id_a1_pep),
                                          dyad_trades_joint$id_a2 == dyad_trades_joint$id_a2_pep),]

prev_deviation_diff = dyad_trades_joint$prev_deviation - dyad_trades_joint$prev_deviation_pep
prev_number_of_exchanges_diff = dyad_trades_joint$prev_number_of_exchanges-dyad_trades_joint$prev_number_of_exchanges_pep
prev_number_exchange_diff = dyad_trades_joint$prev_number_exchange - dyad_trades_joint$prev_number_exchange_pep
rep_distance_diff = dyad_trades_joint$rep_distance - dyad_trades_joint$rep_distance_pep
priv_rep_distance_diff = dyad_trades_joint$priv_rep_distance - dyad_trades_joint$priv_rep_distance_pep
dyad_trades_joint = cbind(dyad_trades_joint, prev_deviation_diff, prev_number_of_exchanges_diff,
                          prev_number_exchange_diff, rep_distance_diff, priv_rep_distance_diff)
# Exclude third exchanges
dyad_trades_joint = dyad_trades_joint[dyad_trades_joint$exchange_number != '3',]

# Rescale variables
dyad_trades_joint$log_prev_deviation_diff <- log(dyad_trades_joint$prev_deviation_diff - min(dyad_trades_joint$prev_deviation_diff) + 1)
dyad_trades_joint$log_prev_number_of_exchanges_diff <- log(dyad_trades_joint$prev_number_of_exchanges_diff - min(dyad_trades_joint$prev_number_of_exchanges_diff) + 1)
dyad_trades_joint$prev_number_exchange_diff <- scale(dyad_trades_joint$prev_number_exchange_diff, center = TRUE, scale = TRUE)
dyad_trades_joint$rep_distance_diff <- scale(dyad_trades_joint$rep_distance_diff, center = TRUE, scale = TRUE)
dyad_trades_joint$priv_rep_distance_diff <- scale(dyad_trades_joint$priv_rep_distance_diff, center = TRUE, scale = TRUE)

# ANALYSIS
# Model 1 on partner change including the interaction between rs and number of previous exchanges
rs_model_t <- glmer(trade ~ log_prev_deviation_diff + log_prev_number_of_exchanges_diff + 
                    prev_number_exchange_diff + prev_number_exchange_diff +
                    round.number + rs + log_prev_number_of_exchanges_diff:rs +
                    (1 |group_id/dyad_id),
                    data = dyad_trades_joint, family = binomial)
summary(rs_model_t)

# AMEs of model 1
margins_RS <- margins(rs_model_t, variables=c('log_prev_number_of_exchanges_diff'), at=list(rs=1))
margins_noRS <- margins(rs_model_t, variables=c('log_prev_number_of_exchanges_diff'), at=list(rs=0))
summary(margins_RS)
summary(margins_noRS)

coef2 <- summary(margins_RS)$AME
se2 <- summary(margins_RS)$SE
coef1 <- summary(margins_noRS)$AME
se1 <- summary(margins_noRS)$SE

# Calculate the t statistic
t_stat <- (coef1 - coef2) / sqrt(se1^2 + se2^2)
# Calculate the p-value
p_value <- 2 * pt(abs(t_stat), df=7481, lower.tail=FALSE)
p_value

# Model 2 on partner change including the distance in ranks
rank_model_t <- glmer(trade ~ log_prev_deviation_diff + log_prev_number_of_exchanges_diff + prev_number_exchange_diff +
                        round.number + rs + rep_distance_diff + log_prev_number_of_exchanges_diff:rs + 
                        priv_rep_distance_diff + rs:rep_distance_diff +
                        (1 |group_id/dyad_id),
                      data = dyad_trades_joint, family = binomial)
summary(rank_model_t)

# AMEs model 2
margins_RS <- margins(rank_model_t, variables=c('log_prev_number_of_exchanges_diff', 'rep_distance_diff'), at=list(rs=1))
margins_noRS <- margins(rank_model_t, variables=c('log_prev_number_of_exchanges_diff', 'rep_distance_diff'), at=list(rs=0))
summary(margins_RS)
summary(margins_noRS)

coef2 <- summary(margins_RS)$AME
se2 <- summary(margins_RS)$SE
coef1 <- summary(margins_noRS)$AME
se1 <- summary(margins_noRS)$SE

# Calculate the t statistic
t_stat <- (coef1 - coef2) / sqrt(se1^2 + se2^2)
# Calculate the p-value
p_value <- 2 * pt(abs(t_stat), df=7481, lower.tail=FALSE)
p_value

# Reduce set for new partner choices
dyad_trades_joint = dyad_trades_joint[dyad_trades_joint$prev_number_of_exchanges == 0,]

# Model 3 on new partner choice including the interaction between rs and number of previous exchanges
rs_model_t_np <- glmer(trade ~ log_prev_deviation_diff + log_prev_number_of_exchanges_diff + 
                         prev_number_exchange_diff + prev_number_exchange_diff
                       + round.number + rs + log_prev_number_of_exchanges_diff:rs +
                         (1 |dyad_id),
                       data = dyad_trades_joint, family = binomial)
summary(rs_model_t_np)

margins_RS <- margins(rs_model_t_np, variables=c('log_prev_number_of_exchanges_diff'), at=list(rs=1))
margins_noRS <- margins(rs_model_t_np, variables=c('log_prev_number_of_exchanges_diff'), at=list(rs=0))
summary(margins_RS)
summary(margins_noRS)

coef2 <- summary(margins_RS)$AME
se2 <- summary(margins_RS)$SE
coef1 <- summary(margins_noRS)$AME
se1 <- summary(margins_noRS)$SE

# Calculate the t statistic
t_stat <- (coef1 - coef2) / sqrt(se1^2 + se2^2)
# Calculate the p-value
p_value <- 2 * pt(abs(t_stat), df=7481, lower.tail=FALSE)
p_value

# Model 4 on new partner choice including the distance in ranks
rank_model_t_np <- glmer(trade ~ log_prev_deviation_diff + log_prev_number_of_exchanges_diff + prev_number_exchange_diff +
                           round.number + rs + rep_distance_diff + log_prev_number_of_exchanges_diff:rs + 
                           priv_rep_distance_diff + rs:rep_distance_diff +
                           (1 | dyad_id),
                         data = dyad_trades_joint, family = binomial)
summary(rank_model_t_np)

# AMEs model 4
margins_RS <- margins(rank_model_t_np, variables=c('log_prev_number_of_exchanges_diff', 'rep_distance_diff'), at=list(rs=1))
margins_noRS <- margins(rank_model_t_np, variables=c('log_prev_number_of_exchanges_diff', 'rep_distance_diff'), at=list(rs=0))
summary(margins_RS)
summary(margins_noRS)

coef2 <- summary(margins_RS)$AME
se2 <- summary(margins_RS)$SE
coef1 <- summary(margins_noRS)$AME
se1 <- summary(margins_noRS)$SE

# Calculate the t statistic
t_stat <- (coef1 - coef2) / sqrt(se1^2 + se2^2)
# Calculate the p-value
p_value <- 2 * pt(abs(t_stat), df=7481, lower.tail=FALSE)
p_value

# Create table
model_list <- list(rs_model_t, rank_model_t, rs_model_t_np, rank_model_t_np)

dep_var <- c("Partner Change", "Partner Change", "New Partner", "New Partner")


# generate the regression table using stargazer
table <- stargazer(model_list, 
                   type = "latex", 
                   title = "Logistic multi-level regression results on partner change and new partner choice at the pair-dyad-round level (n = 14,962)", 
                   label = "tab:partner_change_regression",
                   model.numbers = TRUE, 
                   header = FALSE,
                   dep.var.labels = dep_var, 
                   column.sep.width = "0.01in",
                   star.cutoffs	= c(0.05, 0.01, 0.001),
                   omit = c('prev_number_exchange_diff'),
                   single.row = TRUE,
                   covariate.labels=c('difference in log(total deviation)',
                                      'difference in log(number of previous exchanges)',
                                      'round number','reputation system (RS)',
                                      'difference in distance public reputation ranks',
                                      'difference in distance dyadic reputation ranks',
                                      'difference in log(number of previous exchanges) X RS',
                                      'difference in distance public reputation ranks X RS', 'constant'))
