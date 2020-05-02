#load packages
library(readr)
library(psych)
library(Hmisc)
library(leaps)
library(car)
library(lm.beta)
library(reshape2)
library(tidyr)

#load in dataset
dx_data <- read_csv("~/Documents/Basketball Stats/Draft Predicting/dx_stats.csv")
View(dx_data)

g2017=subset(dx_data, pos == "Guard")
w2017=subset(dx_data, pos == "Wing")
b2017=subset(dx_data, pos == "Big")

df17g=as.data.frame(g2017[,c("Name", "age", "height","ncaaG",	
                                "ncaaMP",	"ncaaFGM",	"ncaaFGA",
                                "ncaaFGPER",	"ncaaM2PM",	"ncaa2PA",
                                "ncaa2PER",  "ncaa3PM",	"ncaa3PA",
                                "ncaa3PER", "ncaaFTM",	"ncaaFTA",
                                "ncaaFTPER", "ncaaTRB",	"ncaaAST",
                                "ncaaSTL","ncaaBLK", "ncaaPF",	
                                "ncaaTOV", "ncaaPTS")])

df17w=as.data.frame(w2017[,c("Name", "age", "height","ncaaG",	
                             "ncaaMP",	"ncaaFGM",	"ncaaFGA",
                             "ncaaFGPER",	"ncaaM2PM",	"ncaa2PA",
                             "ncaa2PER",  "ncaa3PM",	"ncaa3PA",
                             "ncaa3PER", "ncaaFTM",	"ncaaFTA",
                             "ncaaFTPER", "ncaaTRB",	"ncaaAST",
                             "ncaaSTL","ncaaBLK", "ncaaPF",	
                             "ncaaTOV", "ncaaPTS")])

df17b=as.data.frame(b2017[,c("Name", "age", "height","ncaaG",	
                             "ncaaMP",	"ncaaFGM",	"ncaaFGA",
                             "ncaaFGPER",	"ncaaM2PM",	"ncaa2PA",
                             "ncaa2PER",  "ncaa3PM",	"ncaa3PA",
                             "ncaa3PER", "ncaaFTM",	"ncaaFTA",
                             "ncaaFTPER", "ncaaTRB",	"ncaaAST",
                             "ncaaSTL","ncaaBLK", "ncaaPF",	
                             "ncaaTOV", "ncaaPTS")])

g2017$prednew=predict(new_guard_mod, df17g)
w2017$prednew=predict(new_wing_mod, df17w)
b2017$prednew=predict(new_big_mod, df17b)
class2017=rbind(g2017, w2017, b2017)
class2017$wjrank=rank(-class2017$prednew)
class2017$dxrank=rank(class2017$dxSpot)
class2017$rankdiff=class2017$dxrank-class2017$wjrank
View(class2017)


df17=as.data.frame(class2017[,c("Name", "age", "height","ncaaG",	
                             "ncaaMP",	"ncaaFGM",	"ncaaFGA",
                             "ncaaFGPER",	"ncaaM2PM",	"ncaa2PA",
                             "ncaa2PER",  "ncaa3PM",	"ncaa3PA",
                             "ncaa3PER", "ncaaFTM",	"ncaaFTA",
                             "ncaaFTPER", "ncaaTRB",	"ncaaAST",
                             "ncaaSTL","ncaaBLK", "ncaaPF",	
                             "ncaaTOV", "ncaaPTS")])


class2017$guardpred=predict(new_guard_mod, df17)
class2017$wingpred=predict(new_wing_mod, df17)
class2017$bigpred=predict(new_big_mod, df17)
View(class2017)

rcorr(class2017$wjrank, class2017$dxrank)


ggplot(class2017, aes(x=dxrank, y=wjrank))+
  geom_text(aes(label=Name),
            size=3)+
  geom_smooth(se=FALSE,
              method="loess")+
  scale_x_continuous("Draft Express Ranking")+
  scale_y_continuous("WISP Ranking")+
  ggtitle("2017 Draft Class")

ggplot(class2017, aes(x=dxrank, y=prednew))+
  geom_text(aes(label=Name),
            size=3)+
  geom_smooth(se=FALSE,
              method="loess")+
  scale_x_continuous("Draft Express Ranking")+
  scale_y_continuous("Predicted BPM")+
  ggtitle("2017 Draft Class")

#Check people in DX mock draft

inmock=subset(class2017, dxSpot < 61)
inmock$wjrank=rank(-inmock$prednew)
inmock$dxrank=rank(inmock$dxSpot)
inmock$rankdiff=inmock$dxrank-inmock$wjrank
View(inmock)
rcorr(inmock$dxrank, inmock$wjrank)
write.csv(inmock,"~/Documents/Basketball Stats/Draft Predicting/class_2017.csv")


ggplot(inmock, aes(x=dxrank, y=prednew))+
  geom_text(aes(label=Name),
            size=3.5)+
  geom_smooth(se=FALSE,
              method="lm")+
  scale_x_continuous("Draft Express Ranking")+
  scale_y_continuous("WISP Predicted BPM")+
  ggtitle("2017 Top 60")

ggplot(inmock, aes(x=dxrank, y=wjrank))+
  geom_text(aes(label=Name),
            size=3)+
  geom_abline(slope = 1, 
              intercept = 0,
              color = "blue")+
  scale_x_continuous("Draft Express Ranking")+
  scale_y_continuous("Model Ranking")+
  ggtitle("2017 Top 60")
