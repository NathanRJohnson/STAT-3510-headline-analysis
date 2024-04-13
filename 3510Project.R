
setwd("C:\\Users\\15195\\Documents")
data = read.csv("aggregated_undersampled.csv")
View(data)

data$tot_neg = (data$negative_l + data$negative_r)
X1 = as.Date(data$date)
Y = data$tot_neg

pre_covid_mod = glm( Y ~ X1, subset=data$pre_covid==0, family = poisson)
post_covid_mod = glm( Y ~ X1, subset=data$pre_covid==1, family = poisson)

summary(pre_covid_mod)
summary(post_covid_mod)

library(MASS)

pre_covid_mod_nb = glm.nb( Y ~ X1, subset=data$pre_covid==0, maxit=1000)
post_covid_mod_nb = glm.nb( Y ~ X1, subset=data$pre_covid==1, maxit=1000)

summary(pre_covid_mod_nb)

plot(X1, Y)

# plot pre covid
pre_points <- seq(as.Date("2018-01-01"),as.Date("2019-11-30"),by="1 day") #seq(from=0, to=50, length.out=10000)
#pre_mod_vec <- pre_covid_mod$coefficients[1] + pre_covid_mod$coefficients[2] * pre_points
f <- data.frame(X1=pre_points)
pre_y_vec <- predict(pre_covid_mod, f, type="response")

post_points <- seq(as.Date("2019-12-01"),as.Date("2021-12-31"),by="1 day")
f <- data.frame(X1=post_points)
post_y_vec <- predict(post_covid_mod, f, type="response")

library(tidyverse)

ggplot(data, aes(x = X1, y = Y)) +
  geom_point() +
  geom_line(data=data.frame(x=pre_points, y=pre_y_vec), aes(x=pre_points, y=pre_y_vec), size=2, color="darkgreen") +
  geom_line(data=data.frame(x=post_points, y=post_y_vec), aes(x=post_points, y=post_y_vec), size=2, color="darkgreen") +
  geom_vline(xintercept = as.Date("2019-11-30"), linetype="dotdash", color="black") +
  geom_text(x=as.Date("2019-11-30"), y=10.5, size=6, label="Covid-19 Begins", vjust=-1, color="black") +
  labs(x = "Date", y = "Number of Negative Headlines", title = "Number of Negative Headlines: Pre vs Post Covid-19", subtitle = "poisson regression") + # Labels
  theme_bw() +
  theme(plot.background = element_rect(fill = "#b3cbd3"), axis.title = element_text(size = 18), axis.text = element_text(size = 14), plot.title = element_text(size = 20))


## without binary term
detach(data)
split_data = read.csv("split_aggregated.csv")
attach(split_data)
View(split_data)

id_total <- c()
for (i in 0:99) {
  id_total[i+1] = split_data[2*i+1, 'count'] + split_data[2*i+2, 'count']
}


BIAS = as.factor(is_r)
X1 = as.Date(date)

# Pre-covid w/o BIAS
pre_covid_mod_a = glm( count ~ X1, subset=pre_covid==0, family = poisson, data=split_data)
summary(pre_covid_mod_a)

# Pre-covid w/ BIAS
pre_covid_mod_b = glm( count ~ X1 + BIAS, subset=pre_covid==0, family = poisson, data=split_data)
summary(pre_covid_mod_b)

# Post-covid w/o BIAS
post_covid_mod_a = glm( count ~ X1, subset=pre_covid==1, family = poisson, data=split_data)
summary(post_covid_mod_a)

# Post-covid w/ BIAS
post_covid_mod_b = glm( count ~ X1 + BIAS, subset=pre_covid==1, family = poisson, data=split_data)
summary(post_covid_mod_b)

timeless_mod <- glm(count ~ BIAS, subset=pre_covid==1, family=poisson, data=split_data)
summary(timeless_mod)

# Deviance Tests
#pre_deviance_test <- anova(pre_covid_mod_a, pre_covid_mod_b, test = "Chisq")
#pre_deviance_test

#post_deviance_test <- anova(post_covid_mod_a, post_covid_mod_b, test = "Chisq")
#post_deviance_test

f <- data.frame(X1=pre_points, BIAS=as.factor(rep(0, 699)))
pre_l_y_vec <- predict.glm(pre_covid_mod_b, f, type="response")

f <- data.frame(X1=pre_points, BIAS=as.factor(rep(1, 699)))
pre_r_y_vec <- predict.glm(pre_covid_mod_b, f, type="response")


f <- data.frame(X1=post_points, BIAS=as.factor(rep(0, 762)))
post_l_y_vec <- predict.glm(post_covid_mod_b, f, type="response")
f <- data.frame(X1=post_points, BIAS=as.factor(rep(1, 762)))
post_r_y_vec <- predict.glm(post_covid_mod_b, f, type="response")

length(factor(is_r))
length(X1)
scatter_points <- data.frame(x = X1, y = id_total)

attach(split_data)

split_data$color = ifelse(split_data$is_r == 0, "Liberal", "Conservative")

ggplot(split_data, aes(x = X1, y = count)) + #shape=factor(is_r),
  geom_point(data=split_data, aes(x = X1, y = count, color=color, shape=factor(is_r))) +
  scale_shape_manual(values = c(16, 17)) +  # Change shape based on category
  scale_color_manual(values = c("Liberal"="darkblue", "Conservative"="darkred"), name = "BIAS", labels=c("Liberal", "Conservative")) +  # Change color based on category
  
  geom_line(data=data.frame(x=pre_points, y=pre_l_y_vec), size=2, aes(x=pre_points, y=pre_l_y_vec), color="blue") +
  geom_line(data=data.frame(x=post_points, y=post_l_y_vec), size=2, aes(x=post_points, y=post_l_y_vec), color="blue") +
  geom_line(data=data.frame(x=pre_points, y=pre_r_y_vec), size=2, aes(x=pre_points, y=pre_r_y_vec), color="red") +
  geom_line(data=data.frame(x=post_points, y=post_r_y_vec), size=2, aes(x=post_points, y=post_r_y_vec), color="red") +
  geom_vline(xintercept = as.Date("2019-11-30"), linetype="dotdash", color="black") +
  geom_text(x=as.Date("2019-11-30"), y=2.5, size=6, label="Covid-19 Begins", vjust=-1, color="black") +
  
  labs(x = "Date ID", y = "Number of Negative Headlines", title = "Number of Negative Headlines: Pre vs Post Covid-19", subtitle = "poisson regression with bias category") + # Labels
  guides(shape=FALSE, color = guide_legend(title = "Bias", override.aes = list(shape = c(16, 17), color = c("darkblue", "darkred"), labels = c("Liberal", "Conservative")))) +
  theme_bw() +
  theme(plot.background = element_rect(fill = "#b3cbd3"), axis.title = element_text(size = 18), axis.text = element_text(size = 14), plot.title = element_text(size = 20), legend.title = element_text(size = 16), legend.text = element_text(size = 12))

#plot(data$date_id, (data$negative_r / data$total_r))
#plot(data$date_id, (data$negative_l / data$total_l))


## RATE MODELS -----------------------------------------------------------------
setwd("C:\\Users\\15195\\Documents")
full_df = read.csv("aggregated_full.csv")
View(full_df)

full_df$tot_neg = (full_df$negative_l + full_df$negative_r)
DATE = as.Date(full_df$date)
Y = full_df$tot_neg

# 
pre_covid_mod = glm( Y ~ offset(log(full_df$total))+DATE, subset=full_df$pre_covid==0, family = poisson, data=full_df)
summary(pre_covid_mod)
post_covid_mod = glm( Y ~ offset(log(total))+DATE, subset=full_df$pre_covid==1, family = poisson, data=full_df)
summary(post_covid_mod)

# ---------- ## WITH BIAS ## -------------------------------
split_full_df = read.csv("split_bias_full.csv")
attach(split_full_df)
View(split_full_df)
Y = split_full_df$n_count
BIAS = as.factor(split_full_df$is_r)
DATE = as.Date(split_full_df$date)


pre_covid_a_mod = glm( Y ~ DATE, subset=split_full_df$pre_covid==0, family = poisson, data=split_full_df)
summary(pre_covid_a_mod)

pre_covid_b_mod = glm( Y ~ DATE + BIAS, subset=split_full_df$pre_covid==0, family = poisson, data=split_full_df)
summary(pre_covid_b_mod)

pre_covid_c_mod = glm( Y ~ offset(log(t_count))+DATE, subset=split_full_df$pre_covid==0, family = poisson, data=split_full_df)
summary(pre_covid_c_mod)

pre_covid_d_mod = glm( Y ~ offset(log(t_count))+DATE + BIAS, subset=split_full_df$pre_covid==0, family = poisson, data=split_full_df)
summary(pre_covid_d_mod)

split_cred_df = read.csv("split_cred_full.csv")
View(split_cred_df)
Y = split_cred_df$n_count
CRED = as.factor(split_cred_df$is_high)
DATE = as.Date(split_full_df$date)
pre_covid_e_mod = glm( Y ~ offset(log(d_count))+ DATE + CRED, subset=split_cred_df$pre_covid==0, family = poisson, data=split_cred_df)
summary(pre_covid_e_mod)


post_covid_a_mod = glm( Y ~ DATE, subset=split_full_df$pre_covid==1, family = poisson, data=split_full_df)
summary(post_covid_a_mod)

post_covid_b_mod = glm( Y ~ DATE + BIAS, subset=split_full_df$pre_covid==1, family = poisson, data=split_full_df)
summary(post_covid_b_mod)

post_covid_c_mod = glm( Y ~ offset(log(t_count))+DATE, subset=split_full_df$pre_covid==1, family = poisson, data=split_full_df)
summary(post_covid_c_mod)

post_covid_d_mod = glm( Y ~ offset(log(t_count))+DATE + BIAS, subset=split_full_df$pre_covid==1, family = poisson, data=split_full_df)
summary(post_covid_d_mod)

View(split_cred_df)
Y = split_cred_df$n_count
CRED = as.factor(split_cred_df$is_high)
DATE = as.Date(split_full_df$date)
post_covid_e_mod = glm( Y ~ offset(log(d_count))+ DATE + CRED, subset=split_cred_df$pre_covid==1, family = poisson, data=split_cred_df)
summary(post_covid_e_mod)

X1 <- split_full_df$date_id
X2 <- c()
for (i in 1:length(split_full_df$date_id)){
  if (split_full_df$date_id[i] < 50) {
    X2[i] <- 0
  } else {
    X2[i] <- date_id[i] - 50
  }
}


summary(pre_covid_c_mod)
summary(post_covid_c_mod)

pre_points <- seq(as.Date("2018-01-01"),as.Date("2019-11-30"),by="1 day") #seq(from=0, to=50, length.out=10000)
#pre_mod_vec <- pre_covid_mod$coefficients[1] + pre_covid_mod$coefficients[2] * pre_points
t_counts = rep(mean(split_full_df$t_count), times=length(pre_points))
f <- data.frame(t_count=t_counts,DATE=pre_points)
pre_y_vec <- predict(pre_covid_c_mod, f, type="response")

post_points <- seq(as.Date("2019-12-01"),as.Date("2021-12-31"),by="1 day")
t_counts = rep(mean(split_full_df$t_count), times=length(post_points))
f <- data.frame(t_count=t_counts, DATE=post_points)
post_y_vec <- predict(post_covid_c_mod, f, type="response")

library(tidyverse)

ggplot(split_full_df, aes(x = DATE, y = Y)) +
  geom_point() +
  geom_line(data=data.frame(x=pre_points, y=pre_y_vec), aes(x=pre_points, y=pre_y_vec), size=2, color="darkgreen") +
  geom_line(data=data.frame(x=post_points, y=post_y_vec), aes(x=post_points, y=post_y_vec), size=2, color="darkgreen") +
  geom_vline(xintercept = as.Date("2019-11-30"), linetype="dotdash", color="black") +
  geom_text(x=as.Date("2019-11-30"), y=10.5, size=6, label="Covid-19 Begins", vjust=-1, color="black") +
  labs(x = "Date", y = "Number of Negative Headlines", title = "Number of Negative Headlines: Pre vs Post Covid-19", subtitle = "poisson regression") + # Labels
  theme_bw() +
  theme(axis.title = element_text(size = 18), axis.text = element_text(size = 14), plot.title = element_text(size = 20))

