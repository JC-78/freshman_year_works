####################################################
#                      example 4                   #
####################################################
# Original sample
x = c(2.6, 0.89, 1.6, 0.76, 1.01, 4.06, 0.17)

# Plot histogram of x to get a rough idea of the underlying distribution F
hist(x, freq = FALSE, ylim = c(0, 0.45))

# Let's fit a gamma distribution to x. Hence the estimates of parameters shape (alpha) and rate (beta) are sample analogues of methods of moments
meanx = mean(x)
varx = var(x)

alpha = meanx^2/varx
beta = meanx/varx

#Add the fitted distribution curve to the histogram
curve(dgamma(x, shape = alpha, rate = beta), add = TRUE, col = "red")

# Number of bootstrap samples
B = 500

# Generating bootstrap samples from the estimated F i.e. gamma and arranging in a matrix form. Each row is a sample
xb = matrix(rgamma(B*length(x), shape = alpha, rate = beta), nrow = B)

# Calculate T(F) for each B bootstrap sample
tb = sapply(1:B, function(b){return(mean(xb[b,]))})

# Plot the histogram of the bootstrap estimates
hist(tb, xlab = "T(F)_hat", main = "Histogram of T(F)_hat")
# Mark the 95% confidence interval with two vertical red lines
abline(v = quantile(tb, probs = c(0.025, 0.975)), col = "red")

# Calculate the qualtile 95% confidence interval
quantile(tb, probs = c(0.025, 0.975))

# Calculate the normal 95% confidence interval
mean(tb) + c(-1.95, 1.95)*sd(tb)

