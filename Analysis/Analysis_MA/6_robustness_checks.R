# Date 14-05-2023
# Name: Lenard Strahringer
# This file runs a series of robustness checks at the actor and the dyad round level

# Robustness quadratic and positive negative 
sign_model_g <- plm(gift ~ log(deviation_total_other-min(deviation_total_other)+1) + log(number_of_trades + 1) + rs + rs:log(deviation_total_other-min(deviation_total_other)+1) + (deviation_total_other>0), data = actor_df_panel, model = "pooling", vcov = vcovHC, cluster = "group")
summary(sign_model_g)

sign_model_q <- plm(scq_total ~ log(deviation_total_other-min(deviation_total_other)+1) + log(number_of_trades + 1) + rs + rs:log(deviation_total_other-min(deviation_total_other)+1)  + (deviation_total_other>0), data = actor_df_panel, model = "pooling", vcov = vcovHC, cluster = "group")
summary(sign_model_q)

# Multivariate analysis with controls
basis_model_g_clustered <- plm(gift ~ log(deviation_total_other-min(deviation_total_other)+1) + log(number_of_trades + 1) + as.numeric(age)  + sex, data = actor_df_panel, model = "pooling", vcov = vcovHC, cluster = "group")
summary(basis_model_g_clustered)

basis_model_q_clustered <- plm(scq_total ~ log(deviation_total_other-min(deviation_total_other)+1) + log(number_of_trades + 1) + as.numeric(age)  + sex, data = actor_df_panel, model = "pooling", vcov = vcovHC, cluster = "group")
summary(basis_model_q_clustered)

inter_model_g <- plm(gift ~ log(deviation_total_other-min(deviation_total_other)+1) + log(number_of_trades + 1) + rs + rs:log(deviation_total_other-min(deviation_total_other)+1) + as.numeric(age)  + sex, data = actor_df_panel, model = "pooling", vcov = vcovHC, cluster = "group")
summary(inter_model_g)

inter_model_q <- plm(scq_total ~ log(deviation_total_other-min(deviation_total_other)+1) + log(number_of_trades + 1) + rs + rs:log(deviation_total_other-min(deviation_total_other)+1) + as.numeric(age)  + sex, data = actor_df_panel, model = "pooling", vcov = vcovHC, cluster = "group")
summary(inter_model_q)

# Create regression table
model_list <- list(basis_model_g_clustered, basis_model_q_clustered, inter_model_g, inter_model_q)

# specify the dependent variable names for each model
dep_var <- c("gift", "questionnaire", "gift", "questionnaire")

# specify the model labels for each model
model_labels <- c("Model 1", "Model 2", "Model 3", "Model 4")

# generate the regression table using stargazer
table <- stargazer(model_list, 
                   type = "latex", 
                   title = "Regression results on social cohesion at the directed dyad level including demographic controls (n = 840)", 
                   dep.var.labels = dep_var, 
                   label = "tab:regression_results_controls",
                   model.numbers = FALSE, 
                   header = FALSE, 
                   column.sep.width = "0.05in", 
                   omit.stat = "f",
                   star.cutoffs	= c(0.05, 0.01, 0.001),
                   covariate.labels=c('log(total deviation)', 'number of exchanges', 'reputation system (RS)',
                                      'age', 'gender male', 'gender other', 'log(total deviation) X RS', 'constant'))

# Robustness check including demographic controls at the dyad round level
# Fit the model with normalized variables
basis_model_t <- glmer(trade ~ log_prev_deviation_norm +
                         log_prev_number_of_exchanges_norm +
                         as.numeric(age_a1) + as.numeric(age_a2) + factor(sex_a1) + factor(sex_a2) +
                         (1 | dyad_id) + (1 | group_id),
                       data = dyad_trades12, family = binomial)
# Summarize model
summary(basis_model_t)

inter_model_t = glmer(trade ~ log_prev_deviation_norm +
                        log_prev_number_of_exchanges_norm + rs + rs:log_prev_number_of_exchanges_norm +
                        as.numeric(age_a1) + as.numeric(age_a2) + factor(sex_a1) + factor(sex_a2) +
                        (1 | dyad_id) + (1 | group_id),
                      data = dyad_trades12, family = binomial)
summary(inter_model_t)

inter_model_dist_t = glmer(trade ~ log_prev_deviation_norm +log_prev_number_of_exchanges_norm +
                             rs + rs:log_prev_number_of_exchanges_norm +
                             rep_distance_norm + priv_rep_distance_norm + rs:rep_distance_norm +
                             as.numeric(age_a1) + as.numeric(age_a2) + factor(sex_a1) + factor(sex_a2) +
                             (1 | dyad_id) + (1 | group_id),
                           data = dyad_trades12, family = binomial)
summary(inter_model_dist_t)


# Create regression table
model_list <- list(basis_model_t, inter_model_t, inter_model_dist_t)

# specify the model labels for each model
model_labels <- c("Model 1", "Model 2", "Model 3")

# generate the regression table using stargazer
table <- stargazer(model_list, 
                   type = "latex", 
                   title = "Logistic multi-level regression results on exchange at the dyad-round level including demographic controls (n = 9,380)", 
                   label = "tab:round_regression_results_controls",
                   model.numbers = TRUE, 
                   header = TRUE, 
                   digits = 2,
                   column.sep.width = "0.05in", 
                   omit.stat = "f",
                   single.row = TRUE,
                   star.cutoffs	= c(0.05, 0.01, 0.001),
                   font.size = 'small',
                   covariate.labels=c('log(total previous deviation)',
                                      'log(number of previous exchanges)', 'reputation system (RS)',
                                      'distance public reputation ranks', 'distance private reputation ranks',
                                      'age (actor 1)', 'age (actor 2)', 'gender male (actor 1)', 'gender other (actor 1)',
                                      'gender male (actor 2)', 'gender other (actor 2)',
                                      'log(number of previous exchanges) X RS', 'distance public reputation ranks X RS', 'constant'))