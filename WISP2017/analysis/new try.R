#load packages
library(readr)
library(psych)
library(Hmisc)
library(leaps)
library(car)
library(lm.beta)
library(reshape2)
library(tidyr)
library(caseMatch)

#import data
draft_data <- read_csv("~/Documents/Basketball Stats/Draft Predicting/draft_data_updated.csv")
View(draft_data)

#create predicted TOs & PFs for guards
guards_have_PF=subset(draft_data, ncaaMP != "NA" & pos == "Guard" & ncaaPF != "NA")
guards_only_TO=subset(draft_data, ncaaMP != "NA"& pos == "Guard" & ncaaTOV != "NA" & is.na(ncaaPF))

df_g_onlyTO = as.data.frame(guards_only_TO[,c("Name", "age", "height","ncaaG",	
                                                   "ncaaMP",	"ncaaFGM",	"ncaaFGA",
                                                  "ncaaFGPER",	"ncaaM2PM",	"ncaa2PA",	
                                                   "ncaa2PER",  "ncaa3PM",	"ncaa3PA",	
                                                  "ncaa3PER", "ncaaFTM",	"ncaaFTA",
                                                  "ncaaFTPER", "ncaaTRB",	"ncaaAST",
                                                  "ncaaSTL", "ncaaBLK",	"ncaaPTS")])

guards_pf_mod=lm(ncaaPF~ncaaMP+ncaa2PA+ncaa2PER+
                   ncaa3PA+ncaaFTA+ncaaAST+
                   ncaaSTL+ncaaBLK+ncaaPTS, 
                 data=in_guards)
guards_only_TO$ncaaPF=predict(guards_pf_mod, df_g_onlyTO)

guards_no_TO=subset(draft_data, ncaaMP != "NA" 
                        & pos == "Guard" 
                        & is.na(ncaaTOV) 
                        & is.na(ncaaPF))

df_g_noTO = as.data.frame(guards_no_TO[,c("Name", "age", "height","ncaaG",	
                                                   "ncaaMP",	"ncaaFGM",	"ncaaFGA",
                                                   "ncaaFGPER",	"ncaaM2PM",	"ncaa2PA",	
                                                   "ncaa2PER",  "ncaa3PM",	"ncaa3PA",	
                                                   "ncaa3PER", "ncaaFTM",	"ncaaFTA",
                                                   "ncaaFTPER", "ncaaTRB",	"ncaaAST",
                                                   "ncaaSTL", "ncaaBLK",	"ncaaPTS")])

guards_no_TO$ncaaPF=predict(guards_pf_mod, df_g_noTO)
guards_to_mod=lm(ncaaTOV~age+ncaaMP+ncaa3PER+
                   ncaaFTM+ncaaFTA+ncaaFTPER+
                   ncaaAST+ncaaPTS, data=in_guards)

guards_no_TO$ncaaTOV=predict(guards_to_mod, df_g_noTO)

#combine guard datasets

guards=rbind(guards_have_PF,guards_only_TO,guards_no_TO)
View(guards)


#create predicted TOs & PFs for wings
wing_have_PF=subset(draft_data, ncaaMP != "NA" & 
                          pos == "Big" & 
                          ncaaPF != "NA" & 
                          height < 82 &
                          ncaa3PER != "NA")
wing_only_TO=subset(draft_data, ncaaMP != "NA" & 
                          pos == "Big" & 
                          ncaaTOV != "NA" & 
                          is.na(ncaaPF) &
                          height < 82 &
                          ncaa3PER != "NA")

df_w_onlyTO = as.data.frame(wing_only_TO[,c("Name", "age", "height","ncaaG",	
                                                   "ncaaMP",	"ncaaFGM",	"ncaaFGA",
                                                   "ncaaFGPER",	"ncaaM2PM",	"ncaa2PA",	
                                                   "ncaa2PER",  "ncaa3PM",	"ncaa3PA",	
                                                   "ncaa3PER", "ncaaFTM",	"ncaaFTA",
                                                   "ncaaFTPER", "ncaaTRB",	"ncaaAST",
                                                   "ncaaSTL", "ncaaBLK",	"ncaaPTS")])

big_pf_mod=lm(ncaaPF~height+ncaaMP+ncaa2PA+ncaaFTM+
                 ncaaFTA+ncaaFTPER+ncaaTRB+ncaaSTL, 
               data=in_big_full)
wing_only_TO$ncaaPF=predict(big_pf_mod, df_w_onlyTO)

wing_no_TO=subset(draft_data, ncaaMP != "NA" 
                        & pos == "Big" 
                        & is.na(ncaaTOV) 
                        & is.na(ncaaPF)
                        & height < 82 &
                        ncaa3PER != "NA")

df_w_noTO = as.data.frame(wing_no_TO[,c("Name", "age", "height","ncaaG",	
                                               "ncaaMP",	"ncaaFGM",	"ncaaFGA",
                                               "ncaaFGPER",	"ncaaM2PM",	"ncaa2PA",	
                                               "ncaa2PER",  "ncaa3PM",	"ncaa3PA",	
                                               "ncaa3PER", "ncaaFTM",	"ncaaFTA",
                                               "ncaaFTPER", "ncaaTRB",	"ncaaAST",
                                               "ncaaSTL", "ncaaBLK",	"ncaaPTS")])

wing_no_TO$ncaaPF=predict(big_pf_mod, df_w_noTO)
big_to_mod=lm(ncaaTOV~age+ncaaMP+ncaa2PA+
                ncaa3PA+ncaa3PM+ncaaFTM+
                ncaaAST+ncaaSTL+ncaaBLK, data=in_big)

wing_no_TO$ncaaTOV=predict(big_to_mod, df_w_noTO)

#combine datasets

wings=rbind(wing_have_PF,wing_only_TO,wing_no_TO)
View(wings)


#create predicted TOs & PFs for Bigs
big_have_PF=subset(draft_data, ncaaMP != "NA" &
                          pos == "Big" & 
                          ncaaPF != "NA" & 
                          height > 81)
big_only_TO=subset(draft_data, ncaaMP != "NA" 
                          & ncaaTOV != "NA" 
                          & is.na(ncaaPF) 
                          & height > 81)

df_b_onlyTO = as.data.frame(big_only_TO[,c("Name", "age", "height","ncaaG",	
                                                 "ncaaMP",	"ncaaFGM",	"ncaaFGA",
                                                 "ncaaFGPER",	"ncaaM2PM",	"ncaa2PA",	
                                                 "ncaa2PER",  "ncaa3PM",	"ncaa3PA",	
                                                 "ncaa3PER", "ncaaFTM",	"ncaaFTA",
                                                 "ncaaFTPER", "ncaaTRB",	"ncaaAST",
                                                 "ncaaSTL", "ncaaBLK",	"ncaaPTS")])

big_pf_mod=lm(ncaaPF~height+ncaaMP+ncaa2PA+ncaaFTM+
                ncaaFTA+ncaaFTPER+ncaaTRB+ncaaSTL, 
              data=in_big_full)
big_only_TO$ncaaPF=predict(big_pf_mod, df_b_onlyTO)

big_no_TO=subset(draft_data, ncaaMP != "NA" 
                      & is.na(ncaaTOV) 
                      & is.na(ncaaPF)
                      & height > 81)

df_b_noTO = as.data.frame(big_no_TO[,c("Name", "age", "height","ncaaG",	
                                             "ncaaMP",	"ncaaFGM",	"ncaaFGA",
                                             "ncaaFGPER",	"ncaaM2PM",	"ncaa2PA",	
                                             "ncaa2PER",  "ncaa3PM",	"ncaa3PA",	
                                             "ncaa3PER", "ncaaFTM",	"ncaaFTA",
                                             "ncaaFTPER", "ncaaTRB",	"ncaaAST",
                                             "ncaaSTL", "ncaaBLK",	"ncaaPTS")])

big_no_TO$ncaaPF=predict(big_pf_mod, df_b_noTO)
big_to_mod=lm(ncaaTOV~age+ncaaMP+ncaa2PA+
                ncaa3PA+ncaa3PM+ncaaFTM+
                ncaaAST+ncaaSTL+ncaaBLK, data=in_big)

big_no_TO$ncaaTOV=predict(big_to_mod, df_b_noTO)

bigs=rbind(big_have_PF, big_only_TO, big_no_TO)
#build analytic samples
new_guards=subset(guards, Year < 2016
                  & COLLEGE != "NA" 
                  & ncaaMP != "NA" 
                  & nbaMP > 0)

new_wings=subset(wings, Year < 2016 
                 & COLLEGE != "NA" 
                 & ncaaMP != "NA" 
                 & nbaMP > 0)

new_bigs=subset(bigs, Year < 2016 
                & COLLEGE != "NA" 
                & ncaaMP != "NA" 
                & nbaMP > 0)

#build guard model
newgset = regsubsets(nbaBPM~age*height+
                       ncaaMP+
                       ncaa2PA*ncaa2PER+
                       ncaa3PM*ncaa3PER+
                       ncaaFTM*ncaaFTPER+
                       ncaaTRB*ncaaAST+ncaaTRB*ncaaSTL+ncaaTRB*ncaaBLK+ncaaTRB*ncaaTOV+ncaaTRB*ncaaPF+
                       ncaaAST*ncaaSTL+ncaaAST*ncaaBLK+ncaaAST*ncaaTOV+ncaaAST*ncaaPF+
                       ncaaSTL*ncaaBLK+ncaaSTL*ncaaTOV+ncaaSTL*ncaaPF+
                       ncaaBLK*ncaaTOV+ncaaBLK*ncaaPF+
                       ncaaTOV*ncaaPF+
                       ncaaPTS,
                     data=new_guards, nbest=3)
plot(newgset,scale = "adjr2", main = "Adjusted R^2")

new_guard_mod=lm(nbaBPM~age*height
                 +ncaaFTM*ncaaFTPER
                 +ncaa3PM*ncaaSTL
                 +ncaaTRB*ncaaAST
                 +ncaaTRB*ncaaSTL
                 +ncaaTRB*ncaaPF
                 +ncaaAST*ncaaBLK,
                 data=new_guards)
summary(new_guard_mod)

#make wing model
newWset = regsubsets(nbaBPM~age*height+
                       ncaaMP+
                       ncaa2PA*ncaa2PER+
                       ncaa3PM*ncaa3PER+
                       ncaaFTM*ncaaFTPER+
                       ncaaTRB*ncaaAST+ncaaTRB*ncaaSTL+ncaaTRB*ncaaBLK+ncaaTRB*ncaaTOV+ncaaTRB*ncaaPF+
                       ncaaAST*ncaaSTL+ncaaAST*ncaaBLK+ncaaAST*ncaaTOV+ncaaAST*ncaaPF+
                       ncaaSTL*ncaaBLK+ncaaSTL*ncaaTOV+ncaaSTL*ncaaPF+
                       ncaaBLK*ncaaTOV+ncaaBLK*ncaaPF+
                       ncaaTOV*ncaaPF+
                       ncaaPTS,
                     data=new_wings, nbest=3)
plot(newWset,scale = "adjr2", main = "Adjusted R^2")

new_wing_mod=lm(nbaBPM~age*height
                +ncaaM2PM*ncaa2PER*ncaa3PA
                +ncaaTRB*ncaaAST
                +ncaaAST*ncaaBLK
                +ncaaSTL*ncaaPF
                +ncaaBLK*ncaaTOV
                +ncaaFTPER*ncaaTOV,
                data=new_wings)
summary(new_wing_mod)


#make Big Model
newBset = regsubsets(nbaBPM~age*height+
                       ncaaMP+
                       ncaa2PA*ncaa2PER+
                       ncaa3PM*ncaa3PER+
                       ncaaFTM*ncaaFTPER+
                       ncaaTRB*ncaaAST+ncaaTRB*ncaaSTL+ncaaTRB*ncaaBLK+ncaaTRB*ncaaTOV+ncaaTRB*ncaaPF+
                       ncaaAST*ncaaSTL+ncaaAST*ncaaBLK+ncaaAST*ncaaTOV+ncaaAST*ncaaPF+
                       ncaaSTL*ncaaBLK+ncaaSTL*ncaaTOV+ncaaSTL*ncaaPF+
                       ncaaBLK*ncaaTOV+ncaaBLK*ncaaPF+
                       ncaaTOV*ncaaPF+
                       ncaaPTS,
                     data=new_bigs, nbest=3)
plot(newBset,scale = "adjr2", main = "Adjusted R^2")

new_big_mod=lm(nbaBPM~age+
               +ncaa3PA
               +ncaa2PER*ncaaSTL
               +ncaaTRB*ncaaBLK
               +ncaaAST*ncaaSTL
               +ncaaSTL*ncaaBLK
               +ncaaSTL*ncaaPF
               +ncaaTOV*ncaaPF,
               data=new_bigs)
summary(new_big_mod)




#Run for all players
guards$prednew=predict(new_guard_mod, guards)
guards$pos=c("Guard")
wings$prednew=predict(new_wing_mod, wings)
wings$pos=c("Wing")
bigs$prednew=predict(new_big_mod, bigs)
bigs$pos=c("Big")

totalplayers=rbind(guards,wings,bigs)
totalplayers$guardpred=predict(new_guard_mod, totalplayers)
totalplayers$wingpred=predict(new_wing_mod, totalplayers)
totalplayers$bigpred=predict(new_big_mod, totalplayers)
View(totalplayers)

#check out of sample
out_sample=subset(totalplayers, ncaaMP != "NA," & Year == 2016)
View(out_sample)

playersnba=subset(totalplayers, nbaMP > 1000)
View(playersnba)
rcorr(totalplayers$prednew, totalplayers$nbaBPM)
rcorr(playersnba$prednew, playersnba$nbaBPM)
lottoAll=subset(totalplayers, OverallPick < 15)
FirstRound=subset(totalplayers, OverallPick < 31 & prednew < 10)
rcorr(FirstRound$prednew, FirstRound$nbaBPM)

ggplot(playersnba, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Predicted BPM") +
  scale_y_continuous("Actual BPM") +
  ggtitle("Drafted Players Players 2006-2016")

ggplot(class16, aes(x=OverallPick, y=prednew))+
  geom_text(aes(label= Name), size = 3) +
  geom_smooth(method="lm",
              se=TRUE,
              alpha=.2)+
  scale_x_continuous("Draft Position") +
  scale_y_continuous("Predicted BPM") +
  ggtitle("2016 Draft")



View(ben)
dropvars=names(totalplayers[c(1:3,6:10,19,30:49)])
matchben <- case.match(data=totalplayers, match.case="Ben Simmons",
                     id.var="Name",leaveout.vars=dropvars,
                     distance="mahalanobis",
                     number.of.matches.to.return=5)






#########
#run tables for article:

new_guards$prednew=predict(new_guard_mod, new_guards)
new_guards$pos=c("Guard")
View(new_guards)
write.csv(new_guards, "~/Documents/Basketball Stats/Draft Predicting/in_guards.csv")


ggplot(new_guards, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label=Name),
            size=2.5)+
  geom_smooth(method="lm",
              se=FALSE)+
  ggtitle("In-Sample Guards")+
  scale_x_continuous("WISP-Predicted BPM")+
  scale_y_continuous("Actual NBA BPM",
                     limits=c(-10, 7.5))
  
new_wings$prednew=predict(new_wing_mod, new_wings)
new_wings$pos=c("Wing")
View(new_wings)
write.csv(new_wings, "~/Documents/Basketball Stats/Draft Predicting/in_wings.csv")


ggplot(new_wings, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label=Name),
            size=2.5)+
  geom_smooth(method="lm",
              se=FALSE)+
  ggtitle("In-Sample Wings")+
  scale_x_continuous("WISP-Predicted BPM",
                     limits=c(-8,3))+
  scale_y_continuous("Actual NBA BPM",
                     limits=c(-10, 7.5))

new_bigs$prednew=predict(new_big_mod, new_bigs)
new_bigs$pos=c("Big")
View(new_bigs)
write.csv(new_bigs, "~/Documents/Basketball Stats/Draft Predicting/in_bigs.csv")


ggplot(new_bigs, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label=Name),
            size=2.5)+
  geom_smooth(method="lm",
              se=FALSE)+
  ggtitle("In-Sample Bigs")+
  scale_x_continuous("WISP-Predicted BPM")+
  scale_y_continuous("Actual NBA BPM",
                     limits=c(-10,5))

all_in=rbind(new_guards, new_wings, new_bigs)
View(all_in)
write.csv(all_in, "~/Documents/Basketball Stats/Draft Predicting/in_all2.csv")

ggplot(all_in, aes(x=prednew, y=nbaBPM))+
  geom_text(aes(label=Name),
            size=2.5)+
  geom_smooth(method="lm",
              se=FALSE)+
  ggtitle("All In-Sample Players")+
  scale_x_continuous("WISP-Predicted BPM",
                     limits = c(-7.5, 5))+
  scale_y_continuous("Actual NBA BPM",
                     limits = c(-10, 7.5))


#check all stats
only500=subset(totalplayers, nbaMP > 500& nba3PER > 0)
rcorr(only500$ncaaFGPER, only500$nbaFGPER)
rcorr(only500$ncaa3PER, only500$nba3PER)
rcorr(only500$ncaaFTPER, only500$nbaFTPER)
rcorr(only500$ncaaTRB, only500$nbaTRB_G)
rcorr(only500$ncaaAST, only500$nbaAST_G)
rcorr(only500$ncaaPTS, only500$nbaPTS_G)



