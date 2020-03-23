
# custom packages
packages <- read.table("/root/packages.txt")

for (package in packages[,1]) {
  install.packages(package, repos='https://cran.rstudio.com/', Ncpus=4)
}
