####################################################
#                      example 2                   #
####################################################
# Original sample
x = c(2.46,0.89,1.6,2.76,1.01,3.06,0.17)

# Number of bootstrap samples
B = 500

# Generating bootstrap samples and arranging in a matrix form. Each row is a sample
xb = matrix(sample(size = B*length(x), x, replace = TRUE), nrow = B)

# Calculate T(F) for each B bootstrap sample
tb = sapply(1:B, function(b){return(median(xb[b,]))})

# Plot the histogram of the bootstrap estimates
hist(tb, xlab = "T(F)_hat", main = "Histogram of T(F)_hat")
# Mark the 80% confidence interval with two vertical red lines
abline(v = quantile(tb, probs = c(0.1, 0.9)), col = "red")

# Calculate the qualtile 80% and 95% confidence intervals
quantile(tb, probs = c(0.1, 0.9))
quantile(tb, probs = c(0.025, 0.975))

# Calculate the normal 95% and 90% confidence intervals
mean(tb) + c(-1.95, 1.95)*sd(tb)
mean(tb) + c(-1.65, 1.65)*sd(tb)