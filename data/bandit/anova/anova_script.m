a = csvread('dfs',1,0);
anovan(a(:,5),a(:,2:4),'model', 'interaction','varnames', {'method','arms','cost'});