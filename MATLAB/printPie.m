function [] = printPie(SEChomeAU,SEChomeOP,SECawayAU,SECawayOP,homeAU,homeOP,awayAU,awayOP)
%Draw two pie charts

%Draw the away graph
graph1AU = sum(SECawayAU(:,3));%Find Auburn percentage for first graph
graph1AUB= sum(awayAU(:,3));
graph1Auburn = sum(graph1AU + graph1AUB);
graph1OP = sum(SECawayOP(:,3));%Find Opponent percentage for first graph
graph1OPP= sum(awayOP(:,3));
graph1OPPO = sum(graph1OP + graph1OPP);
graph1 = [graph1Auburn,graph1OPPO];
labels = {'Auburn','Opponents'};
pie(graph1,labels)
title('Season Total Runs for Away Games')

%Draw the home graph
figure;
graph2AU = sum(SEChomeAU(:,3));%Find Auburn percentage for first graph
graph2AUB= sum(homeAU(:,3));
graph2Auburn = sum(graph2AU + graph2AUB);
graph2OP = sum(SEChomeOP(:,3));%Find Opponent percentage for first graph
graph2OPP= sum(homeOP(:,3));
graph2OPPO = sum(graph2OP + graph2OPP);
graph2 = [graph2Auburn,graph2OPPO];
labels = {'Auburn','Opponents'};
pie(graph2,labels)
title('Season Total Runs at Jane B Moore Field (home)')





