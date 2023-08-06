# load and install the packages -------------------------------------
if (!require("rjson")) install.packages("rjson")
if (!require("jsonlite")) install.packages("jsonlite")
if (!require("tidyverse")) install.packages("tidyverse")
if (!require("stringr")) install.packages("stringr")

library(rjson)
library(jsonlite)
library(tidyverse)
library(stringr)

# packageVersion('rjson')  # 0.2.21
# packageVersion('jsonlite')  # 0.2.21
# packageVersion('tidyverse')  # 1.3.2
# packageVersion('stringr')  # 1.4.1

args <- commandArgs(trailingOnly = TRUE)
fil_navn <- "xml"

# Set wd
PATH <- args[1]
NAME <- args[2]

setwd(PATH)

# Give the input file name to the function.
result <-  jsonlite::fromJSON(paste0(NAME, ".json"))

# Categories
categories <- result[["categories"]] %>%
  rename(category_id = id)

# Images
images <- result[["images"]]
images <- images %>%
  mutate(id = format(id, scientific = FALSE)) %>%
  rename(image_id = id)

# boxes
boxes <- result[["annotations"]]
boxes <- boxes %>%
  mutate(image_id = format(image_id, scientific = FALSE)) %>%
  rename(boxes_id = id) %>%
  select(!(segmentation)) %>%
  mutate(category_id = as.integer(ifelse(lengths(category_id)==1, 
                              as.character(category_id), 
                              str_match(as.character(category_id), 'id = ([0-9]+)')[,2])))
  
#View(categories)
#View(images)
#View(boxes)

# merging
full <- full_join(boxes, categories, by = "category_id")
full <- full_join(full, images, by = "image_id")

full <- full %>%
  mutate(name = ifelse(name == "@","title", name)) %>%
  #filter(name == "title" | name == "sub") %>%
  separate('bbox', c("left", "top", "right", "bottom"), sep=", ", extra="drop") %>%
  mutate(left = sub('^..', '', left)) %>%
  mutate(bottom = sub('.$', '', bottom))

# export csv
write.csv(full, paste0(fil_navn, ".csv"))


