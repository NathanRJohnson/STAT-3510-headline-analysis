full_data <- read.csv("/Users/skytruong/Documents/UoG-CS/Winter2024/STAT3510/Project/stat3510-headline-analysis/aggregated/aggregated_full.csv")
head(full_data)

# MODEL 1:
# add a column for total_negative count
total_negative <- full_data$negative_l + full_data$negative_r
full_data$total_negative <- total_negative
head(full_data)

# linear model on full data
full_plot <- plot(x=full_data$date_id, y=full_data$total_negative, xlab="date_id", ylab="count of negative news headlines", pch=19)
full_model <- lm(total_negative~date_id, data=full_data)
summary(full_model)
abline(full_model, col="red")

# check residuals plot of full model
par(mfrow=c(1,2))
qqnorm(full_model$residuals, pch=19, main=" ")
qqline(full_model$residuals)
plot(full_model$fitted.values, full_model$residuals, pch=19, xlab="Fitted Values", ylab="Residuals")
abline(h=5, col="red")


# MODEL 2:
# categorial variable plot
par(mfrow=c(1,2))
barplot(height=full_data$negative_l, names.arg=full_data$date_id, xlab="date_id", ylab="negative_l", col="blue")
barplot(height=full_data$negative_r, names.arg=full_data$date_id, xlab="date_id", ylab="negative_r", col="red")

library(reshape)
sliced_df <- full_data[, c("date_id", "negative_l", "negative_r")]
head(sliced_df)
long_data <- melt(sliced_df, id=c("date_id"))
head(long_data)

t_date_id <- rep(long_data$date_id, times=long_data$value)
t_negative <- rep(long_data$variable, times=long_data$value)

cat_data <- data.frame(date_id=t_date_id, negative=t_negative)
head(cat_data)

cat_data$negative_l <- as.factor(ifelse(cat_data$negative=="negative_l", "1", "0"))
cat_data$negative_r <- as.factor(ifelse(cat_data$negative=="negative_r", "1", "0"))
head(cat_data, 10)
tail(cat_data, 10)

cat_model <- lm(date_id~negative_l, data=cat_data)
summary(cat_model)





