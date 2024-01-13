# 2D plot
# Create a subsets for rs
data_rs0 <- actor_df[2<actor_df$number_of_trades & actor_df$rs == 0,]
data_rs1 <- actor_df[2<actor_df$number_of_trades & actor_df$rs == 1,]

# Dens
dens_g0 <- kde2d(data_rs0$gift, data_rs0$number_of_trades, n = 26)
dens_g1 <- kde2d(data_rs1$gift, data_rs1$number_of_trades, n = 26)
dens_q0 <- kde2d(data_rs0$scq_total, data_rs0$number_of_trades, n = 26)
dens_q1 <- kde2d(data_rs1$scq_total, data_rs1$number_of_trades, n = 26)

# Convert density matrices to data frames
dens_df_g0 <- reshape2::melt(as.matrix(dens_g0$z)) %>% mutate(number_of_trades = Var2, gift = Var1/26)
dens_df_g1 <- reshape2::melt(as.matrix(dens_g1$z)) %>% mutate(number_of_trades = Var2, gift = Var1/26)
dens_df_q0 <- reshape2::melt(as.matrix(dens_q0$z)) %>% mutate(number_of_trades = Var2, scq_total = Var1/26)
dens_df_q1 <- reshape2::melt(as.matrix(dens_q1$z)) %>% mutate(number_of_trades = Var2, scq_total = Var1/26)
dens_df_gc = dens_df_g1
dens_df_qc = dens_df_q1
dens_df_gc$value = dens_df_gc$value - dens_df_g0$value
dens_df_qc$value = dens_df_qc$value - dens_df_q0$value

plot8.1 = ggplot(dyad_list[2<dyad_list$number_of_trades,], aes(x = number_of_trades, y = gift)) +
  geom_raster(data = dens_df_g0, aes(fill = value), interpolate = FALSE, show.legend = FALSE)+
  xlab('') +  ylab('Social Coehsion (Gift)') + labs(title="Baseline Condition") +
  theme(plot.title = element_text(size = 8, face = "plain", hjust = 0.5, )) +
  scale_fill_gradient(low = "white", high = "#00bfc4") + scale_x_continuous(labels = NULL)

plot8.2 = ggplot(dyad_list[2<dyad_list$number_of_trades,], aes(x = number_of_trades, y = gift)) +
  geom_raster(data = dens_df_g1, aes(fill = value), interpolate = FALSE, show.legend = FALSE)+
  xlab('') +  ylab('') + labs(title="Reputation Condition") +
  theme(plot.title = element_text(size = 8, face = "plain", hjust = 0.5, )) +
  scale_fill_gradient(low = "white", high = "#f8766d") + scale_x_continuous(labels = NULL) +
  scale_y_continuous(labels = NULL) 

plot8.3 = ggplot(dyad_list[2<dyad_list$number_of_trades,], aes(x = number_of_trades, y = scq_total)) +
  geom_raster(data = dens_df_q0, aes(fill = value), interpolate = FALSE, show.legend = TRUE)+
  xlab('Number of Exchanges') + ylab('Social Coehsion (Questionnaire)') +
  scale_fill_gradient(low = "white", high = "#00bfc4") 

plot8.4 = ggplot(dyad_list[2<dyad_list$number_of_trades,], aes(x = number_of_trades, y = scq_total)) +
  geom_raster(data = dens_df_q1, aes(fill = value), interpolate = FALSE, show.legend = TRUE)+
  xlab('Number of Exchanges') +  ylab('') + scale_y_continuous(labels = NULL)  +
  scale_fill_gradient(low = "white", high = "#f8766d")

plot8.5 = ggplot(dyad_list[2<dyad_list$number_of_trades,], aes(x = number_of_trades, y = gift)) +
  geom_raster(data = dens_df_gc, aes(fill = value), interpolate = FALSE, show.legend = FALSE) +
  labs(title="Reputation Condition - Baseline Condition") + xlab('') + ylab('') +
  theme(plot.title = element_text(size = 8, face = "plain", hjust = 0.5, )) +
  scale_fill_gradient(low = "white", high = "black") + scale_x_continuous(labels = NULL) + scale_y_continuous(labels = NULL) 

plot8.6 = ggplot(dyad_list[2<dyad_list$number_of_trades,], aes(x = number_of_trades, y = scq_total)) +
  geom_raster(data = dens_df_qc, aes(fill = value), interpolate = FALSE, show.legend = TRUE) +
  xlab('Number of Exchanges') +  ylab('') + scale_fill_gradient(low = "white", high = "black") + scale_y_continuous(labels = NULL) 


ggarrange(plot8.1, plot8.2, plot8.5, plot8.3, plot8.4, plot8.6, ncol = 3, nrow = 2, heights = c(1, 1.3),
          common.legend = FALSE, legend = "bottom", labels = 'AUTO')
