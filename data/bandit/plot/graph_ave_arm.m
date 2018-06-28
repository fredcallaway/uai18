means = csvread('mean_by_arm',1,0);
means = means(:,[1 6 5 7 3 4 8]);

errs = csvread('error_by_arm',1,0);
errs = errs(:,[1 6 5 7 3 4 8]);

fig = figure();
ax = axes;

% hold on
% for i = 1:length(means)
%     h=bar(means(i,1),means(i,2:end));
%     set(h,'FaceColor',myColorOrder(i));
% end
% hold off

hb = bar(means(:,1),means(:,2:end)); hold on;

% X and Y labels
xlabel ('Number of Options');
ylabel ('Metareasoning Performance');

xt = get(gca, 'XTick');
set(gca, 'FontSize', 16)
myColorOrder = [[0.9290 0.6940 0.1250];[0.6350 0.0780 0.1840];[0.4940 0.1840 0.5560];[0 0.4470 0.7410];[0.8500 0.3250 0.0980];[0.4660 0.6740 0.1880]];
set(gca, 'ColorOrder', myColorOrder, 'NextPlot', 'replacechildren');
ylim([0,1]);

lg = legend('Full Deliberation','DQN','Meta-greedy', 'BMPS', 'Blinkered', 'Optimal','AutoUpdate','off');
lg.Location = 'NorthWest';
% lg.Orientation = 'Horizontal';

hold on;

ngroups = size(means, 1);
nbars = size(means, 2)-1;

groupwidth = min(0.8, nbars/(nbars + 1.5));

for i = 1:nbars
    % Calculate center of each bar
    xo = (1:ngroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*nbars);
    errorbar(xo + 1, means(:,i+1), errs(:,i+1), 'k', 'linestyle', 'none');
    hb(i).FaceColor = myColorOrder(i,:);
end

% figh = figure(1);
% pos = get(figh,'position');
% set(figh,'position',[pos(1:2)/4 pos(3:4)*1.3])
