%{
Cameron Beck Group number (a_assign): 42
Harrison Hall,Grayson Eng, Christopher Graham
File name: assign10.m
COMP1200 - Spring 2020
Due Date: Apr 17, 2020
We used & and | from iclicker questions to add
parameters, as well as contains from the worksheet in  order to search by
multiple variables. Besides that, the help command was used to determine
how to use pie
Sort AU softball games by two parameters then from there print season
statistics and a pie graph
%}

clc, clear all
format short

%***** CONSTANTS *****
FILENAME = 'assign10_2019_SB_season.txt' ;

%Check to see if file exists
if ~exist(FILENAME, 'file')
    disp('File not available')
end

%***** INPUT *****

%Read the text file for data and input into matricies
[dates(:,1),dates(:,2),sec, location, scores(:,1),scores(:,2)]=textread('assign10_2019_SB_season.txt','%d%d%s%s%*s%f%f%*f%*f%*f%*f');
%Find number of games
games = length(dates);
%Find out of division home games
home = find(contains(sec, 'x') & contains(location, 'jm')); %find by location and division
for i = home
        homeAU = [dates(i,:),scores(i,1)];
        homeOP = [dates(i,:),scores(i,2)];    
end

%Find out of division away games
away = find(contains(sec, 'x') & contains(location, 'at') | contains(location, 'gs') | contains(location, 'fc'));
for i = away
        awayAU = [dates(i,:),scores(i,1)];
        awayOP = [dates(i,:),scores(i,2)];    
end

%Find SEC home games
SEChome = find(contains(sec, 'sec') & contains(location, 'jm'));
for i = SEChome
        SEChomeAU = [dates(i,:),scores(i,1)];
        SEChomeOP = [dates(i,:),scores(i,2)];
end

%Find SEC away games
SECaway =  find(contains(sec,'sec') & contains(location, 'at'));
for i = SECaway
        SECawayAU = [dates(i,:),scores(i,1)];
        SECawayOP = [dates(i,:),scores(i,2)];   
end


%*****OUTPUT*****

%Print data
fprintf('Season Average Scores by Category \n')
fprintf('                  Home        Away     \n')
fprintf('                AU    Opp   AU    Opp  \n')
fprintf('SEC games      %.2f   %.2f  %.2f  %.2f \n', mean(SEChomeAU(:,3)), mean(SEChomeOP(:,3)), mean(SECawayAU(:,3)), mean(SECawayOP(:,3)))
fprintf('nonSEC games   %.2f   %.2f  %.2f  %.2f \n', mean(homeAU(:,3)), mean(homeOP(:,3)), mean(awayAU(:,3)), mean(awayOP(:,3)))
fprintf('\nSeason Highest Scores and Game Dates by Category \n')
fprintf('                    Home                 Away     \n')
fprintf('              Auburn    Opponent    Auburn    Opponent  \n')
[auBestSEChome,dateABSH]= max(SEChomeAU(:,3));
[opBestSEChome,dateOPSH]= max(SEChomeOP(:,3));
[auBestSECaway,dateABSA]= max(SECawayAU(:,3));
[opBestSECaway,dateOPSA]= max(SECawayOP(:,3));
fprintf('SEC games    %d %02d/%02d   %d %02d/%02d   %d %02d/%02d   %d  %02d/%02d\n', auBestSEChome,SEChomeOP(dateABSH,1),SEChomeAU(dateABSH,2),opBestSEChome,SEChomeOP(dateOPSH,1),SEChomeOP(dateOPSH,2),auBestSECaway,SECawayAU(dateABSA,1),SECawayAU(dateABSA,2),opBestSECaway,SECawayOP(dateOPSA,1),SECawayOP(dateOPSA,2))
[auBesthome,dateABH]= max(homeAU(:,3));
[opBesthome,dateOPH]= max(homeOP(:,3));
[auBestaway,dateABA]= max(awayAU(:,3));
[opBestaway,dateOPA]= max(awayOP(:,3));
fprintf('nonSEC games %d %02d/%02d   %d %02d/%02d    %d %02d/%02d   %d  %02d/%02d\n', auBesthome,homeOP(dateABH,1),homeAU(dateABH,2),opBesthome,homeOP(dateOPH,1),homeOP(dateOPH,2),auBestaway,awayAU(dateABA,1),awayAU(dateABA,2),opBestaway,awayOP(dateOPA,1),awayOP(dateOPA,2))

%User defined function draws graph
printPie(SEChomeAU,SEChomeOP,SECawayAU,SECawayOP,homeAU,homeOP,awayAU,awayOP)

