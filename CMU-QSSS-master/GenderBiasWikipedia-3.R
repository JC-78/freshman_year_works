## Filename: GenderBiasWikipedia
## Purpose : provide helper tools for investigating contents of 
##         : wikipedia articles


#### clear workspace; load libraries ####
rm(list = ls())
library(tidyverse)



#### background ####

## reference site -- this link randomly selects a wikipedia page about 
 # a living person:
site = "https://en.wikipedia.org/wiki/Special:RandomInCategory/Living_people"


## Overview: 
 # we're going to procede by 
 # (1) reading in the html for a random wikipedia page
 # (2) grabbing the name of the person the page is about (from the raw HTML)
 # (3) doing a little cleaning to extract the paragraphs that are about 
 #     that person
 # (4) 


#### helper functions ####

## extract.title: (helpful for step (1))
##   input: raw HTML for a wikipedia article
##   output: the name of the person the article is about

    extract.title = function(lns){
      cut.1 = lns[grep(lns, pattern = "<title>")]
      cut.2 = gsub("</?title>","",cut.1)
      cut.3 = gsub(" - Wikipedia, the free encyclopedia","",cut.2)
      cut.4 = gsub(pattern = " - Wikipedia", replacement = "", x= cut.3)
      return(cut.4)
    }


## (This is a set of functions you'll run as a big chunk)
## these take raw HTML as an input, and (together) extract
## the paragraphs and conduct some light cleaning. (helpful for steps (1) - (3))

    extract.p = function(lns){
      cut.1 = lns[grep(lns, pattern = "<p>")]
      cut.2 = tolower(cut.1)
      return(cut.2)
    }
    
    par.cleaner = function(str){
      cut.1 = gsub(str, pattern = "<a href.+?>", replacement = "")
      cut.2 = gsub(cut.1, pattern = "</a>", replacement = "")
      cut.3 = gsub(cut.2, pattern = "<p>", replacement = "")
      cut.4 = gsub(cut.3, pattern = "</p>", replacement = "")
      cut.5 = gsub(cut.4, pattern = "<b>", replacement = "")
      cut.6 = gsub(cut.5, pattern = "</b>", replacement = "")
      cut.7 = gsub(cut.6, pattern = "<i>", replacement = "")
      cut.8 = gsub(cut.7, pattern = "</i>", replacement = "")
      cut.9 = gsub(cut.8, pattern = "<sup.+?>", replacement = "")
      cut.10 = gsub(cut.9, pattern = "</sup>", replacement = "")
      cut.11 = gsub(cut.10, pattern = "\"", replacement = "")
      cut.12 = gsub(cut.11, pattern = "\\(", replacement = "")
      cut.13 = gsub(cut.12, pattern = "\\)", replacement = "")
      cut.14 = gsub(cut.13, pattern = "\\.", replacement = "")
      cut.15 = gsub(cut.14, pattern = ",", replacement = "")
      
      return(cut.15)
    }
    
    par.remover = function(str){
      char.counter = sapply(str, nchar)
      str.out = str[which(char.counter > 0)]
      return(str.out)
    }
    
    par.combiner = function(str){
      out = paste(str, collapse = " ")
      return(out)
    }

## Functions for 


count.em = function(cln.in,str){
  adj = paste(" ",str," ",sep = "")
  hits.ind <- gregexpr(adj, cln.in)
  test = regmatches(x = cln.in, m = hits.ind)
  #hits = unlist(test)
  out = length(unlist(test))
  return(out)
}

year.extractor = function(cln.in){
  hits.ind <- gregexpr(pattern = " [0-9]{4} ", cln.in)
  test = regmatches(x = cln.in, m = hits.ind)
  cut.1 = as.numeric(unlist(test))
  if(length(cut.1) == 0){return(NA)}
  return(cut.1)
}


bday.extractor = function(cln.in){
  born.hit1 = regexpr(cln.in, pattern = "born")[[1]][1]
  sub.string = substr(cln.in,born.hit1,born.hit1 + 30)
  out = year.extractor(sub.string)[1]
  return(out)
}

# example: 

site = "https://en.wikipedia.org/wiki/Special:RandomInCategory/Living_people"

cur.lns = readLines(site) 
extract.title(cur.lns)

cur.words = cur.lns %>% 
  extract.p(.) %>% 
  par.cleaner(.) %>%
  par.remover(.) %>%
  par.combiner(.)

count.em(cur.words,"he")

bday.extractor(cur.words)

nchar(cur.words)

year.extractor(cur.words)

q1.func=function(cl.in){
  cur.df=data.frame(the.count=count.em(cl.in,'the'),an.count=count.em(cl.in,"an"))
  return(cur.df)
}

q1.func(cur.words)

q2.func=function(cl.in){
  cur.df=data.frame(he.count=count.em(cl.in,'he'),she.count=count.em(cl.in,"she"))
  return(cur.df)
}

q2.func(cur.words)


q4.func=function(){
  site = "https://en.wikipedia.org/wiki/Special:RandomInCategory/Living_people"
  cur.lns = readLines(site) 
  title=extract.title(cur.lns)
  cur.words = cur.lns %>% 
    extract.p(.) %>% 
    par.cleaner(.) %>%
    par.remover(.) %>%
    par.combiner(.)
  result = q2.func(cur.words)
  result$title = title
  result$tot.words = nchar(cur.words)
  result$outcome = 0
  result$birth= bday.extractor(cur.words)
  if (result$he.count>result$she.count){result$outcome=1} 
  if (result$he.count<result$she.count){result$outcome=-1}
  return (result)
}

q4.func()

base = q4.func()
for (i in 1:499){
  cur=q4.func()
  base=rbind(base,cur)
  print(i)
}
base
view(base)
write.csv(base,file="/users/joonghochoi/desktop/gender_bias_wiki.csv")

answer=read.csv(file="/users/joonghochoi/desktop/gender_bias_wiki.csv")
head(answer)
final=answer%>%
  group_by(outcome)%>%
  summarize (pct=n() /nrow(answer))
final
  
final2=answer%>%
  group_by(outcome)%>%
  summarize(avgLength=mean(tot.words,na.rm=TRUE))

head(final2)


answer %>%
  mutate(decade = floor(birth/10)*10) %>%
  group_by(outcome, decade) %>%
  summarize(avgLength=mean(tot.words,na.rm=TRUE))%>%
  ggplot(aes(x=decade,y=avgLength, col = factor(outcome))) +
  geom_point() + geom_line()

answer %>%
  ggplot(.,aes(x = birth, y = tot.words, col = factor(outcome))) + geom_point() 

#The article lengths for men and women both change over time. While the article length for female
#is higher than men from 1920 to around 1930 and from 1970 to 1990, the article length for men is
#higher during other yars. Thus, according to the graph, the gender imbalance is changing over time. 




