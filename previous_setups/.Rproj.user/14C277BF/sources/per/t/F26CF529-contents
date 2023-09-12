#this code calculates the biomass of mangrove trees based on the excel output of pyManga
#Emma Bouzanne, 07/06/2023

#tree output dateien einlesen und in Liste konvertieren

csv_files = list.files(path = 'TreeOutput/', pattern = "csv$", full.names = TRUE)

myfiles <- lapply(csv_files, read.delim)

#-------------------------------------------------------------------------------
#Dominik Loesung
volume_all <- lapply(myfiles, function(y) 
  apply(y, 1, FUN=function(x) as.numeric(x[9]) * pi * as.numeric(x[5]) + (2 * as.numeric(x[6]) + as.numeric(x[8]) + 0.5^0.5 * as.numeric(x[5]) * pi * as.numeric(x[7])^2 + as.numeric(x[10]) * pi * as.numeric(x[6])^2)))
  

mean_volume_all <- lapply(volume_all, mean)

#wie als csv exportieren?

#liste zu dataframe konvertieren
df_mean_volume <- as.data.frame(do.call(rbind, mean_volume_all))

#Spalte umbenennen
names(df_mean_volume)[1] <- 'mean_volume'

#exportieren
write.table(df_mean_volume,file = "meanvolume.csv" ,row.names=FALSE, col.names=FALSE)


