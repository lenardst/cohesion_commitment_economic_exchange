# Date 14-05-2023
# Name: Lenard Strahringer
# This file runs the analysis on trade at the dyad round level

# dyad_trades analysis
  # Exclude third exchange in rounds because it is basically forced
dyad_trades12 = dyad_trades[dyad_trades$exchange_number != '3',]

# Normalize the variables
dyad_trades12$log_prev_deviation_norm <- scale(log(dyad_trades12$prev_deviation - min(dyad_trades12$prev_deviation) + 1))
dyad_trades12$log_prev_number_of_exchanges_norm <- scale(log(dyad_trades12$prev_number_of_exchanges + 1))
dyad_trades12$rep_distance_norm <- scale(dyad_trades12$rep_distance)
dyad_trades12$priv_rep_distance_norm <- scale(dyad_trades12$priv_rep_distance)

# Asess ML structure
test_ml_structure = glmer(trade ~ (1 |group_id/dyad_id) + (1 | player_id_a2) + (1 |player_id_a1),
                          data = dyad_trades12, family = binomial)
summary(test_ml_structure)

# Calculate ICC
(3.996e-09 + 4.935e-10)/(1.110e+01 +3.996e-09 + 4.935e-10)

# Fit model 1 with normalized variables
basis_model_t <- glmer(trade ~ log_prev_deviation_norm +
                                   log_prev_number_of_exchanges_norm +
                         (1 |group_id/dyad_id) + (1 | player_id_a2) + (1 |player_id_a1),
                                 data = dyad_trades12, family = binomial)
summary(basis_model_t)

# Fit model 2 including the interaction between rs and number of previous exchanges
inter_model_t = glmer(trade ~ log_prev_deviation_norm +
                        log_prev_number_of_exchanges_norm + rs + rs:log_prev_number_of_exchanges_norm +
                        (1 |group_id/dyad_id) + (1 | player_id_a2) + (1 |player_id_a1),
                      data = dyad_trades12, family = binomial)
summary(inter_model_t)

# Fit model 3 including the rank distance
inter_model_dist_t = glmer(trade ~ log_prev_deviation_norm +log_prev_number_of_exchanges_norm +
                             rs + rs:log_prev_number_of_exchanges_norm +
                             rep_distance_norm + priv_rep_distance_norm + rs:rep_distance_norm +
                             (1 |group_id/dyad_id) + (1 | player_id_a2) + (1 |player_id_a1),
                           data = dyad_trades12, family = binomial)
summary(inter_model_dist_t)

# Create regression table
model_list <- list(basis_model_t, inter_model_t, inter_model_dist_t)

# specify the model labels for each model
model_labels <- c("Model 1", "Model 2", "Model 3")

# generate the regression table using stargazer
table <- stargazer(model_list, 
                   type = "latex", 
                   title = "Logistic multi-level regression results on exchange at the dyad-round level
(n = 9,380)", 
                   label = "tab:round_regression_results",
                   model.numbers = TRUE, 
                   header = TRUE, 
                   column.sep.width = "0.05in", 
                   omit.stat = "f",
                   star.cutoffs	= c(0.05, 0.01, 0.001),
                   covariate.labels=c('log(total previous deviation)',
                                      'log(number of previous exchanges)', 'reputation system (RS)',
                                      'distance public reputation ranks', 'distance dyadic reputation ranks',
                                      'log(number of previous exchanges) X RS', 'distance public reputation ranks X RS', 'constant'))

# Calculate AME for log_prev_number_of_exchanges_norm and test difference
# AMEs for model 2
margins_RS <- margins(inter_model_t, variables=c('log_prev_number_of_exchanges_norm'), at=list(rs=1))
margins_noRS <- margins(inter_model_t, variables=c('log_prev_number_of_exchanges_norm'), at=list(rs=0))
summary(margins_RS)
summary(margins_noRS)
coef2 <- summary(margins_RS)$AME
se2 <- summary(margins_RS)$SE
coef1 <- summary(margins_noRS)$AME
se1 <- summary(margins_noRS)$SE

# Calculate the t statistic
t_stat <- (coef1 - coef2) / sqrt(se1^2 + se2^2)
# Calculate the p-value
p_value <- 2 * pt(abs(t_stat), df=4689, lower.tail=FALSE)
p_value

# AMEs for model 3
margins_RS <- margins(inter_model_dist_t, variables=c('log_prev_number_of_exchanges_norm', 'rep_distance_norm'), at=list(rs=1))
margins_noRS <- margins(inter_model_dist_t, variables=c('log_prev_number_of_exchanges_norm', 'rep_distance_norm'), at=list(rs=0))
summary(margins_RS)
summary(margins_noRS)

coef2 <- summary(margins_RS)$AME
se2 <- summary(margins_RS)$SE
coef1 <- summary(margins_noRS)$AME
se1 <- summary(margins_noRS)$SE


# Calculate the t statistic
t_stat <- (coef1 - coef2) / sqrt(se1^2 + se2^2)
# Calculate the p-value
p_value <- 2 * pt(abs(t_stat), df=4689, lower.tail=FALSE)
p_value


