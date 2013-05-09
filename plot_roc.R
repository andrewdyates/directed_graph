library(calibrate)
# precision(ppv), x:recall(tpr)
# tpr, x:fpr
overall.ppv <- c("MIM"=0.706, "EDGE"=0.775, "PATH"=0.83)
overall.tpr <- c("MIM"=0.546, "EDGE"=0.469, "PATH"=0.742)
overall.fpr <- c("MIM"=0.515, "EDGE"=0.31, "PATH"=0.344)

# three colors, one for each model
# ppv, tpr, fpr for
# overall, pal1, meso(w), endo(w)
#(12 * 3 == 36 points)
colors <- c("MIM"="#E41A1C", "EDGE"="#377EB8", "PATH"="#4DAF4A")

# PR Plot
pdf("data/gold_pr_plot_overall.pdf", width=6, height=6)
plot(overall.ppv, overall.tpr, main="PR Plot (Overall)", xlab="precision (ppv) ", ylab="recall (tpr)", pch=19, xlim=c(0,1), ylim=c(0,1), col=colors)
textxy(overall.ppv, overall.tpr, labs=names(overall.tpr), cx = 1, dcol = "black", m = c(0, 0))
abline(a=1.0,b=-1.0, col="#999999", lty=2)
dev.off()

# ROC Plot
pdf("data/gold_roc_plot_overall.pdf", width=6, height=6)
plot(overall.fpr, overall.tpr, main="ROC Plot (Overall)", xlab="false positive (fpr)", ylab="recall (tpr)", pch=19, xlim=c(0,1), ylim=c(0,1), col=colors)
textxy(overall.fpr, overall.tpr, labs=names(overall.tpr), cx = 1, dcol = "black", m = c(0, 0))
abline(a=0,b=1.0, col="#999999", lty=2)
dev.off()


