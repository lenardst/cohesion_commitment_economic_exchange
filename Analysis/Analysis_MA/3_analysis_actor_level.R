# Date 14-05-2023
# Name: Lenard Strahringer
# This file runs the analysis on cohesion at the actor level 

# Calculate Cronbach's alpha for questionnaire measure
psych::alpha(subset(actor_df, select = c(close, cohesive, team, partners, harmonious)))

# Differences in earnings per round and t-test
var_list <- c("earnings_per_round")
t_test_results <- lapply(var_list, function(var) {
  t_test <- t.test(raw_dataset[[var]][raw_dataset$session.config.rs == 1], raw_dataset[[var]][raw_dataset$session.config.rs == 0], alternative = "greater")
  return(t_test$p.value)
})
t_test_results
mean(raw_dataset[raw_dataset$session.config.rs == 1,]$earnings_per_round)/mean(raw_dataset[raw_dataset$session.config.rs == 0,]$earnings_per_round)

# Differences in means for social cohesion measures
var_list <- c("gift", "scq_total")
t_test_results <- lapply(var_list, function(var) {
  t_test <- t.test(actor_df[[var]][actor_df$rs == 1], actor_df[[var]][actor_df$rs == 0], alternative = "greater")
  return(t_test$p.value)
})
t_test_results

# Test for difference in deviation between condition
t_test <- t.test(c(dyad_trades$deviation_a1[dyad_trades$rs == 1 & dyad_trades$trade],
                   dyad_trades$deviation_a2[dyad_trades$rs == 1 & dyad_trades$trade]),
                 c(dyad_trades$deviation_a1[dyad_trades$rs == 0 & dyad_trades$trade],
                   dyad_trades$deviation_a2[dyad_trades$rs == 0 & dyad_trades$trade]), alternative = 'two.sided')
t_test

# Create plot for deviation
dev_a1 <- dyad_trades[, c("rs", "deviation_a1", "trade", "prev_number_of_exchanges")] %>% rename(deviation = deviation_a1)
dev_a2 <- dyad_trades[, c("rs", "deviation_a2", "trade", "prev_number_of_exchanges")] %>% rename(deviation = deviation_a2)
dev_list <- bind_rows(dev_a1, dev_a2)
dev_list = dev_list[dev_list$trade == 1,]

means_df <- setNames(aggregate(c(deviation) ~ rs, data = dev_list, FUN = function(x) c(mean = mean(x))), c('rs', 'deviation'))
se_df <- setNames(aggregate(c(deviation) ~ rs, data = dev_list, FUN = function(x) c(se = qt(0.95,df=length(x)-1)*sd(x) / sqrt(length(x)))), c('rs', 'deviation'))
result_df <- merge(means_df, se_df, by = "rs")

plot2 = # plot for deviation total
  ggplot(result_df, aes(x = factor(rs), y = deviation.x, fill = factor(rs))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.9), color = "black") +
  geom_errorbar(aes(ymin = deviation.x - deviation.y, ymax = deviation.x + deviation.y), position = position_dodge(width = 0.9), width = 0.2) +
  theme(legend.position = "none") +
  ggtitle('mean deviation per exchange') + theme(plot.title = element_text(hjust = 0.5, size = 10)) +
  labs(x = '', y='') + scale_x_discrete(labels = c("no reputation system", "reputation system"))

# Plots for social cohesion measures
# calculate mean and standard error for each variable by rs group
means_df <- setNames(aggregate(cbind(gift, scq_total) ~ rs, data = actor_df, FUN = function(x) c(mean = mean(x))), c('rs', 'gift', 'scq_total'))
se_df <- setNames(aggregate(cbind(gift, scq_total) ~ rs, data = actor_df, FUN = function(x) c(se = qt(0.95,df=length(x)-1)*sd(x) / sqrt(length(x)))), c('rs', 'gift', 'scq_total'))
result_df <- merge(means_df, se_df, by = "rs")

# plot for gift total
plot3 = ggplot(result_df, aes(x = factor(rs), y = gift.x, fill = factor(rs))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.9), color = "black") +
  geom_errorbar(aes(ymin = gift.x - gift.y, ymax = gift.x + gift.y), position = position_dodge(width = 0.6), width = 0.2) +
  theme(legend.position = "none") + ylim(0, .75) +
  ggtitle('social cohesion (gift)') + theme(plot.title = element_text(hjust = 0.5, size = 10)) +
  labs(x = '', y='') + scale_x_discrete(labels = c("no reputation system", "reputation system"))

# Plot for scq total
plot4 = ggplot(result_df, aes(x = factor(rs), y = scq_total.x, fill = factor(rs))) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.9), color = "black") +
  geom_errorbar(aes(ymin = scq_total.x - scq_total.y, ymax = scq_total.x + scq_total.y), position = position_dodge(width = 0.6), width = 0.2) +
  theme(legend.position = "none") + ylim(0, .75) +
  ggtitle('social cohesion (questionnaire)') + theme(plot.title = element_text(hjust = 0.5, size = 10)) +
  labs(x = '', y='') + scale_x_discrete(labels = c("no reputation system", "reputation system"))

# Plot commitment behavior
# calculate the share of trades with changing partners and new partners for each round and rs value
dyad_trades_summary <- dyad_trades %>%
  group_by(round.number, rs) %>%
  summarize(
    share_change_partner = sum(change_partner)/sum(trade),
    share_new_partner = sum(new_partner)/sum(trade),
    cum_new_partner = sum(new_partner)/(14*15),
    n = n(),
    deviation = (sum(as.numeric(deviation_a1)) + sum(as.numeric(deviation_a2)))/sum(trade),
    sd_deviation = sd(as.numeric(deviation_a1)) + sum(as.numeric(deviation_a2))
  ) %>%
  ungroup() %>% group_by(rs) %>%
  mutate(
    se_change_partner = 1.96 * sqrt(share_change_partner * (1 - share_change_partner) / n),
    se_new_partner = 1.96 * sqrt(share_new_partner * (1 - share_new_partner) / n),
    cum_share_new_partner = cumsum(cum_new_partner),
    se_deviation = 1.96 * sqrt(sd_deviation/ n),
    cum_n = cumsum(n),
    cum_se_new_partner = 1.96 * sqrt((cum_share_new_partner* (1 - cum_share_new_partner) / cum_n))
  )

# plot the data
plot5 = ggplot(dyad_trades_summary, aes(x = as.numeric(round.number)-1, color = factor(rs))) +
  geom_line(aes(y = cum_share_new_partner, linetype = "Cumulative share of actors who exchanged at least once")) +
  geom_ribbon(aes(ymin = cum_share_new_partner - cum_se_new_partner, 
                  ymax = cum_share_new_partner + cum_se_new_partner, 
                  fill = "cumulative share of actors who exchanged at least once"), alpha = 0.05) +
  geom_line(aes(y = share_new_partner, linetype = "rate of exchanges between new/changing partners")) +
  geom_errorbar(aes(ymin = share_new_partner - se_new_partner, 
                    ymax = share_new_partner + se_new_partner), 
                width = 0.2) + xlim(1, 25) +
  scale_linetype_manual(values=c("solid","dashed")) +
  scale_fill_manual(values = "blue", guide = FALSE) +
  labs(x = "round", y = "rate of exchanges with new partners", color = "", linetype = "") +
  ggtitle('new exchange partners by round') + 
  scale_color_manual(values = c("#00bfc4", "#f8766d"), labels = c("no reputation system", "reputation system")) +
  theme(plot.title = element_text(hjust = 0.5, size = 10)) +
  theme(legend.position = "none", legend.title = element_blank())

# plot the data
plot6 = ggplot(dyad_trades_summary, aes(x = as.numeric(round.number)-1, y = share_change_partner, color = factor(rs))) +
  geom_line(aes(y = share_change_partner),linetype = "dashed") +
  geom_errorbar(aes(ymin = share_change_partner - se_change_partner, 
                    ymax = share_change_partner + se_change_partner), 
                width = 0.2) + xlim(1, 25) +
  labs(x = "round", y = "rate of exchanges with changing partners", color = "") +
  ggtitle('changing exchange partners by round') + theme(plot.title = element_text(hjust = 0.5, size = 10)) +
  scale_color_manual(values = c("#00bfc4", "#f8766d"), labels = c("no reputation system", "reputation system")) +
  theme(legend.position = "none", legend.title = element_blank())

# Combine plots
ggarrange(ggarrange(plot5, plot6, ncol = 2, nrow = 1, 
                    common.legend = TRUE, legend = "bottom", labels = c('A', 'B')),
          ggarrange(plot2, plot3, plot4, ncol = 3, nrow = 1, labels = c('C', 'D', 'E')), ncol = 1, nrow = 2)

# Multivariate analysis without controls
actor_df_panel <- pdata.frame(actor_df, index = c("actor_id"))

# Fit basic models 1 and 2
basis_model_g_clustered <- plm(gift ~ log(deviation_total_other-min(deviation_total_other)+1) + log(number_of_trades + 1), data = actor_df_panel, model = "pooling", vcov = vcovHC, cluster = "group")
summary(basis_model_g_clustered)

basis_model_q_clustered <- plm(scq_total ~ log(deviation_total_other-min(deviation_total_other)+1) + log(number_of_trades + 1), data = actor_df_panel, model = "pooling", vcov = vcovHC, cluster = "group")
summary(basis_model_q_clustered)

# Fit models 3 and 4 including the interaction effect between rs and deviation
inter_model_g <- plm(gift ~ log(deviation_total_other-min(deviation_total_other)+1) + log(number_of_trades + 1) + rs + rs:log(deviation_total_other-min(deviation_total_other)+1), data = actor_df_panel, model = "pooling", vcov = vcovHC, cluster = "group")
summary(inter_model_g)

inter_model_q <- plm(scq_total ~ log(deviation_total_other-min(deviation_total_other)+1) + log(number_of_trades + 1) + rs + rs:log(deviation_total_other-min(deviation_total_other)+1), data = actor_df_panel, model = "pooling", vcov = vcovHC, cluster = "group")
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
                   title = "Regression results on social cohesion at the directed dyad level (n = 840)", 
                   dep.var.labels = dep_var, 
                   label = "tab:regression_results",
                   model.numbers = TRUE, 
                   header = FALSE, 
                   column.sep.width = "0.05in",
                   notes = 'All models have robust standard errors clustered at the ego level.',
                   omit.stat = "f",
                   star.cutoffs	= c(0.05, 0.01, 0.001),
                   covariate.labels=c('log(total deviation)',
                                      'log(number of exchanges)', 'reputation system (RS)',
                                      'log(total deviation) X RS',
                                      'constant'))
