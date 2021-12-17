####################################################
#                      example 3                   #
####################################################
# Original sample
x = c(2.6,3.16,0.8,1.19,0.1,1.14,1.73,1.73,2.72,1.05)

# Plot histogram of x to get a rough idea of the underlying distribution F 
hist(x)

# Let's fit a normal distribution to x. Hence the estimates of parameters mu and sigma are sample analogues
mu = mean(x)
sigma = sd(x)

#Add the fitted distribution curve to the histogram
curve(dnorm(x, mu, sigma), add = TRUE, col = "red")

# Number of bootstrap samples
B = 500

# Generating bootstrap samples from the estimated F i.e. normal and arranging in a matrix form. Each row is a sample
xb = matrix(rnorm(B*length(x), mu, sigma), nrow = B)

# Calculate T(F) for each B bootstrap sample
tb = sapply(1:B, function(b){return(median(xb[b,]))})

# Plot the histogram of the bootstrap estimates
hist(tb, xlab = "T(F)_hat", main = "Histogram of T(F)_hat")
# Mark the 95% confidence interval with two vertical red lines
abline(v = quantile(tb, probs = c(0.025, 0.975)), col = "red")

# Calculate the qualtile 95% confidence interval
quantile(tb, probs = c(0.025, 0.975))

# Calculate the normal 95% confidence interval
mean(tb) + c(-1.95, 1.95)*sd(tb)
