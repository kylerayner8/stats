#Check classes

#load packages
library(readr)
library(psych)
library(Hmisc)
library(leaps)
library(car)
library(lm.beta)
library(reshape2)
library(tidyr)

#Class of 2016
class16=subset(totalplayers, Year == 2016)
rcorr(class16$prednew, class16$nbaBPM)
rcorr(class16$wjrank, class16$OverallPick)

ggplot(class16, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Predicted BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("2016 Draft")

class16$wjrank=rank(-class16$prednew)
class16$draftrank=rank(class16$OverallPick)
class16ranks=class16[,c("Name", "nbaBPM", "draftrank", "wjrank")]
class16L=gather(class16ranks, RankType, Rank, draftrank:wjrank)
ggplot(class16L, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(alpha=.1)+
  geom_text(aes(label=Name),
            size=2.5)+
  ggtitle("2016 Draft Slot vs Model ")+
  scale_x_continuous("Draft Ranking")+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","Model Rank")))+
  scale_y_continuous("Career BPM")

ggplot(class16, aes(y=draftrank, x=wjrank))+
  geom_abline(intercept=0,
              slope= 1)+
  geom_text(aes(label=Name),
            size=1.75)+
  ggtitle("2016 Draft Slot vs Model ")+
  scale_x_continuous("WISP Ranking")+
  scale_y_continuous("Draft Slot")

#class of 2015
class15=subset(totalplayers, Year == 2015)

ggplot(class15, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Predicted BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("2015 Draft")

class15$wjrank=rank(-class15$prednew)
class15$draftrank=rank(class15$OverallPick)
class15ranks=class15[,c("Name", "nbaBPM", "draftrank", "wjrank")]
class15L=gather(class15ranks, RankType, Rank, draftrank:wjrank)
ggplot(class15L, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(alpha=.1)+
  geom_text(aes(label=Name),
            size=1.75)+
  ggtitle("2015 Draft Slot vs Model ")+
  scale_x_continuous("Draft Ranking")+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","Model Rank")))+
  scale_y_continuous("Career BPM")

#class of 2014
class14=subset(totalplayers, Year == 2014)
View(class14)
write.csv(class14,"~/Documents/Basketball Stats/Draft Predicting/class_2014.csv")


ggplot(class14, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("WISP BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("2014 Draft")

class14$wjrank=rank(-class14$prednew)
class14$draftrank=rank(class14$OverallPick)
class14ranks=class14[,c("Name", "nbaBPM", "draftrank", "wjrank")]
class14L=gather(class14ranks, RankType, Rank, draftrank:wjrank)
ggplot(class14L, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(method="loess", 
              se=FALSE)+
  geom_text(aes(label=Name),
            size=2.5)+
  ggtitle("2014 Draft Slot vs Model ")+
  scale_x_continuous("Draft Ranking")+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","WISP Rank")))+
  scale_y_continuous("NBA Career BPM")

#Class of 2013
class13=subset(totalplayers, Year == 2013)

rcorr(class13$prednew, class13$nbaBPM)

ggplot(class13, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 2.5) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Predicted BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("2013 Draft")

class13$wjrank=rank(-class13$prednew)
class13$draftrank=rank(class13$OverallPick)
class13ranks=class13[,c("Name", "nbaBPM", "draftrank", "wjrank")]
class13L=gather(class13ranks, RankType, Rank, draftrank:wjrank)
ggplot(class13L, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(alpha=.1)+
  geom_text(aes(label=Name),
            size=1.75)+
  ggtitle("2013 Draft Slot vs Model ")+
  scale_x_continuous("Draft Ranking")+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","Model Rank")))+
  scale_y_continuous("Career BPM")

ggplot(class13, aes(y=prednew, x=OverallPick))+
  geom_smooth(alpha=.15)+
  geom_text(aes(label=Name),
            size=2.25)+
  ggtitle("2013 Draft Slot and Model Prediction")+
  scale_x_continuous("Draft Slot")+
  scale_y_continuous("Predicted BPM")


#class of 2012
class12=subset(totalplayers, Year == 2012)

ggplot(class12, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Predicted BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("2012 Draft")

class12$wjrank=rank(-class12$prednew)
class12$draftrank=rank(class12$OverallPick)
class12ranks=class12[,c("Name", "nbaBPM", "draftrank", "wjrank")]
class12L=gather(class12ranks, RankType, Rank, draftrank:wjrank)

ggplot(class12L, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(alpha=.1)+
  geom_text(aes(label=Name),
            size=1.75)+
  ggtitle("2012 Draft Slot vs Model ")+
  scale_x_continuous("Draft Ranking")+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","Model Rank")))+
  scale_y_continuous("Career BPM")

#Class of 2011
class11=subset(totalplayers, Year == 2011)

ggplot(class11, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Predicted BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("2011 Draft")

class11$wjrank=rank(-class11$prednew)
class11$draftrank=rank(class11$OverallPick)
class11ranks=class11[,c("Name", "nbaBPM", "draftrank", "wjrank")]
class11L=gather(class11ranks, RankType, Rank, draftrank:wjrank)
ggplot(class11L, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(alpha=.1)+
  geom_text(aes(label=Name),
            size=1.75)+
  ggtitle("2011 Draft Slot vs Model ")+
  scale_x_continuous("Draft Ranking")+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","Model Rank")))+
  scale_y_continuous("Career BPM")

#Class of 2010
class10=subset(totalplayers, Year == 2010)

ggplot(class10, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Predicted BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("2010 Draft")

class10$wjrank=rank(-class10$prednew)
class10$draftrank=rank(class10$OverallPick)
class10ranks=class10[,c("Name", "nbaBPM", "draftrank", "wjrank")]
class10L=gather(class10ranks, RankType, Rank, draftrank:wjrank)
ggplot(class10L, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(alpha=.1)+
  geom_text(aes(label=Name),
            size=1.75)+
  ggtitle("2010 Draft Slot vs Model ")+
  scale_x_continuous("Draft Ranking")+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","Model Rank")))+
  scale_y_continuous("Career BPM")

#Class of 08
class08=subset(totalplayers, Year == 2008)

ggplot(class08, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Predicted BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("2008 Draft")

class08$wjrank=rank(-class08$prednew)
class08$draftrank=rank(class08$OverallPick)
class08ranks=class08[,c("Name", "nbaBPM", "draftrank", "wjrank")]
class08L=gather(class08ranks, RankType, Rank, draftrank:wjrank)
ggplot(class08L, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(alpha=.1)+
  geom_text(aes(label=Name),
            size=1.75)+
  ggtitle("2008 Draft Slot vs Model ")+
  scale_x_continuous("Draft Ranking")+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","Model Rank")))+
  scale_y_continuous("Career BPM")

#class of 07
class07=subset(totalplayers, Year == 2007)

ggplot(class07, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Predicted BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("2007 Draft")

class07$wjrank=rank(-class07$prednew)
class07$draftrank=rank(class07$OverallPick)
class07ranks=class07[,c("Name", "nbaBPM", "draftrank", "wjrank")]
class07L=gather(class07ranks, RankType, Rank, draftrank:wjrank)
ggplot(class07L, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(alpha=.1)+
  geom_text(aes(label=Name),
            size=1.75)+
  ggtitle("2007 Draft Slot vs Model ")+
  scale_x_continuous("Draft Ranking")+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","Model Rank")))+
  scale_y_continuous("Career BPM")

#class of 06
class06=subset(totalplayers, Year == 2006)

ggplot(class06, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Predicted BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("2006 Draft")

class06$wjrank=rank(-class06$prednew)
class06$draftrank=rank(class06$OverallPick)
class06ranks=class06[,c("Name", "nbaBPM", "draftrank", "wjrank")]
class06L=gather(class06ranks, RankType, Rank, draftrank:wjrank)
ggplot(class06L, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(method= "lm",
              alpha=.1)+
  geom_text(aes(label=Name),
            size=2.5)+
  ggtitle("2006 Draft Slot vs Model ")+
  scale_x_continuous("Draft Ranking")+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","Model Rank")))+
  scale_y_continuous("Career BPM")

#allclasses
allclassrank=rbind(class06L, class07L, class08L, 
                   class10L, class11L, class12L, 
                   class13L, class14L, class15L,
                   class16L)

ggplot(allclassrank, aes(y=nbaBPM, x=Rank, color=RankType))+
  geom_smooth(method= "loess",
              alpha=.1)+
  geom_text(aes(label=Name),
            size=1.5)+
  ggtitle("2006-2016 Draft Slot vs WISP ")+
  scale_x_continuous("Draft Ranking", 
                     limits = c(1,50))+
  scale_color_discrete(name = "Ranking Type", 
                       label = (c("Draft Slot","WISP Rank")))+
  scale_y_continuous("Career BPM", limits = c(-12.5,7.5))


