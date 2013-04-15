M <- read.csv("data/gold.celegans.gse2180.M.csv", header=T, row.names=1, check.names=F)
CLS <- read.csv("data/gold.celegans.gse2180.cls.csv", header=T, row.names=1, check.names=F)
PCC <- read.csv("data/gold.celegans.gse2180.dcor.csv", header=T, row.names=1, check.names=F)
DCOR <- read.csv("data/gold.celegans.gse2180.pcc.csv", header=T, row.names=1, check.names=F)

to.graphvis(CLS, DCOR, th=0.3) {
}
