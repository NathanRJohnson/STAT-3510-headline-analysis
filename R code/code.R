full_data <- read.csv("/Users/skytruong/Documents/UoG-CS/Winter2024/STAT3510/Project/stat3510-headline-analysis/aggregated/aggregated_full.csv")
head(full_data)

attach(full_data)

# add a column for total_negative count
total_negative <- negative_l + negative_r
full_data$total_negative <- total_negative
head(full_data)

# linear model on full data
full_plot <- plot(x=date_id, y=(negative_l + negative_r), xlab="date_id", ylab="count of negative news headlines", pch=19)
full_model <- lm(total_negative~date_id)
summary(full_model)
abline(full_model, col="red")

# check residuals plot of full model
par(mfrow=c(1,2))
qqnorm(full_model$residuals, pch=19, main=" ")
qqline(full_model$residuals)
plot(full_model$fitted.values, full_model$residuals, pch=19, xlab="Fitted Values", ylab="Residuals")
abline(h=0, col="red")




detach(full_data)