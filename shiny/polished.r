
# setting up requisites
install.packages("remotes", repos="http://cran.mirror.garr.it/mirrors/CRAN/", Ncpus=4)

# https://github.com/Tychobra/polished#polished-installation
remotes::install_github("tychobra/tychobratools", repos="http://cran.mirror.garr.it/mirrors/CRAN/", Ncpus=4)
remotes::install_github("tychobra/polished", repos="http://cran.mirror.garr.it/mirrors/CRAN/", Ncpus=4)
