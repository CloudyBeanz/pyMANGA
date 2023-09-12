# @Emma: Du brauchst auch das data.table package. Ich benutze es an
# zwei stellen, weil es daten schneller einliest und zusammenpack.
# das siehst du dann immer wenn data.table::
library(tidyverse)
library(data.table)
library(tidyr)

# list all csv files that are inside a folder and all subfolders ----------
# @Emma: change folder to model_output
file_list <- list.files("model_output/",
  full.names = TRUE,
  recursive = TRUE,
  pattern = ".csv"
)

# Read all files in a list
tree_files <- lapply(file_list, data.table::fread)

# name each file in the list according to their names in the folder
names(tree_files) <- file_list

# bind all tables together and give them an ID column called file_id
tree_table <- data.table::rbindlist(tree_files, idcol = "file_id")

tree_table <- tree_table %>% drop_na()

# Extract all the necessary information from the file_id column and put it in
# separate columns
tree_table <- tree_table %>%
  # extract everything followed by after t_ and before .0.csv
  # @Emma: but maybe you can remove this because there is already a time column that
  # has this information
  mutate(timestep = str_extract(file_id, "(?<=t_).*(?=.0.csv)")) %>% 
  # extract everything followed by after previous_setups/ and before /FS_100
  # @Emma: this is a dummy to extract the model type from the file name, you need
  # to adjust this to your actual file structure
  mutate(module_type = str_extract(file_id, "(?<=model_output//).*(?=/Population_t_)")) %>%
  # @Emma: you need to do something similar for the tree_composition, this is just
  # a placeholder
  separate_wider_delim(module_type, "_", names = c("module_type", "tree_comp", "wdh"))
  #mutate(tree_composition = str_extract(file_id, "(?<=model_output//).*(?=/Population_t_)")) %>%
  # separate the tree column into tree_species and tree_id
  separate(tree, into = c("tree_species", "tree_id"), sep = "_") %>%
  # add a segment column based on x-value
  mutate(segment = case_when(
    x <= 10 ~ 1,
    x > 10 & x <= 20 ~ 2,
    x > 20 & x <= 30 ~ 3,
    x > 30 & x <= 40 ~ 4,
    .default = 5
  )) %>%
  # calculate the biomass of each tree
  # @Emma: Adapt the formula and double check
tree_table <- tree_table %>%  
  mutate(biomass = h_root * pi * r_root^2 + (2 * r_crown + h_stem + 0.5^0.5 * r_root)
  * pi * r_stem^2 + h_crown * pi * r_crown^2)

# function to summarize the data per
# timestep, tree_species, segment, model_type and tree composition
tree_summary <- tree_table %>%
  group_by(time, tree_species, segment, module_type, tree_composition, wdh) %>%
  summarise(
    biomass = mean(biomass, na.rm = TRUE),
    tree_height = mean(h_stem, na.rm = TRUE)
  )
