%{
Cameron Beck
File name: assign09.m
COMP1200 - Spring 2020
Due Date: Apr 20, 2020
Worked without a group however needed to consult a classmate for trouble
with textread and isolating columns for the matricies
Read a file using text read then write a report and draw a graph using a user defined
function
%}

clc, clear all
format short

%***** CONSTANTS *****
FILENAME = 'AU_SB_2020_09.txt' ;

%Check to see if file exists
if ~exist(FILENAME, 'file')
    disp('File not available')
end

%***** INPUT *****

%Develop matricies
dates = [];
scores = [];
%Read the text file for data and input into matricies
[dates(:,1),dates(:,2),location, opponent, scores(:,1),scores(:,2)]=textread('AU_SB_2020_09.txt','%d%d%s%s%f%f%*f%*f%*f%*f');

%***** OUTPUT *****
%Use a user defined function to create a report and graph

reportGraph(dates,scores,location,opponent)

