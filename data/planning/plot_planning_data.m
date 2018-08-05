included = [4,2,1,5];
labels = {'BMPS',	'Blinkered',	'Full Deliberation',	'Meta-greedy' 	'Optimal'};
means_depth = csvread('depth_mean.csv',1,0);
ci_depth = csvread('depth_ci.csv',1,0);

%means = means(:,[1 6 5 7 3 4 8]);

fig = figure();
ax = axes;

% hold on
% for i = 1:length(means)
%     h=bar(means(i,1),means(i,2:end));
%     set(h,'FaceColor',myColorOrder(i));
% end
% hold off

hb = barwitherr(ci_depth(:,included+1),means_depth(:,1),means_depth(:,included+1)); hold on;

myColorOrder = [[0.6350 0.0780 0.1840];[0.8500 0.3250 0.0980];[0 0.4470 0.7410];[0.4660 0.6740 0.1880];[0.9290 0.6940 0.1250];[0.4940 0.1840 0.5560]];
set(gca, 'ColorOrder', myColorOrder, 'NextPlot', 'replacechildren');

% X and Y labels
xlabel ('Tree Height','FontSize',30);
ylabel ('Metareasoning Performance','FontSize',30);

xt = get(gca, 'XTick');
set(gca, 'FontSize', 24)
ylim([0,0.55]);

%lg = legend('Full Deliberation','DQN','Meta-greedy', 'BMPS', 'Blinkered', 'Optimal','AutoUpdate','off');
lg = columnlegend(2,labels(included))
lg.Location = 'NorthWest';
% lg.Orientation = 'Horizontal';

hold on;

nbars = size(means_depth, 1)-1;
ngroups = size(means_depth, 2)-1;

groupwidth = min(0.8, nbars/(nbars + 1.5));


for i = 1:nbars
    % Calculate center of each bar
    %xo = (1:ngroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*nbars);
    %errorbar(xo + 1, means_depth(:,i+1), ci_depth(:,i+1), 'k', 'linestyle', 'none');
    hb(i).FaceColor = myColorOrder(i,:);
end

% figh = figure(1);
% pos = get(figh,'position');
% set(figh,'position',[pos(1:2)/4 pos(3:4)*1.3])

%% 
included = [1,2,3,4,5];
labels = {'BMPS',	'Blinkered',	'Full Deliberation',	'Meta-greedy' 	'Optimal'};
means_cost = csvread('cost_mean.csv',1,0);
ci_cost = csvread('cost_ci.csv',1,0);

%means = means(:,[1 6 5 7 3 4 8]);

fig = figure();
ax = axes;

% hold on
% for i = 1:length(means)
%     h=bar(means(i,1),means(i,2:end));
%     set(h,'FaceColor',myColorOrder(i));
% end
% hold off

hb = errorbar(repmat(means_cost(:,1),[1,5]),means_cost(:,included+1),ci_cost(:,included+1),'LineWidth',3); hold on;
set(ax,'xscale','log')
% X and Y labels
xlabel ('Cost of Computation','FontSize',30);
ylabel ('Metareasoning Performance','FontSize',30);

xt = get(gca, 'XTick');
set(gca, 'FontSize', 24)
myColorOrder = [[0.9290 0.6940 0.1250];[0.6350 0.0780 0.1840];[0.4940 0.1840 0.5560];[0 0.4470 0.7410];[0.8500 0.3250 0.0980];[0.4660 0.6740 0.1880]];
set(gca, 'ColorOrder', myColorOrder, 'NextPlot', 'replacechildren');
ylim([0,0.8]);
xlim([0.01,1])

%lg = legend('Full Deliberation','DQN','Meta-greedy', 'BMPS', 'Blinkered', 'Optimal','AutoUpdate','off');
lg = columnlegend(2,labels(included))
lg.Location = 'NorthWest';
% lg.Orientation = 'Horizontal';