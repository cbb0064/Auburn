function [] = reportGraph(dates,scores,stats)
%Develop a table using the information provided

%Calculate Batting Average
batAve = (stats (:,3) ./ stats(:,1));
games=length(scores);
%Print headers
fprintf('2020 AU Softball Batting Stats as of ')
fprintf('%02d/%02d\n', dates(games,1),dates(games,2))
fprintf('Date       Score     W/L      AB     Runs   Hits   HRuns   Ave\n')


for i=1:games
    fprintf('%02d/%02d      %02d-%02d    ', dates(i,:), scores(i,:))
    if scores(i,1)>scores(i,2)
        fprintf('  W       ')
    else
        fprintf('  L       ')
    end
    
fprintf('%2d      %2d     %2d     %2d    %4.3f\n', stats(i,:),batAve(i) )

end
%Print averages
fprintf('Ave:      %.1f-%.1f       %10.2f  %5.2f%7.1f    %.1f   %.3f\n', mean(scores(:,1)), mean(scores(:,2)), mean(stats(:,1)), mean(stats(:,2)), mean(stats(:,3)), mean(stats(:,4)),mean(batAve))
graphScores(scores)
end
function[]=graphScores(scores)
%Draw a bargraph that compares scores
bar(scores, 'stacked')
title('2020 AU Softball Score');
xlabel('Game Number');
ylabel('Scores');
legend('Auburn','Opponents')
end
