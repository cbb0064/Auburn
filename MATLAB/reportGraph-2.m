function [] = reportGraph(dates,scores,location,opponent)
%Develop a table using the information provided

%Find scores for only home games
games=length(scores);
%Print headers
fprintf('2020 AU Softball Batting Stats as of ')
fprintf('%02d/%02d\n', dates(games,1),dates(games,2))
fprintf('Date       Opponent          Score   W/L\n')


for i=1:games
    if strfind(location{i}, 'home')
        fprintf('%02d/%02d      %-16s  %02d-%02d  ', dates(i,:), opponent {i,:}, scores(i,:))
    if scores(i,1)>scores(i,2)
        fprintf('  W \n')
    else
        fprintf('  L  \n')
    end
    end
end
%Find season record without loops
auDubs = length(find(scores(:,1)>scores(:,2)));
auCries = games - auDubs;
[bigDiff,dateSp]= max(abs(scores(:,1)- scores(:,2)));
[auBest,dateAb]= max(scores(1,:));
[opBest,dateOb]= max(scores(2,:));
fprintf('\nSeason Record:\n')
fprintf('Wins-Losses:       %d-%d\n',auDubs,auCries)
fprintf('Largest pt spread: %-3d on %02d/%02d\n', bigDiff,dates(dateSp,1),dates(dateSp,2));
fprintf('Most AU runs:      %-3d on %02d/%02d\n', auBest,dates(dateAb,1),dates(dateAb,2));
fprintf('Most Opp runs:     %-3d on %02d/%02d\n', opBest,dates(dateOb,1),dates(dateOb,2));
graphScores(scores)
end

function [] = graphScores(scores)
%Draw two graphs that compare scores of home versus away
auburn = [scores(:,1)];
op = [scores(:,2)];
subplot(2,1,1);plot(auburn, ':ro')
title('2020 Auburn Softball Scores')
xlabel('Game Number');
ylabel('Scores');
subplot(2,1,2);plot(op, '--gs')
title('2020 Opponent Softball Scores')
xlabel('Game Number');
ylabel('Scores');
end
